#---------------------------------Imports------------------------------------------
import ROOT
from Variables.CrystallBall import variables, fit_initial_guess_tree
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
#--------------------------------File Inputs---------------------------------------
parser = argparse.ArgumentParser(description='Open a ROOT file and process data.')
parser.add_argument('input_file', type=str, help='Path to the input ROOT file') 
parser.add_argument("particle", type=str, help="Provide the particle for fitting")
parser.add_argument("fit_range", type=str, help="sigma for fit range")
args = parser.parse_args()
input_directory = os.path.dirname(args.input_file)

args = parser.parse_args()
input_directory = os.path.dirname(args.input_file)
if args.particle == "xiccpp":
    particle_mass = 3.622
    x_label = "m(#Xi_{cc}^{++}) [MeV/c^{2}]"
if args.particle == "lambdac":
    particle_mass = 2.287
    x_label = "m(#Lambda_{c}^{+}) [MeV/c^{2}]"
if args.particle == "xiccp":
    particle_mass = 3.5189
    x_label = "m(#Xi_{cc}^{+}) [MeV/c^{2}]"
#-------------------------------Tree Reading---------------------------------------
root_file = ROOT.TFile.Open(args.input_file, "READ") 
run_tree = root_file.Get("RunParams")
outputs = root_file.Get("Outputs")
diagnostics = root_file.Get("RunDiagnostics")
diagnostics.SetDirectory(0)
run_tree.SetDirectory(0)
outputs.SetDirectory(0)
root_file.Close()
#Use RDataFrame to access the data 
rdf = ROOT.RDataFrame(diagnostics) 
if args.particle == "xiccpp":
    df = rdf.AsNumpy()["xiccpp_is_signal_mass_post_selections"]*0.001
elif args.particle == "lambdac":
    df = rdf.AsNumpy()["lambdac_is_signal_mass_post_selections"]*0.001
if args.particle == "xiccp":
    df = rdf.AsNumpy()["xiccpp_is_signal_mass_post_selections"]*0.001
lower_fit_range = particle_mass - float(args.fit_range)*(variables['sigma']['value'])
upper_fit_range = particle_mass + float(args.fit_range)*(variables['sigma']['value'])
unbinned_data = df[(df > lower_fit_range) & (df < upper_fit_range)]
# Convert the bs_mass branch to a Numpy array
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
# --------------------------- Variables and PDF Declerations -----------
mu = ROOT.RooRealVar("mu1", "mean of CB1", variables['mu']['value'], variables['mu']['min'], variables['mu']['max'])  # Gaussian core mean estimate
sigma = ROOT.RooRealVar("sigma1", "std of core gaussian 1", variables['sigma']['value'], variables['sigma']['min'], variables['sigma']['max'])  # Gaussian core std estimate
alphaL = ROOT.RooRealVar("alphaL", "cut off gauss left", variables['alphaL']['value'], variables['alphaL']['min'], variables['alphaL']['max'])  # Gaussian core limit 1 estimate
alphaR = ROOT.RooRealVar("alphaR", "cut off gauss right", variables['alphaR']['value'], variables['alphaR']['min'], variables['alphaR']['max'])  # Gaussian core limit 2 estimate
nL = ROOT.RooRealVar("n1", "nleft of DCB", variables['nL']['value'], variables['nL']['min'], variables['nL']['max'])  # First power law exponent estimate
nR = ROOT.RooRealVar("n2", "nright of DCB", variables['nR']['value'], variables['nR']['min'], variables['nR']['max'])  # Second power law exponent estimate
sig = ROOT.RooCrystalBall("sig", "double crystal ball", x, mu, sigma, alphaL, nL, alphaR, nR)
#-------------------------------------PDF Fitting-------------------------------------------------------------
minos_params = ROOT.RooArgSet(mu,sigma,alphaL,alphaR,nL,nR)
fit_result = sig.fitTo(data, ROOT.RooFit.PrintLevel(-1), 
                         ROOT.RooFit.Strategy(2),
                           ROOT.RooFit.Minimizer("Minuit",'migradimproved'),
                           ROOT.RooFit.Save(),
                           ROOT.RooFit.Minos(minos_params),
                           ROOT.RooFit.Optimize(True),
                           ROOT.RooFit.MaxCalls(5000000))
# --------------------------- Plotting Initialisation -----------------------------------
number_of_bins = 20
energy_range = (upper_fit_range - lower_fit_range)/number_of_bins
frame1 = x.frame()
frame1.SetTitle("")
data.plotOn(frame1,ROOT.RooFit.Name("data"),ROOT.RooFit.Binning(number_of_bins), ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
sig.plotOn(frame1,ROOT.RooFit.Name("sig"), ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.LineStyle(ROOT.kSolid))
chi2 = frame1.chiSquare("sig", "data",7)
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
os.makedirs(f"{input_directory}/{current_time}_{origin_file_name_reduced}", exist_ok=True)
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
    frame1.GetYaxis().SetTitle(f"Entries/ ({round(energy_range,4)} MeV/c^{{2}})")
    frame1.GetXaxis().SetTitle(x_label)
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
    legend.AddEntry("sig", "DCB", "l")  # Solid blue line
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
    frame2.GetXaxis().SetTitle(x_label)
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
    c.SaveAs(f"{input_directory}/{current_time}_{origin_file_name_reduced}/FitT.pdf","pdf 800")


output_file = ROOT.TFile(f"{input_directory}/{current_time}_{origin_file_name_reduced}/FitT.root", "RECREATE")
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
alphaL_val = ROOT.std.vector('float')()
alphaL_err_sym = ROOT.std.vector('float')()
alphaR_val = ROOT.std.vector('float')()
alphaR_err_sym = ROOT.std.vector('float')()
nL_val = ROOT.std.vector('float')()
nL_err_sym = ROOT.std.vector('float')()
nR_val = ROOT.std.vector('float')()
nR_err_sym = ROOT.std.vector('float')()
chi2_val = ROOT.std.vector('float')()
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
alphaL_val.push_back(alphaL.getVal())
alphaL_err_sym.push_back(alphaL.getError())
alphaR_val.push_back(alphaR.getVal())
alphaR_err_sym.push_back(alphaR.getError())
nL_val.push_back(nL.getVal())
nL_err_sym.push_back(nL.getError())
nR_val.push_back(nR.getVal())
nR_err_sym.push_back(nR.getError())
chi2_val.push_back(chi2)
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
tree.Branch("alphaL", alphaL_val)
tree.Branch("alphaL_error_sym", alphaL_err_sym)
tree.Branch("alphaR", alphaR_val)
tree.Branch("alphaR_error_sym", alphaR_err_sym)
tree.Branch("nL", nL_val)
tree.Branch("nL_error_sym", nL_err_sym)
tree.Branch("nR", nR_val)
tree.Branch("nR_error_sym", nR_err_sym)
tree.Branch("timing", timing_val)
tree.Branch("pid_kaon_flag", pid_kaon_flag)
tree.Branch("pid_pion_flag", pid_pion_flag)
tree.Fill()
#--------------------------- Summary Vectors -----------------------------------
# --------------------------- File Writing -----------------------------------
# Write the tree to the file
tree.Write()
run_tree.Write()
fit_result.Write("fit_result")
fit_initial_guess_tree.Write()
# Close the ROOT file
output_file.Close()
# -------------------------- Workspace Writing-----------------------------------
w = ROOT.RooWorkspace("w", "workspace")
w.Import(sig)
w.Import(data)
w.Import(run_tree)
w.Import(outputs)
w.Import(fit_result)
w.Import(timing_int)
w.writeToFile(f"{input_directory}/{current_time}_{origin_file_name_reduced}/WSPACE")
w.Print()