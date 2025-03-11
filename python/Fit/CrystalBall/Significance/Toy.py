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
import lhcbstyle
from lhcbstyle import LHCbStyle
from datetime import datetime
import time
import argparse
import uuid

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
    def __init__(self, workspace_file,f_value,VariableStore=None):
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
        self.R = 0.04
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
         self.original_nbkg = self.model.getVariables().find("nbkg").getVal()*self.f
         self.model.getVariables().find("nbkg").setVal( self.model.getVariables().find("nbkg").getVal()*self.f)
    
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
                                      ROOT.RooFit.Strategy(2),
                                      ROOT.RooFit.Minimizer("Minuit2"),
                                      ROOT.RooFit.Extended(True),
                                      ROOT.RooFit.Save(),
                                      ROOT.RooFit.Minos(minos_params),
                                      ROOT.RooFit.Optimize(True),
                                      ROOT.RooFit.MaxCalls(5000000))
        significance_value = significance.getVal()
        significance_error = significance.getPropagatedError(fit_result)
        print(significance_value)
        return significance_value, significance_error




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
                                      ROOT.RooFit.MaxCalls(5000000))

        # --------------------------- Plotting Initialisation -----------------------------------
        for param in [mu, sigma, nsig, nbkg]:
            print(f"{param.GetName()}:")
            print(f"   Value: {param.getVal()}")
            print(f"   Error (Symmetric): {param.getError()}")
            print(f"   Error (MINOS Lower): {param.getAsymErrorLo()}")
            print(f"   Error (MINOS Upper): {param.getAsymErrorHi()}")
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
        with LHCbStyle() as lbs:
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
        toy.GenerateModel(n_points)
        #toy.Fit_ResetLimit("bkg_coef1", -3, 3)
        #toy.Fit_ResetLimit("bkg_coef2", -3, 3)
        toy.Fit_ResetLimit("nbkg", 100,8000)
        toy.Fit_ResetLimit("nsig",100,8000)
        significance, significance_error = toy.Fit_GetSignificance()
        significances.append(significance)
        significance_errors.append(significance_error)

def MeanSignificanceSignal(workspace_file, f_value, variables, velo_time=50, number_of_models=5):
    significances = []
    
    # First loop to collect significances
    for i in range(number_of_models):
        toy = Toy(workspace_file, f_value, variables)
        toy.ScaleBackground()
        toy.FluctuateYields()
        toy.GenerateModel()
        # toy.Fit_ResetLimit("bkg_coef1", -3, 3)
        # toy.Fit_ResetLimit("bkg_coef2", -3, 3)
        toy.Fit_ResetLimit("nbkg", 100, 8000)
        toy.Fit_ResetLimit("nsig", 100, 8000)
        significance, _ = toy.Fit_GetSignificance()
        significances.append(significance)

    print("Significances:", significances)

    # Determine histogram range dynamically
    if not significances:
        return None  # No data to plot

    min_significance = min(significances) * 0.9  # Slightly lower than min value
    max_significance = max(significances) * 1.1  # Slightly higher than max value

    # Define histogram after computing min and max
    hist = TH1D("significance_hist", "Significance Distribution", 20, min_significance, max_significance)

    # Second loop to fill the histogram
    for significance in significances:
        hist.Fill(significance)

    # Draw and save the histogram
    canvas = TCanvas("canvas", "Significance Histogram", 800, 600)
    hist.Draw()
    basedir= f"{path.dirname(path.realpath(__file__))}/../../.."
    makedirs(f"{basedir}/Outputs/ToyPlots/Velo{velo_time}")
    canvas.SaveAs(f"{basedir}/Outputs/ToyPlots/Velo{velo_time}/Significance.pdf")






if __name__ == "__main__":
    basedir= f"{path.dirname(path.realpath(__file__))}/../../.."
    signal_workspace_file = f"{basedir}/Outputs/XisToXis/Velo50DanFix/xiccp_5_sigma/WSPACE.root"
    signal_efficiency_purity_file = f"{basedir}/Outputs/XisToXis/Velo50DanFix/xiccp_5_sigma/PurityEfficiency.txt"
    control_efficiency_purity_file = f"{basedir}/Outputs/XisToLambdas/Velo50DanFix/xiccpp_5_sigma/PurityEfficiency.txt"
    control_workspace_file = f"{basedir}/Outputs/XisToLambdas/Velo50DanFix/xiccpp_5_sigma/WSPACE.root"

    velo_time = 50
    f_values = {30: 2.4638, 50: 2.3074, 70: 2.3755, 100: 2.2675, 200: 2.9514}
    # In case of bad results, break glass here ↓↓↓
    # f_values = {30: 2.3074, 50: 2.3074, 70: 2.3074, 100: 2.3074, 200: 2.3074}
    f_value = f_values[velo_time]
    #print(MeanSignificance(workspace_file,f_value,number_of_models=5))

    #control_toy = Toy(control_workspace_file, f_value)
    #control_toy.ScaleBackground()
    ##control_toy.FluctuateYields()
    #control_toy.GenerateModel()
    #control_toy.Fit_ResetLimit("nbkg", 100,10000)
    #control_toy.Fit_ResetLimit("nsig",100,10000)
   #control_toy.Fit_Visualise("xiccpp",50,30)

    variables = VariableStore(control_workspace_file, control_efficiency_purity_file,control_efficiency_purity_file)
    signal_toy = Toy(control_workspace_file, f_value, variables)
    signal_toy.ScaleSignal()
    signal_toy.ScaleBackground()
    signal_toy.FluctuateYields()
    signal_toy.GenerateModel()
    signal_toy.Fit_ResetLimit("nbkg", 100,20000)
    signal_toy.Fit_ResetLimit("nsig",100,20000)
    signal_toy.Fit_Visualise("xiccp",velo_time,30)
    MeanSignificanceSignal(control_workspace_file,f_value,variables,velo_time,number_of_models=5)

