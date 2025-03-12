import pandas as pd
import ROOT
import ROOT
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

df= pd.read_csv('/home/user294/Documents/selections/python/Outputs/ToyPlots/RScanWide/results.csv')
#df= pd.read_csv("/home/user294/Documents/selections/python/Outputs/ToyPlots/RScan_Velo50/results.csv")

R = df['R'].values  # UpperPercentile column renamed to 'R'
lower_percentile = df['LowerPercentile'].values
n = len(R)
graph = ROOT.TGraph(n)
for i in range(n):
    graph.SetPoint(i, R[i], lower_percentile[i])  # R on X, LowerPercentile on Y

# Step 4: Create a canvas to display the plot
canvas = ROOT.TCanvas("canvas", "ROOT Plot", 900, 600)

# Set title and axis labels
graph.SetTitle("")
graph.GetXaxis().SetTitle("R")
graph.GetYaxis().SetTitle("Significance (95% CI)")

# Apply your styling settings for the plot
latex = ROOT.TLatex() 
latex.SetNDC()  # Normalized coordinates
latex.SetTextSize(0.050)  # Set text size
latex.SetTextFont(62)  # Use Helvetica font

# Set the margins (without the log scale)
ROOT.gPad.SetLeftMargin(0.15)  # Increase left margin

# Adjust the line scale for better line drawing
ROOT.gStyle.SetLineScalePS(1.2)

# Apply the font and size to axes
graph.GetYaxis().SetTitleOffset(0.9)
graph.GetXaxis().SetTitleOffset(0.6)
graph.GetYaxis().SetTitleFont(62)
graph.GetXaxis().SetTitleFont(62)
graph.GetYaxis().SetTitleSize(0.06)  # Increase title font size
graph.GetXaxis().SetTitleSize(0.06)  # Increase title font size

# Axis label styling
graph.GetXaxis().SetLabelSize(0.05)  # Label size
graph.GetYaxis().SetLabelSize(0.05)  # Label size
graph.GetXaxis().SetLabelFont(62)  # Label font
graph.GetYaxis().SetLabelFont(62)  # Label font

# Step 5: Draw the graph (points and no lines)
graph.SetMarkerStyle(21)  # Marker style (circle)
graph.SetMarkerSize(1.5)    # Marker size
graph.SetLineColor(ROOT.kRed)  # Line color (blue)
graph.SetLineWidth(2)     # Line width
graph.SetMarkerColor(ROOT.kBlue)


# Step 6: Create a customized legend (without the signal line)
legend = ROOT.TLegend(0.2, 0.45, 0.4, 0.6)  # Define legend position
legend.SetLineColor(0)  # Remove the legend border
legend.SetLineStyle(0)  # Ensure no border line style
legend.SetLineWidth(0)  # Set line width to 0 (remove lines)
legend.SetFillColor(0)  # Remove any fill color
legend.SetFillStyle(0)  # Ensure no fill style
legend.SetTextFont(62)  # Helvetica font
legend.SetTextSize(0.045)  # Legend text size

# Add entries to the legend (only for the data points)
legend.AddEntry(graph, "Data", "P")  # 'p' for points only (no line)
#legend.AddEntry(graph2,"Zoom","P")
graph.Draw("AP")         # 'A' for axis, 'P' for points only (no line)
#graph2.Draw("SAME")
# Step 7: Add text annotations (like the ones you requested)
latex.DrawLatex(0.2, 0.81, "LHCb Simulation")
latex.DrawLatex(0.2, 0.765, "#sqrt{s} = 14 TeV")

# Example of displaying timing (replace `timing_value` with your actual value)
timing_value = 50  # Replace this with your actual timing value
timing_int = int(timing_value)
latex.DrawLatex(0.2, 0.71, f"VELO {timing_int} ps")

# Step 8: Draw the legend
legend.Draw()



# Step 8: Save the plot (optional)
canvas.SaveAs("/home/user294/Documents/selections/python/Fit/CrystalBall/Significance/Figures/50psUnzoomed.pdf")
