#region IMPORTS
import ROOT
from Selections import load_event_library
load_event_library()
from ROOT import uParticle
from ROOT import TFile, gSystem, gInterpreter
from ROOT import TH1D, TH2D, TCanvas, TChain, TTree, TString, TFile
import time
from math import * 
import pandas as pd
import sys
import numpy as np
from os import path, listdir
import os
from array import array
import ctypes

import lhcbstyle
from lhcbstyle import LHCbStyle
latex = ROOT.TLatex() 
latex.SetNDC() 

import argparse
import ROOT

particle = "B"

parser = argparse.ArgumentParser(description='Open a ROOT file and process data.')
parser.add_argument('input_files',nargs="+", type=str, help='Path to the input ROOT file') 
args = parser.parse_args()

args_array = np.array(args.input_files)
histograms = []
rich_window_timings = []
velo_timings = []
pid_status = []
colours = []
line_styles = []
pid_status = []
marker_styles = []
set_colours =[ROOT.kBlue,ROOT.kRed,ROOT.kMagenta,ROOT.kBlue]
set_markers = [5,25,22,23,24,25,26,27,28]

hatch_styles = [3345,3354,3345,3354]


for index,file_name in enumerate(args.input_files):
# Open the ROOT files and get the histograms
    root_file = ROOT.TFile.Open(file_name, "READ")
    file_hist = root_file.Get(f"{particle}_Histogram")
    file_tree = root_file.Get("RunParams")
    file_tree.SetDirectory(0)
    file_hist.SetDirectory(0)
    root_file.Close()

    rich_window_timing_arr = array('f', [0])
    velo_timing_arr = array('f', [0])
    pid_kaon= array('f', [0])   
    file_tree.SetBranchAddress("rich_window_timing", rich_window_timing_arr)
    file_tree.SetBranchAddress("velo_timing", velo_timing_arr)
    file_tree.SetBranchAddress("PID_kaon", pid_kaon)

    file_tree.GetEntry(0)

    velo_timing_value = velo_timing_arr[0]
    rich_window_timing_value = rich_window_timing_arr[0]
    pid_kaon_value = pid_kaon[0]


    velo_timings.append(velo_timing_value)
    rich_window_timings.append(rich_window_timing_value)
    pid_status.append(pid_kaon_value)

    histograms.append(file_hist)
    if index == 0:
        colours.append(1)
    else:
        line_styles.append(index+1)
        marker_styles.append(index+1)


# Create a canvas to draw the histograms on
with LHCbStyle() as lbs:
    hist_canvas = ROOT.TCanvas("canvas","canvas",900,700)
    hist_canvas.cd()
    latex = ROOT.TLatex() 
    latex.SetNDC() 
    latex.SetTextSize(0.05)  

    if all(int(status) == 0 for status in pid_status):
        pid_string = "off"
        x1 = 0.66
        y1 = 0.79
        x2 = 0.86
        y2 = 0.88
    else:
        pid_string ="on"
        x1 = 0.2
        y1 = 0.8
        x2 = 0.9
        y2 = 0.9
    

    hs = ROOT.THStack("hs", "Stacked Histograms")
    legend = ROOT.TLegend(x1, y1, x2, y2) 

    for i in range(len(histograms)):
        histogram = histograms[i]
        print(histogram.GetNbinsX())
        if i>0:
            histogram.SetMarkerSize(0.5)  # Decrease marker size
            #histogram.SetFillColor(set_colours[i])
            #histogram.SetFillStyle(hatch_styles[i])  
        
        histogram.SetLineColor(set_colours[i]) 
        histogram.SetMarkerStyle(set_markers[i]) 
        histogram.SetMarkerColor(set_colours[i])

        hs.Add(histogram)
        if pid_string == "off":
            legend.AddEntry(histogram, f"VELO {int(velo_timings[i])} ps")
        if pid_string == "on":
            legend.AddEntry(histogram, f"VELO {int(velo_timings[i])}ps, RICH {int(rich_window_timings[i])}ps")

    hs.Draw("nostack L p")
    if particle == "B":
        hs.GetXaxis().SetTitle("m(B_{s}^{0}) [GeV/c^{2}]")
        hs.GetYaxis().SetTitle("Entries/ (5 MeV/c^{2})")
        hs.GetYaxis().SetTitleOffset(1.25)
    else:
        hs.GetXaxis().SetTitle("m(D_{s}^{#pm}) [GeV/c^{2}]")
        hs.GetYaxis().SetTitle("Entries/ (3 MeV/c^{2})")
        hs.GetYaxis().SetTitleOffset(1.43)
    hs.GetXaxis().SetTitleSize(0.05)
    hs.GetYaxis().SetTitleSize(0.05)
    hs.GetXaxis().SetTitleOffset(1.15)

    legend.SetLineColor(0)  # Remove the legend border
    legend.SetLineStyle(0)  # Ensure no border line style
    legend.SetLineWidth(0)  # Set line width to 0
    legend.SetFillColor(0)  # Remove any fill color
    legend.SetFillStyle(0)  # Ensure no fill style
    legend.SetTextFont(42)  # Helvetica, normal
    legend.SetTextSize(0.045)  # Adjust text size as needed

    latex.DrawLatex(0.2, 0.80, "#sqrt{s}  = 14 TeV") 
    latex.DrawText(0.2,0.855,"LHCb Simulation")

    latex2 = ROOT.TLatex() 
    latex2.SetNDC() 
    latex2.SetTextSize(0.03)  
    plot_time = time.strftime("%d %m %y", time.localtime())

    latex2.DrawLatex(0.1, 0.06, f"E.Walsh ({plot_time})")
    
    legend.Draw()

    if particle == "B":
        zoom_x1, zoom_x2 = 5.2, 5.3
        zoom_y1, zoom_y2 = 0, 40
    else:
        zoom_x1, zoom_x2 = 1.86, 1.92
        zoom_y1, zoom_y2 = 0, 400
    box = ROOT.TBox(zoom_x1, zoom_y1, zoom_x2, zoom_y2)
    box.SetLineColor(ROOT.kBlack)
    box.SetLineWidth(1)
    box.SetFillStyle(0)  # Transparent fill
    box.Draw()

    hs_zoomed = hs.Clone("hs_zoomed")

    # Define the zoom-in region relative to the histogram's axis ranges
    # Create a new pad for the zoom-in region
    pad = ROOT.TPad("pad", "Zoom-in Pad", 0.15, 0.3, 0.5, 0.6)
    pad.SetFillStyle(4000)  # Transparent pad
    pad.Draw()
    pad.cd()

    # Create a new THStack for the zoomed-in region

    # Set the axis ranges for the zoomed-in histograms
    #hs_zoomed.GetYaxis().SetRangeUser(zoom_y1, zoom_y2)

    # Draw the zoomed-in THStack
    hs_zoomed.Draw("nostack L p")
    hs_zoomed.GetXaxis().SetRangeUser(zoom_x1, zoom_x2)
    hs_zoomed.GetYaxis().SetRangeUser(zoom_y1, zoom_y2)
    hs_zoomed.GetXaxis().SetLabelSize(0)
    hs_zoomed.GetYaxis().SetLabelSize(0)
    hs_zoomed.GetXaxis().SetTickLength(0)
    hs_zoomed.GetYaxis().SetTickLength(0)
    hs_zoomed.GetXaxis().SetTitle()
    hs_zoomed.GetYaxis().SetTitle()

    # Reduce the border thickness of the pad
    pad.GetFrame().SetLineWidth(1)  # Adjust the line width as needed

    ROOT.gPad.Update()

    rich_window_timings_strings = [str(timing) for timing in rich_window_timings]
    rich_window_timings_string = "_".join(rich_window_timings_strings)

    velo_timings_strings = [str(timing) for timing in velo_timings]
    velo_timings_string = "_".join(velo_timings_strings)
    
    pid_strings = [str(status) for status in pid_status]
    pid_status_string = "_".join(pid_strings)
    
    current_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
    hist_canvas.SaveAs(f"ComparisonPlots/{particle}_VELO{velo_timings_string}RICH{rich_window_timings_string}PID{pid_status_string}_{current_time}.pdf", "pdf 800")

ascii_art = """
.%%%%%%..%%..%%...%%%%...%%..%%..........%%%%%...%%.......%%%%...%%%%%%.
.%%......%%..%%..%%..%%..%%%.%%..........%%..%%..%%......%%..%%....%%...
.%%%%....%%..%%..%%%%%%..%%.%%%..........%%%%%...%%......%%..%%....%%...
.%%......%%..%%..%%..%%..%%..%%..........%%......%%......%%..%%....%%...
.%%%%%%...%%%%...%%..%%..%%..%%..........%%......%%%%%%...%%%%.....%%...
"""
print(ascii_art)
