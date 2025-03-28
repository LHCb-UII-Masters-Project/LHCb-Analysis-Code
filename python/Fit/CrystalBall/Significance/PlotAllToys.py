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
latex = ROOT.TLatex() 

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
    graph.GetYaxis().SetTitle("Significance (90% CL)")
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
    graph.SetMarkerSize(1.5)    # Marker size
    graph.SetLineColor(colour)  # Line color (blue)
    graph.SetLineWidth(2)     # Line width
    graph.SetMarkerColor(colour)
    return graph

suppression = "Signal"

df30 = pd.read_csv(f'/home/user293/Documents/selections/python/Outputs/ToyPlots/RScan_Velo30Sup{suppression}_95/results.csv')
df50 = pd.read_csv(f'/home/user293/Documents/selections/python/Outputs/ToyPlots/RScan_Velo50Sup{suppression}_95/results.csv')
df70= pd.read_csv(f'/home/user293/Documents/selections/python/Outputs/ToyPlots/RScan_Velo70Sup{suppression}_95/results.csv')
df100= pd.read_csv(f'/home/user293/Documents/selections/python/Outputs/ToyPlots/RScan_Velo100Sup{suppression}_95/results.csv')
df200= pd.read_csv(f'/home/user293/Documents/selections/python/Outputs/ToyPlots/RScan_Velo200Sup{suppression}_95/results.csv')

graph30 = fill_graph(df30,ROOT.kRed,21)
graph50 = fill_graph(df50,ROOT.kBlue,20)
graph70 = fill_graph(df70, ROOT.kGreen,23)
graph100 = fill_graph(df100, ROOT.kMagenta,33)
graph200 = fill_graph(df200, ROOT.kOrange,34)

line_3sigma = ROOT.TLine(graph30.GetXaxis().GetXmin(), 3, graph30.GetXaxis().GetXmax(), 3)
line_5sigma = ROOT.TLine(graph30.GetXaxis().GetXmin(), 5, graph30.GetXaxis().GetXmax(), 5)

for line in [line_3sigma, line_5sigma]:
    line.SetLineColor(ROOT.kAzure -6)
    line.SetLineStyle(2)
    line.SetLineWidth(3)




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
legend = ROOT.TLegend(0.16, 0.36, 0.55, 0.75)  # Define legend position
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
#legend.AddEntry(graph200, "200 ps", "PE")
graph30.SetMinimum(0)  # Extend lower bound
graph30.SetMaximum(12)  # Extend upper bound
graph30.Draw("APL")         # 'A' for axis, 'P' for points only (no line)
line_3sigma.Draw("SAME")
line_5sigma.Draw("SAME")
graph50.Draw("PL SAME")
graph70.Draw("PL SAME")
graph100.Draw("PL SAME")
#graph200.Draw("PL SAME")


latex.DrawLatex(0.2, 0.81, "LHCb Simulation")
latex.DrawLatex(0.2, 0.765, "#sqrt{s} = 14 TeV")

# Add labels for 3sigma and 5sigma
latex.SetTextColor(ROOT.kAzure -6)
latex.DrawLatex(0.91, 0.29, "3#sigma")  
latex.DrawLatex(0.91, 0.46, "5#sigma")


# Step 8: Draw the legend
legend.Draw()


# Step 8: Save the plot (optional)
#canvas.SaveAs("/home/user293/Documents/selections/python/Fit/CrystalBall/Significance/Figures/NewFinAllTimingslines" + suppression + "_95.pdf")

from scipy.interpolate import make_interp_spline

def interpolate_R_for_sigma(df, sigma_values=[3, 5]):
    """Interpolate the R-values corresponding to given significance levels."""
    R_values = df['R'].values[::-1]
    Sigs = df['LowerPercentile'].values[::-1]  # Assuming significance values are stored here
    
    if len(R_values) < 3:  # Ensure we have enough points for quadratic interpolation
        print("Not enough data points for quadratic interpolation.")
        return {sigma: None for sigma in sigma_values}

    # Create the interpolation function
    spl_inverted = make_interp_spline(Sigs, R_values, k=2)

    # Interpolate R for each significance value
    interpolated_R = {sigma: float(spl_inverted(sigma)) for sigma in sigma_values}
    return interpolated_R

# Compute interpolated R-values for each timing resolution
interpolated_results = {
    "30 ps": interpolate_R_for_sigma(df30),
    "50 ps": interpolate_R_for_sigma(df50),
    "70 ps": interpolate_R_for_sigma(df70),
    "100 ps": interpolate_R_for_sigma(df100),
}

# Print results
for timing, values in interpolated_results.items():
    print(f"{timing}: R(3σ) = {values[3]:.2f}, R(5σ) = {values[5]:.2f}")
