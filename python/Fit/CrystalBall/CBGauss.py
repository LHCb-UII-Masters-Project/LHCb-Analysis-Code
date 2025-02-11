#---------------------------------Imports---------------------------------------------------
import ROOT
from Variables.Gauss import variables, fit_initial_guess_tree
from ROOT import TH1D, TH2D, TCanvas, TChain, TTree, TString, TFile,gInterpreter,gSystem,RooMinimizer
from math import * 
import sys
import numpy as np
from os import path, listdir
import os
from array import array
import ctypes
import lhcbstyle
from lhcbstyle import LHCbStyle
from datetime import datetime
import time
import argparse
#--------------------------------File Inputs---------------------------------------------------
parser = argparse.ArgumentParser(description='Open a ROOT file and process data.')
parser.add_argument('input_file', type=str, help='Path to the input ROOT file') 
args = parser.parse_args()
input_directory = os.path.dirname(args.input_file)
#-------------------------------Tree Reading---------------------------------------
root_file = ROOT.TFile.Open(args.input_file, "READ") 
run_tree = root_file.Get("RunParams")
outputs = root_file.Get("Outputs")
run_tree.SetDirectory(0)
outputs.SetDirectory(0)
root_file.Close()
#Use RDataFrame to access the data 
rdf = ROOT.RDataFrame(outputs) 
# Convert the bs_mass branch to a Numpy array
xiccpp_data = rdf.AsNumpy()["xiccpp_mass"]
unbinned_data = xiccpp_data[xiccpp_data > 1]
total_entries = outputs.GetEntries()
timing = array('f', [0])
PID_pion = array('f', [0])
PID_kaon= array('f', [0])
run_tree.SetBranchAddress("velo_timing", timing)
run_tree.SetBranchAddress("PID_pion", PID_pion)
run_tree.SetBranchAddress("PID_kaon", PID_kaon)
run_tree.GetEntry(0)
timing_value = (timing[0])
PID_pion_value = (PID_pion[0])
PID_kaon_value = (PID_kaon[0])
#-------------------------Data Filtering--------------------------------
x = ROOT.RooRealVar("x", "x", min(unbinned_data), max(unbinned_data))
data = ROOT.RooDataSet("data", "dataset with x", ROOT.RooArgSet(x))
for dp in unbinned_data: # change to filtered data for filtering
    x.setVal(dp)
    data.add(ROOT.RooArgSet(x))
# --------------------------- Variables and PDF Declerations -----------------------------------
mu = ROOT.RooRealVar("mu1", "mean of CB1", variables['mu']['value'], variables['mu']['min'], variables['mu']['max'])  # Gaussian core mean estimate
#mu.setConstant(True)
sigma = ROOT.RooRealVar("sigma1", "std of core gaussian 1", variables['sigma']['value'], variables['sigma']['min'], variables['sigma']['max'])  # Gaussian core std estimate
sig = ROOT.RooGaussian("sig", "Gaussian PDF", x, mu, sigma)
# Number of signal events (floating parameter)
nsig = ROOT.RooRealVar("nsig", "number of signal events", variables['nsig']['value'], variables['nsig']['min'], variables['nsig']['max'])
# Define an extended model where nsig represents the expected number of signal events
model = ROOT.RooExtendPdf("model", "Extended Signal Model",ROOT.RooArgSet(sig), ROOT.RooArgSet(nsig))
#-------------------------------------PDF Fitting-------------------------------------------------------------
minos_params = ROOT.RooArgSet(mu,sigma,nsig)
fit_result = model.fitTo(data, ROOT.RooFit.PrintLevel(-1), 
                         ROOT.RooFit.Strategy(2),
                           ROOT.RooFit.Minimizer("Minuit",'migradimproved'),
                           ROOT.RooFit.Extended(True),
                           ROOT.RooFit.Save(),
                           ROOT.RooFit.Minos(minos_params),
                           ROOT.RooFit.Optimize(True),
                           ROOT.RooFit.MaxCalls(5000000))
# --------------------------- Plotting Initialisation -----------------------------------
number_of_bins = 50
frame1 = x.frame()
frame1.SetTitle("")
data.plotOn(frame1,ROOT.RooFit.Name("data"),ROOT.RooFit.Binning(number_of_bins))
model.plotOn(frame1, ROOT.RooFit.Components("sig"),ROOT.RooFit.Name("sig"), ROOT.RooFit.LineColor(ROOT.kRed), ROOT.RooFit.LineStyle(ROOT.kDotted),ROOT.RooFit.LineStyle(ROOT.kDotted))  # Overall DCB
chi2 = frame1.chiSquare("sig", "data",9)
hpull = frame1.pullHist("data", "sig")
frame2 = x.frame()
frame2.SetTitle("")
frame2.addPlotable(hpull, "P")
line = ROOT.TLine(frame2.GetXaxis().GetXmin(), 0, frame2.GetXaxis().GetXmax(), 0)
line.SetLineColor(ROOT.kBlue)
origin_file_path = root_file.GetName()
origin_file_name = os.path.basename(origin_file_path)
origin_file_name_reduced = origin_file_name.replace(".root", "")
current_time = time.strftime("%H-%M-%S_%d-%m-%Y", time.localtime())
# --------------------------- Plotting -----------------------------------
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
    ROOT.gPad.SetLogy() # Turn on logarithmic scale for Y-axis
    ROOT.gStyle.SetLineScalePS(1.2)
    frame1.GetYaxis().SetTitle("Entries/ (10 MeV/c^{2})")
    frame1.GetXaxis().SetTitle("m(Xi_{cc}^{pp}) [MeV/c^{2}]")
    frame1.GetYaxis().SetTitleOffset(0.9)
    frame1.GetXaxis().SetTitleOffset(1)
    frame1.GetYaxis().SetTitleFont(62) 
    frame1.GetXaxis().SetTitleFont(62)
    frame1.GetYaxis().SetTitleSize(0.06) # Increase this value to make the font size larger
    frame1.GetXaxis().SetTitleSize(0.06) # Increase this value to make the font size larger
    frame1.GetXaxis().SetLabelSize(0.05)
    frame1.GetYaxis().SetLabelSize(0.05)
    frame1.GetXaxis().SetLabelFont(62)
    frame1.GetYaxis().SetLabelFont(62)
    frame1.Draw()
    # Add the legend with LaTeX formatting, without a legend box, and matching LaTeX font
    legend = ROOT.TLegend(0.67, 0.7, 0.97, 0.915) 
    legend.SetLineColor(0)  # Remove the legend border
    legend.SetLineStyle(0)  # Ensure no border line style
    legend.SetLineWidth(0)  # Set line width to 0
    legend.SetFillColor(0)  # Remove any fill color
    legend.SetFillStyle(0)  # Ensure no fill style
    legend.SetTextFont(62)  # Helvetica, normal
    legend.SetTextSize(0.045)  # Adjust text size as needed
    legend.AddEntry("data", "Data", "lep")  # Points with error bars
    legend.AddEntry("sig", "Signal", "l")  # Solid blue line
    dummy_sig_line = ROOT.TLine()
    dummy_sig_line.SetLineColor(ROOT.kRed)
    dummy_sig_line.SetLineStyle(ROOT.kDotted)
    legend.AddEntry(dummy_sig_line, "Signal", "l")  # Red dotted line
    latex.DrawText(0.2,0.875,"LHCb Simulation")
    latex.DrawLatex(0.2, 0.820, "#sqrt{s} = 14 TeV") 
    timing_int = int(timing_value)
    latex.DrawLatex(0.2, 0.765, (f"VELO {timing_int} ps")) 
    latex2 = ROOT.TLatex() 
    latex2.SetNDC() 
    latex2.SetTextSize(0.045)  
    latex2.SetTextFont(62)
    plot_time = time.strftime("%d %m %y", time.localtime())
    # latex2.DrawLatex(0.1, 0.077, f"J.McQueen ({plot_time})")
    legend.Draw()
    c.cd(2)
    ROOT.gPad.SetLeftMargin(0.15)
    frame2.GetYaxis().SetTitle("Pulls")
    frame2.GetXaxis().SetTitle("m(Xi_{cc}}^{pp}) [MeV/c^{2}]")
    frame2.GetYaxis().SetTitleOffset(0.65)
    frame2.GetXaxis().SetTitleOffset(1)
    frame2.GetYaxis().SetTitleSize(0.06) # Increase this value to make the font size larger
    frame2.GetXaxis().SetTitleSize(0.06) # Increase this value to make the font size larger
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
    c.SaveAs(f"{input_directory}/F_{current_time}_{origin_file_name_reduced}.pdf","pdf 800")

output_file = ROOT.TFile(f"{input_directory}/F_{current_time}_{origin_file_name_reduced}.root", "RECREATE")
c.Write()
#-------------------------------------------Main Tree Initialisation----------------------------------------------
tree = ROOT.TTree("fit_parameters", "Fit Parameters Tree")
mean_val = ROOT.std.vector('float')()
mean_err_high = ROOT.std.vector('float')()
mean_err_low = ROOT.std.vector('float')()
mean_err_sym = ROOT.std.vector('float')()
sigma_val = ROOT.std.vector('float')()
sigma_err_high = ROOT.std.vector('float')()
sigma_err_low = ROOT.std.vector('float')()
sigma_err_sym = ROOT.std.vector('float')()
chi2_val = ROOT.std.vector('float')()
nsig_val = ROOT.std.vector('float')()
nsig_err_high = ROOT.std.vector('float')()
nsig_err_low = ROOT.std.vector('float')()
nsig_err_sym = ROOT.std.vector('float')()
timing_val = ROOT.std.vector('float')()
pid_kaon_flag = ROOT.std.vector('float')()
pid_pion_flag = ROOT.std.vector('float')()
mean_val.push_back(mu.getVal())
mean_err_high.push_back(mu.getAsymErrorHi())
mean_err_low.push_back(mu.getAsymErrorLo())
mean_err_sym.push_back(mu.getError())
sigma_val.push_back(sigma.getVal())
sigma_err_high.push_back(sigma.getAsymErrorHi())
sigma_err_low.push_back(sigma.getAsymErrorLo())
sigma_err_sym.push_back(sigma.getError())
chi2_val.push_back(chi2)
nsig_val.push_back(nsig.getVal())
nsig_err_high.push_back(nsig.getAsymErrorHi())
nsig_err_low.push_back(nsig.getAsymErrorLo())
nsig_err_sym.push_back(nsig.getError())
timing_val.push_back(timing_value)
pid_kaon_flag.push_back(PID_kaon_value)
pid_pion_flag.push_back(PID_pion_value)
# --------------------------- Main Tree Branches -----------------------------------
tree.Branch("timing",timing_val)
tree.Branch("pid_kaon_flag",pid_kaon_flag)
tree.Branch("pid_pion_flag",pid_pion_flag)
tree.Branch("mean", mean_val)
tree.Branch("mean_error_high", mean_err_high)
tree.Branch("mean_error_low", mean_err_low)
tree.Branch("mean_error_sym", mean_err_sym)
tree.Branch("sigma", sigma_val)
tree.Branch("sigma_error_high", sigma_err_high)
tree.Branch("sigma_error_low", sigma_err_low)
tree.Branch("sigma_error_sym", sigma_err_sym)
tree.Branch("chi2", chi2_val)
tree.Branch("nsig", nsig_val)
tree.Branch("nsig_error_high", nsig_err_high)
tree.Branch("nsig_error_low", nsig_err_low)
tree.Branch("nsig_error_sym", nsig_err_sym)
tree.Branch("timing", timing_val)
tree.Branch("pid_kaon_flag", pid_kaon_flag)
tree.Branch("pid_pion_flag", pid_pion_flag)
tree.Fill()
#--------------------------- Summary Vectors -----------------------------------
summary = ROOT.TTree("summary", "summary")
sig_yield = ROOT.std.vector('float')()
sig_yield_err_sym = ROOT.std.vector('float')()
sig_yield_err_high =ROOT.std.vector('float')()
sig_yield_err_low = ROOT.std.vector('float')()
#------------------------Yield calcuations----------------------------------------
sig_yield.push_back(nsig.getVal()/total_entries)
sig_yield_err_sym.push_back(nsig.getError()/total_entries)
sig_yield_err_high.push_back(nsig.getAsymErrorHi()/total_entries)
sig_yield_err_low.push_back(nsig.getAsymErrorLo()/total_entries)
# --------------------------- Summary Tree -----------------------------------
summary.Branch("sig_yield", sig_yield)
summary.Branch("sig_yield_error_high", sig_yield_err_high)
summary.Branch("sig_yield_error_low", sig_yield_err_low)
summary.Branch("sig_yield_error_sym", sig_yield_err_sym)
summary.Fill()
# --------------------------- File Writing -----------------------------------
# Write the tree to the file
tree.Write()
run_tree.Write()
summary.Write()
fit_result.Write("fit_result")
fit_initial_guess_tree.Write()
# Close the ROOT file
output_file.Close()
# -------------------------- Workspace Writing-----------------------------------
w = ROOT.RooWorkspace("w", "workspace")
w.Import(model)
w.Import(data)
w.Import(run_tree)
w.Import(outputs)
w.Import(fit_result)
w.Import(timing_int)
w.writeToFile(f"{input_directory}/WSPACE_{current_time}_{origin_file_name_reduced}")
w.Print()