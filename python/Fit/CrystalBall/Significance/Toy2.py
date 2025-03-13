import ROOT
import re
from ROOT import TH1D, TH2D, TCanvas, TChain, TTree, TString, TFile, gInterpreter, gSystem, RooMinimizer
from math import *
import sys
import numpy as np
from os import path, listdir, makedirs
import os
from array import array
import ctypes
from datetime import datetime
import time
import argparse
import uuid
import pandas as pd
import scipy.stats as st 
from statsmodels.robust.scale import mad


def SeedChange():
    seed = abs(uuid.uuid4().int) % (2**32)
    ROOT.gRandom.SetSeed(seed)

def MakeLabels(target_particle):
    if target_particle == "xiccpp":
         x_label = "m(#Xi_{cc}^{++}) [GeV/c^{2}]"
    if target_particle == "lambdac":
        x_label = "m(#Lambda_{c}^{+}) [GeV/c^{2}]"
    if target_particle == "xicp":
        x_label = "m(#Xi_{c}^{+}) [GeV/c^{2}]"
    if target_particle == "xiccp":
        x_label = "m(#Xi_{cc}^{+}) [GeV/c^{2}]"
    return x_label

def ExtractEff(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Regex pattern to match floating point numbers (including scientific notation)
    pattern = (
        r"Efficiency\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*\+-\s*"
        r"([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"
    )
    match = re.search(pattern, content)
    if match:
        efficiency = float(match.group(1))
        error = float(match.group(2))
        return efficiency, error
    else:
        raise ValueError("Efficiency data not found in the file.") 

class VariableStore:
    def __init__(self, control_workspace_file, control_efficiency_purity_file,signal_efficiency_purity_file):
        self.control_file = ROOT.TFile(control_workspace_file)
        self.control_w = self.control_file.Get("w")
        self.control_model = self.control_w["model"]
       
        self.control_efficiency, self.control_efficiency_error = ExtractEff(control_efficiency_purity_file)
        self.signal_efficiency, self.signal_efficiency_error = ExtractEff(signal_efficiency_purity_file)
      

class Toy:
    def __init__(self, workspace_file,f_value,suppresion_factor,VariableStore=None, R_value = 1):
        self.variables = VariableStore
        self.file = ROOT.TFile(workspace_file)
        self.w = self.file.Get("w")
        self.model = self.w["model"]
        self.data = self.w["data"]
        self.run_diagnostics = self.w["RunDiagnostics"]
        self.run_params = self.w["RunParams"]
        self.outputs = self.w["Outputs"]
        self.x = self.w.var("x")

        self.original_nbkg = self.model.getVariables().find("nbkg").getVal()
        self.original_nsig = self.model.getVariables().find("nsig").getVal()
        
        self.f = f_value
        self.R = R_value
        self.suppresion_factor = suppresion_factor
        self.generated_data = None
    
    def ScaleSignal(self):
        # to run control mode, simpily dont use 
        self.control_signal = self.variables.control_model.getVariables().find("nsig")
        control_signal_val = self.control_signal.getVal()
        scaled_signal = self.R*control_signal_val*(self.variables.signal_efficiency/self.variables.control_efficiency)
        signal_eff_err_prop = (self.variables.signal_efficiency_error/self.variables.signal_efficiency)**2
        control_eff_err_prop = (self.variables.control_efficiency_error/self.variables.control_efficiency)**2
        control_signal_err_prop = (self.control_signal.getError()/self.control_signal.getVal())**2
        scaled_signal_error = scaled_signal*np.sqrt(signal_eff_err_prop + control_eff_err_prop + control_signal_err_prop)
        self.model.getVariables().find("nsig").setVal(scaled_signal)
        self.model.getVariables().find("nsig").setError(scaled_signal_error)
        self.original_nsig = scaled_signal

    def FluctuateBackground(self):
        SeedChange()
        variable_for_fluctuation = self.model.getVariables().find("nbkg")
        fluctuated_variable = ROOT.gRandom.Poisson(self.original_nbkg)
        variable_for_fluctuation.setVal(fluctuated_variable)
    
    def FluctuateSignal(self):
        SeedChange()
        variable_for_fluctuation = self.model.getVariables().find("nsig")
        fluctuated_variable = ROOT.gRandom.Poisson(self.original_nsig)
        variable_for_fluctuation.setVal(fluctuated_variable)
    
    def FluctuateYields(self):
        self.FluctuateSignal()
        self.FluctuateBackground()
    
    def ScaleBackground(self):
         self.original_nbkg = self.model.getVariables().find("nbkg").getVal()*self.f*self.suppresion_factor
         self.model.getVariables().find("nbkg").setVal( self.model.getVariables().find("nbkg").getVal()*self.f*self.suppresion_factor)
    
    def GenerateModel(self):
        SeedChange()
        n_points = int(self.model.getVariables().find("nsig").getVal() + self.model.getVariables().find("nbkg").getVal())
        self.generated_data = self.model.generate(ROOT.RooArgSet(self.w["x"]), n_points)
    
    def PrintAllParameters(self):
        print("Model Parameters:")
        for param in self.model.getVariables():
            print(f"{param.GetName()} = {param.getVal()}")
    
    def Fit_ResetLimit(self,parameter,min,max):
        param = self.w.var(parameter)
        param.setRange(min, max)

    def Fit_GetSignificance(self):
        mu = self.w.var("mu1")
        sigma = self.w.var("sigma1")
        nsig = self.w.var("nsig")
        nbkg = self.w.var("nbkg")
        significance = ROOT.RooFormulaVar("significance",  "significance", "nsig/sqrt(nsig + nbkg)",  ROOT.RooArgList(nsig, nbkg))
        minos_params = ROOT.RooArgSet(mu, sigma, nsig, nbkg)
        fit_result = self.model.fitTo(self.generated_data, ROOT.RooFit.PrintLevel(-1),
                                      ROOT.RooFit.Strategy(1),
                                      ROOT.RooFit.Minimizer("Minuit2"),
                                      ROOT.RooFit.Extended(True),
                                      ROOT.RooFit.Save(),
                                      ROOT.RooFit.Minos(False),
                                      ROOT.RooFit.Optimize(True),
                                      ROOT.RooFit.MaxCalls(500000))
        significance_value = significance.getVal()
        significance_error = significance.getPropagatedError(fit_result)
        return significance_value, significance_error, fit_result.status()




    def Fit_Visualise(self,particle,timing, number_of_bins = 30):
        timing_int = int(timing)
        x_label = MakeLabels(particle)
        mu = self.w.var("mu1")
        sigma = self.w.var("sigma1")
        nsig = self.w.var("nsig")
        nbkg = self.w.var("nbkg")

        minos_params = ROOT.RooArgSet(mu, sigma, nsig, nbkg)

        fit_result = self.model.fitTo(self.generated_data, ROOT.RooFit.PrintLevel(-1),
                                      ROOT.RooFit.Strategy(2),
                                      ROOT.RooFit.Minimizer("Minuit2"),
                                      ROOT.RooFit.Extended(True),
                                      ROOT.RooFit.Save(),
                                      ROOT.RooFit.Minos(minos_params),
                                      ROOT.RooFit.Optimize(True),
                                      ROOT.RooFit.MaxCalls(500000))

        # --------------------------- Plotting Initialisation -----------------------------------
        for param in [mu, sigma, nsig, nbkg]:
            print(f"{param.GetName()}:")
            print(f"   Value: {param.getVal()}")
            print(f"   Error (Symmetric): {param.getError()}")
            print(f"   Error (MINOS Lower): {param.getAsymErrorLo()}")
            print(f"   Error (MINOS Upper): {param.getAsymErrorHi()}")
        fit_result.Print()
        frame1 = self.x.frame()
        frame1.SetTitle("")
        self.generated_data.plotOn(frame1, ROOT.RooFit.Name("data"), ROOT.RooFit.Binning(number_of_bins), ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        self.model.plotOn(frame1, ROOT.RooFit.Name("sig+bkg"), ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.LineStyle(ROOT.kSolid))
        self.model.plotOn(frame1, ROOT.RooFit.Components("bkg"), ROOT.RooFit.Name("bkg"), ROOT.RooFit.LineColor(ROOT.kMagenta), ROOT.RooFit.LineStyle(ROOT.kDashed))
        self.model.plotOn(frame1, ROOT.RooFit.Components("sig"), ROOT.RooFit.Name("sig"), ROOT.RooFit.LineColor(ROOT.kRed), ROOT.RooFit.LineStyle(ROOT.kDotted))
        chi2 = frame1.chiSquare("sig+bkg", "data", 6)
        hpull = frame1.pullHist("data", "sig+bkg")
        frame2 = self.x.frame()
        frame2.SetTitle("")
        frame2.addPlotable(hpull, "P")
        line = ROOT.TLine(frame2.GetXaxis().GetXmin(), 0, frame2.GetXaxis().GetXmax(), 0)
        line.SetLineColor(ROOT.kBlue)
        
        # --------------------------- Plotting -----------------------------------
        energy_range = ((frame1.GetXaxis().GetXmax() - frame1.GetXaxis().GetXmin()) / number_of_bins)*1000
        # Set up canvas and drawing
        c = ROOT.TCanvas("rf201_composite", "rf201_composite", 1600, 600)
        c.Divide(2)

        # First pad
        c.cd(1)
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.050)
        latex.SetTextFont(62)
        ROOT.gPad.SetLeftMargin(0.15)
        ROOT.gStyle.SetLineScalePS(1.2)
        frame1.GetYaxis().SetTitle(f"Entries/ ({round(energy_range,3)} MeV/c^{{2}})")
        frame1.GetXaxis().SetTitle(x_label)  # You can replace with the actual label
        frame1.GetYaxis().SetTitleOffset(1.15)
        frame1.GetXaxis().SetTitleOffset(1)
        frame1.GetYaxis().SetTitleFont(62)
        frame1.GetXaxis().SetTitleFont(62)
        frame1.GetYaxis().SetTitleSize(0.06)
        frame1.GetXaxis().SetTitleSize(0.06)
        frame1.GetXaxis().SetLabelSize(0.05)
        frame1.GetYaxis().SetLabelSize(0.05)
        frame1.GetXaxis().SetLabelFont(62)
        frame1.GetYaxis().SetLabelFont(62)
        frame1.Draw()

        # Add the legend with LaTeX formatting
        legend = ROOT.TLegend(0.67, 0.7, 0.97, 0.915)
        legend.SetLineColor(0)
        legend.SetLineStyle(0)
        legend.SetLineWidth(0)
        legend.SetFillColor(0)
        legend.SetFillStyle(0)
        legend.SetTextFont(62)
        legend.SetTextSize(0.045)
        legend.AddEntry("data", "Data", "lep")
        legend.AddEntry("sig+bkg", "Total", "l")

        # Dummy lines for correct styles in the legend
        dummy_bkg_line = ROOT.TLine()
        dummy_bkg_line.SetLineColor(ROOT.kMagenta)
        dummy_bkg_line.SetLineStyle(ROOT.kDashed)
        legend.AddEntry(dummy_bkg_line, "Background", "l")
        dummy_sig_line = ROOT.TLine()
        dummy_sig_line.SetLineColor(ROOT.kRed)
        dummy_sig_line.SetLineStyle(ROOT.kDotted)
        legend.AddEntry(dummy_sig_line, "Signal", "l")

        latex.DrawText(0.2, 0.875, "LHCb Simulation")
        latex.DrawLatex(0.2, 0.820, "#sqrt{s} = 14 TeV")
        latex.DrawLatex(0.2, 0.765, f"VELO {timing_int} ps")
        latex2 = ROOT.TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.045)
        latex2.SetTextFont(62)
        plot_time = time.strftime("%d %m %y", time.localtime())
        legend.Draw()

        # Second pad
        c.cd(2)
        ROOT.gPad.SetLeftMargin(0.15)
        frame2.GetYaxis().SetTitle("Pulls")
        frame2.GetXaxis().SetTitle(x_label)  # You can replace with the actual label
        frame2.GetYaxis().SetTitleOffset(0.65)
        frame2.GetXaxis().SetTitleOffset(1)
        frame2.GetYaxis().SetTitleSize(0.06)
        frame2.GetXaxis().SetTitleSize(0.06)
        frame2.GetYaxis().SetTitleFont(62)
        frame2.GetXaxis().SetTitleFont(62)
        frame2.GetXaxis().SetLabelSize(0.05)
        frame2.GetYaxis().SetLabelSize(0.05)
        frame2.GetXaxis().SetLabelFont(62)
        frame2.GetYaxis().SetLabelFont(62)
        frame2.Draw()
        line.Draw("same")

        c.cd()
        c.Update()
        c.Draw()

        # Save as PDF
        basedir= f"{path.dirname(path.realpath(__file__))}/../../.."
        c.SaveAs(f"{basedir}/Fit/CrystalBall/Significance/Figures/FitT.pdf","pdf 800")    

def MeanSignificanceControl(workspace_file,f_value,number_of_models=5):
    significances = []
    significance_errors = []
    for i in range(number_of_models):
        toy = Toy(workspace_file, f_value)
        toy.ScaleBackground()
        toy.FluctuateYields()
        toy.GenerateModel()
        #toy.Fit_ResetLimit("bkg_coef1", -3, 3)
        #toy.Fit_ResetLimit("bkg_coef2", -3, 3)
        toy.Fit_ResetLimit("nbkg", 100,8000)
        toy.Fit_ResetLimit("nsig",100,8000)
        significance, significance_error = toy.Fit_GetSignificance()
        significances.append(significance)
        significance_errors.append(significance_error)


def MeanSignificanceSignal(workspace_file, f_value, variables, velo_time=50, number_of_models=5, R_input = 1):
    significances = []
    
    # First loop to collect significances
    for i in range(number_of_models):
        toy = Toy(workspace_file, f_value,variables, R_value = R_input)
        toy.ScaleSignal()
        toy.ScaleBackground()
        toy.FluctuateYields()
        toy.GenerateModel()
        toy.Fit_ResetLimit("nbkg", 100,15000)
        toy.Fit_ResetLimit("nsig",1,8000)
        toy.Fit_ResetLimit("sigma1",0.003,0.015)
        toy.Fit_ResetLimit("mu1", 3,4.1)
        # add a line to discard fits that dont converge (flag errors)
        significance, significance_error,convergence = toy.Fit_GetSignificance()
        if convergence == 0:
            significances.append(significance)
        else:
            continue

    min_significance = min(significances) * 0.4  # Slightly lower than min value
    max_significance = max(significances) * 1.5  # Slightly higher than max value
    secondpercentile = np.percentile(significances,5)
    nintyseventhpercentile = np.percentile(significances,95)

   # secondpercentile, nintyseventhpercentile = st.norm.interval(0.9, 
                                                        #loc=np.mean(significances), 
                                                       # scale=st.sem(significances))
    #secondpercentile, nintyseventhpercentile = st.poisson.interval(0.95, np.mean(significances))



    # Define histogram after computing min and max
    hist = TH1D("Legend", f"Significance Distribution For R={R_input}", 40, min_significance, max_significance)
    hist.SetStats(False)  # This disables the stats box on the histogram


    # Second loop to fill the histogram
    for significance in significances:
        hist.Fill(significance)
    

    # Draw and save the histogram
    canvas = TCanvas("canvas", "Significance Histogram", 800, 600)
    hist.GetXaxis().SetTitle("Significance")  # Set x-axis title
    hist.GetYaxis().SetTitle("Entries")      # Set y-axis title to "Entries"
    hist.GetXaxis().SetTitleSize(0.04)   # Set title size for both axes
    hist.GetYaxis().SetTitleSize(0.04)
    hist.GetXaxis().SetLabelSize(0.04)   # Set label size
    hist.GetYaxis().SetLabelSize(0.04)
    hist.GetXaxis().SetTitleOffset(1)  # Set offset for title
    hist.GetYaxis().SetTitleOffset(1)
    hist.GetXaxis().SetLabelFont(62)     # Font style for labels
    hist.GetYaxis().SetLabelFont(62)
    hist.GetXaxis().SetTitleFont(62)     # Font style for titles
    hist.GetYaxis().SetTitleFont(62)
    # Create and draw vertical lines at the 3-sigma and 5-sigma values
    line_secondpercentile = ROOT.TLine(secondpercentile, 0, secondpercentile, hist.GetMaximum())
    line_secondpercentile.SetLineColor(ROOT.kRed)  # Red color for 3-sigma line
    line_secondpercentile.SetLineStyle(2)  # Dashed line for 3-sigma
    line_secondpercentile.SetLineWidth(2)
    line_nintyseventhpercentile = ROOT.TLine(nintyseventhpercentile, 0, nintyseventhpercentile, hist.GetMaximum())
    line_nintyseventhpercentile.SetLineColor(ROOT.kRed)  # Blue color for 5-sigma line
    line_nintyseventhpercentile.SetLineStyle(2)  # Dashed line for 5-sigma
    line_nintyseventhpercentile.SetLineWidth(2)
    legend = ROOT.TLegend(0.74, 0.7, 0.97, 0.9)
    legend.SetLineColor(0)
    legend.SetLineStyle(0)
    legend.SetLineWidth(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(62)
    legend.SetTextSize(0.04)
    legend.AddEntry(hist, "Data", "l")
    legend.AddEntry(line_secondpercentile, "95% SL", "l")
    hist.Draw("HIST")
    line_secondpercentile.Draw()
    legend.Draw()

    canvas.SaveAs(f"/home/user294/Documents/selections/python/Outputs/ToyPlots/RScan_Velo{velo_time}/{R_input}.pdf")
    return secondpercentile, nintyseventhpercentile

def MeanSignificanceSignalNoHist(workspace_file, f_value,suppresion_factor, variables, number_of_models=5, R_input = 1):
    significances = []
    
    # First loop to collect significances
    for i in range(number_of_models):
        toy = Toy(workspace_file, f_value,suppresion_factor,variables, R_value = R_input)
        toy.ScaleSignal()
        toy.ScaleBackground()
        toy.FluctuateYields()
        toy.GenerateModel()
        toy.Fit_ResetLimit("nbkg", 100,30000)
        toy.Fit_ResetLimit("nsig",1,30000)
        toy.Fit_ResetLimit("sigma1",0.003,0.015)
        toy.Fit_ResetLimit("mu1", 3,4.1)
        # add a line to discard fits that dont converge (flag errors)
        significance, significance_error,convergence = toy.Fit_GetSignificance()
        if (convergence == 0) and (significance > 0):
            significances.append(significance)
        else:
            continue
    secondpercentile = np.percentile(significances,5)
    nintyseventhpercentile = np.percentile(significances,95)
    significance_array = np.array(significances)
    num_above = np.sum(significance_array > secondpercentile)
    num_below = np.sum(significance_array <= secondpercentile)
    total = len(significances)
    p = num_above/total
    standard_error = np.sqrt(p*(1-p)/total)
    return secondpercentile, nintyseventhpercentile,standard_error

def RScan(workspace_file, f_value, variables, velo_time=50, number_of_models=5,start_point = 1, step_size = 0.1):
    results_dict = {
    "R": [],
    "UpperPercentile": [],
    "LowerPercentile": []}
    basedir= f"{path.dirname(path.realpath(__file__))}/../../.."
    makedirs(f"{basedir}/Outputs/ToyPlots/RScan_Velo{velo_time}", exist_ok = True)
    for R in  np.arange(start_point, 0, -step_size):
        second_percentile, nintyseventh_percentile = MeanSignificanceSignal(workspace_file, f_value, variables,number_of_models= number_of_models, R_input = R,velo_time=50)
        results_dict["R"].append(R)
        results_dict["LowerPercentile"].append(second_percentile)
        results_dict["UpperPercentile"].append(nintyseventh_percentile)
    df = pd.DataFrame(results_dict)
    df.to_csv(f"{basedir}/Outputs/ToyPlots/RScan_Velo{velo_time}/results.csv", index=False)

def RScanNoHist(workspace_file, f_value,suppresion_factor, variables, velo_time=50, number_of_models=5,start_point = 1, step_size = 0.1):
    results_dict = {
    "R": [],
    "UpperPercentile": [],
    "LowerPercentile": [],
    "StandardError": []}
    basedir= f"{path.dirname(path.realpath(__file__))}/../../.."
    makedirs(f"{basedir}/Outputs/ToyPlots/RScan_Velo{velo_time}", exist_ok = True)
    for R in  np.arange(start_point, 0, -step_size):
        second_percentile, nintyseventh_percentile,SE = MeanSignificanceSignalNoHist(workspace_file, f_value, suppresion_factor, variables,number_of_models= number_of_models, R_input = R)
        results_dict["R"].append(R)
        results_dict["LowerPercentile"].append(second_percentile)
        results_dict["UpperPercentile"].append(nintyseventh_percentile)
        results_dict["StandardError"].append(SE)
    df = pd.DataFrame(results_dict)
    df.to_csv(f"{basedir}/Outputs/ToyPlots/RScan_Velo{velo_time}/results.csv", index=False)


if __name__ == "__main__":
    basedir= f"/home/user294/Documents/selections/python"
    velo_time = 100
    signal_workspace_file = f"{basedir}/Outputs/XisToXis/Velo{velo_time}DanFix/xiccp_5_sigma/WSPACE.root"
    signal_efficiency_purity_file = f"{basedir}/Outputs/XisToXis/Velo{velo_time}DanFix/xiccp_5_sigma/PurityEfficiency.txt"
    control_efficiency_purity_file = f"{basedir}/Outputs/XisToLambdas/Velo{velo_time}DanFix/xiccpp_5_sigma/PurityEfficiency.txt"
    control_workspace_file = f"{basedir}/Outputs/XisToLambdas/Velo{velo_time}DanFix/xiccpp_5_sigma/WSPACE.root"
    f_values = {30: 2.3074, 50: 2.3074, 70: 2.3755, 100: 2.3074, 200: 2.3074}
    #f_values = {30: 2.4638, 50: 2.3074, 70: 2.3755, 100: 2.2675, 200: 2.9514}

    suppresion_factors = {30: 0.65 , 50: 0.76 ,70:0.91545893719
 , 100: 1.06}
    suppresion_factor = suppresion_factors[velo_time]
    f_value = f_values[velo_time]
    variables = VariableStore(control_workspace_file, control_efficiency_purity_file,signal_efficiency_purity_file)
    #RScan(signal_workspace_file, f_value, variables, velo_time=50, number_of_models=500,start_point = 1, step_size = 0.1)
    RScanNoHist(signal_workspace_file, f_value, suppresion_factor, variables, number_of_models=500,start_point = 0.2, step_size = 0.02, velo_time=velo_time)