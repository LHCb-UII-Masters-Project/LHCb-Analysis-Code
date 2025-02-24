import ROOT
from Variables.Exp import variables, fit_initial_guess_tree
from ROOT import TH1D, TH2D, TCanvas, TChain, TTree, TString, TFile, gInterpreter, gSystem, RooMinimizer
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

#-----------------------------MODE SELECTION AND INPUTS------------------------------------
parser = argparse.ArgumentParser(description='Open multiple ROOT files and process data.')
# Accept one or more input files
parser.add_argument('input_files', type=str, nargs='+', help='Paths to the input ROOT files')
parser.add_argument('--timings', type=float, nargs='+', help='List of timings')
args = parser.parse_args()
timings = args.timings
models = []
data_sets = []
x_models = []
nbkgs = []
nsigs = []
bkgs = []
dummy_objects = []


colors = [ROOT.kBlue, ROOT.kRed, ROOT.kMagenta, ROOT.kGreen+2, ROOT.kOrange]
line_styles = [ROOT.kSolid, ROOT.kDotted, ROOT.kDashed, ROOT.kSolid, ROOT.kDashed]

# Loop through all input files and store the components
for i, file_path in enumerate(args.input_files):
    file = ROOT.TFile(file_path)
    w = file.Get("w")
    
    # Retrieve the model and components
    model = w["model"]
    data = w["data"]
    x_model = w["x"]
    run_tree = w["RunParams"]

    # Store the components in lists
    models.append(model)
    data_sets.append(data)
    x_models.append(x_model)

# Create a frame to plot the models
frame = x_models[0].frame()
upper_fit_range = x_models[0].getMax()
lower_fit_range = x_models[0].getMin()  
number_of_bins = 80
energy_range = (upper_fit_range - lower_fit_range)/number_of_bins
legend = ROOT.TLegend(0.67, 0.7, 0.97, 0.915) 
legend.SetLineColor(0)  # Remove the legend border
legend.SetLineStyle(0)  # Ensure no border line style
legend.SetLineWidth(0)  # Set line width to 0
legend.SetFillColor(0)  # Remove any fill color
legend.SetFillStyle(0)  # Ensure no fill style
legend.SetTextFont(62)  # Helvetica, normal
legend.SetTextSize(0.045)  # Adjust text size as needed 

# Inside your loop for each dataset/model pair:
for i, (model, data) in enumerate(zip(models, data_sets)):
    nEvents = data.sumEntries()  # Total number of events for each dataset
    
    # Plot the data as points
    data.plotOn(frame,
                ROOT.RooFit.Binning(number_of_bins),
                ROOT.RooFit.Name(f"data_{i}"),
                ROOT.RooFit.MarkerColor(colors[i % len(colors)]),
                ROOT.RooFit.MarkerStyle(20 + i))
    
    # Plot the model normalized to the number of events
    model.plotOn(frame,
                 ROOT.RooFit.Normalization(nEvents, ROOT.RooAbsReal.NumEvent),
                 ROOT.RooFit.Name(f"model_{i}"),
                 ROOT.RooFit.LineColor(colors[i % len(colors)]),
                 ROOT.RooFit.LineStyle(line_styles[i % len(line_styles)]))
    
    # Create a dummy object that mimics both the data and model style.
    # You can use a TGraph or a dummy TH1F. Here’s an example with TGraph:
    dummy = ROOT.TGraph()
    dummy.SetMarkerStyle(20 + i)
    dummy.SetMarkerColor(colors[i % len(colors)])
    dummy.SetLineColor(colors[i % len(colors)])
    dummy.SetLineStyle(line_styles[i % len(line_styles)])
    dummy_objects.append(dummy)
    
    # Add a single legend entry for both
    legend.AddEntry(dummy, f"{int(timings[i])} ps", "pl")

directory_path = f"/home/user294/Documents/selections/python/Fit/Comparison/Overlays/{timings}"
os.makedirs(directory_path, exist_ok=True)
with LHCbStyle() as lbs:
    c = ROOT.TCanvas("rf201_composite", "rf201_composite", 800, 600)
    latex = ROOT.TLatex() 
    latex.SetNDC() 
    latex.SetTextSize(0.050)  
    latex.SetTextFont(62)
    ROOT.gPad.SetLeftMargin(0.15)
    #ROOT.gPad.SetLogy()  # Logarithmic scale for Y-axis
    ROOT.gStyle.SetLineScalePS(1.2)
    
    # Set axis titles and label sizes
    frame.GetYaxis().SetTitle(f"Entries/ ({round(energy_range,4)} MeV/c^{{2}})")
    frame.GetXaxis().SetTitle("m(B_{s}^{0}) [GeV/c^{2}]")
    frame.GetYaxis().SetTitleOffset(0.9)
    frame.GetXaxis().SetTitleOffset(1)
    frame.GetYaxis().SetTitleFont(62)
    frame.GetXaxis().SetTitleFont(62)
    frame.GetYaxis().SetTitleSize(0.06)
    frame.GetXaxis().SetTitleSize(0.06)
    frame.GetXaxis().SetLabelSize(0.05)
    frame.GetYaxis().SetLabelSize(0.05)
    frame.GetXaxis().SetLabelFont(62)
    frame.GetYaxis().SetLabelFont(62)
    
    frame.Draw()
    legend.Draw()
    latex.DrawText(0.2,0.875,"LHCb Simulation")
    latex.DrawLatex(0.2, 0.820, "#sqrt{s} = 14 TeV") 
    c.Update()
    c.Draw()
    
    # Save the canvas to a PDF file
    c.SaveAs(f"{directory_path}test.pdf", "pdf 800")
