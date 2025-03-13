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

def fill_graph (df, colour, marker_style):
    R = df['R'].values  # UpperPercentile column renamed to 'R'
    lower_percentile = df['LowerPercentile'].values
    yerr = df['StandardError'].values
    n = len(R)
    graph = ROOT.TGraphErrors(n)
    for i in range(n):
        graph.SetPoint(i, R[i], lower_percentile[i])  # R on X, LowerPercentile on Y
        graph.SetPointError(i, 0, yerr[i])  # Set the error in the y direction (x-error is 0)

    # Set title and axis labels
    graph.SetTitle("")
    graph.GetXaxis().SetTitle("R")
    graph.GetYaxis().SetTitle("Significance (95% CI)")
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
    graph.SetMarkerStyle(marker_style)  # Marker style (circle)
    graph.SetMarkerSize(1.1)    # Marker size
    graph.SetLineColor(colour)  # Line color (blue)
    graph.SetLineWidth(2)     # Line width
    graph.SetMarkerColor(colour)
    return graph

df30 = pd.read_csv('/home/user294/Documents/selections/python/Outputs/ToyPlots/RScan_Velo30/results.csv')
df50 = pd.read_csv('/home/user294/Documents/selections/python/Outputs/ToyPlots/RScan_Velo50/results.csv')
df70= pd.read_csv('/home/user294/Documents/selections/python/Outputs/ToyPlots/RScan_Velo70/results.csv')
df100= pd.read_csv('/home/user294/Documents/selections/python/Outputs/ToyPlots/RScan_Velo100/results.csv')

graph30 = fill_graph(df30,ROOT.kRed,21)
graph50 = fill_graph(df50,ROOT.kBlue,20)
graph70 = fill_graph(df70, ROOT.kGreen,23)
graph100 = fill_graph(df100, ROOT.kMagenta,33)


canvas = ROOT.TCanvas("canvas", "ROOT Plot", 900, 600)


# Apply your styling settings for the plot
latex = ROOT.TLatex() 
latex.SetNDC()  # Normalized coordinates
latex.SetTextSize(0.050)  # Set text size
latex.SetTextFont(62)  # Use Helvetica font

# Set the margins (without the log scale)
ROOT.gPad.SetLeftMargin(0.15)  # Increase left margin

# Adjust the line scale for better line drawing
ROOT.gStyle.SetLineScalePS(1.2)



# Step 6: Create a customized legend (without the signal line)
legend = ROOT.TLegend(0.2, 0.35, 0.5, 0.7)  # Define legend position
legend.SetLineColor(0)  # Remove the legend border
legend.SetLineStyle(0)  # Ensure no border line style
legend.SetLineWidth(0)  # Set line width to 0 (remove lines)
legend.SetFillColor(0)  # Remove any fill color
legend.SetFillStyle(0)  # Ensure no fill style
legend.SetTextFont(62)  # Helvetica font
legend.SetTextSize(0.045)  # Legend text size

legend.AddEntry(graph30, "30 ps", "P")  # 'p' for points only (no line)
legend.AddEntry(graph50, "50 ps", "P")  # 'p' for points only (no line)
legend.AddEntry(graph70, "70 ps", "P")  # 'p' for points only (no line)
legend.AddEntry(graph100, "100 ps", "P")  # 'p' for points only (no line)
graph30.SetMinimum(1.2)  # Extend lower bound
graph30.SetMaximum(8)  # Extend upper bound
graph30.Draw("APE")         # 'A' for axis, 'P' for points only (no line)
graph50.Draw("PE SAME")
graph70.Draw("PE SAME")
graph100.Draw("PE SAME")


latex.DrawLatex(0.2, 0.81, "LHCb Simulation")
latex.DrawLatex(0.2, 0.765, "#sqrt{s} = 14 TeV")

# Step 8: Draw the legend
legend.Draw()



# Step 8: Save the plot (optional)
canvas.SaveAs("/home/user294/Documents/selections/python/Fit/CrystalBall/Significance/Figures/AllTimings.pdf")

