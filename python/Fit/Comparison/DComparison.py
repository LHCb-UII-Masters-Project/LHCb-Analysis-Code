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

import argparse
import ROOT

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



for index,file_name in enumerate(args.input_files):
# Open the ROOT files and get the histograms
    root_file = ROOT.TFile.Open(file_name, "READ")
    file_hist = root_file.Get("D_Histogram")
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
        colours.append(index+1)
    line_styles.append(index+1)
    marker_styles.append(index+1)


# Create a canvas to draw the histograms on
with LHCbStyle() as lbs:
    hist_canvas = ROOT.TCanvas("canvas","canvas",800,600)
    hist_canvas.cd()
    latex = ROOT.TLatex() 
    latex.SetNDC() 
    latex.SetTextSize(0.05)  
    legend = ROOT.TLegend(0.2, 0.8, 0.9, 0.9)


    for i in range(len(histograms)):
        histogram = histograms[i]
        draw_option = "" if i == 0 else "same"
        colour = colours[i]
        histogram.SetLineColor(colour)  # Set color for distinction
        histogram.SetStats(0) 
        histogram.SetLineStyle(line_styles[i])
        #histogram.SetMarkerStyle(20 + marker_styles[i])

        if len(histograms) <= 2:
            histogram.GetYaxis().SetRangeUser(0,histogram.GetMaximum()+300)
        elif len(histograms) >2:
            add_space = (len(histograms)-2)*150
            histogram.GetYaxis().SetRangeUser(0,histogram.GetMaximum()+300+add_space)

        histogram.SetTitle("")
        histogram.GetYaxis().SetTitle("Entries")
        histogram.GetXaxis().SetTitle("m_{D0s} [GeV/c^{2}]")
        histogram.Draw(draw_option)
        hist_canvas.Update()


        if pid_status[i] < 1:
            pid_string = "off"
        if pid_status[i] >= 1:
            pid_string ="on"
        legend.AddEntry(histogram, f"VELO {int(velo_timings[i])}ps, RICH {int(rich_window_timings[i])}ps, PID efficiency {pid_string}")

    legend.SetLineColor(0)  # Remove the legend border
    legend.SetLineStyle(0)  # Ensure no border line style
    legend.SetLineWidth(0)  # Set line width to 0
    legend.SetFillColor(0)  # Remove any fill color
    legend.SetFillStyle(0)  # Ensure no fill style
    legend.SetTextFont(42)  # Helvetica, normal

    latex.DrawLatex(0.2, 0.620, "\\sqrt{s}  = 14 TeV") 
    latex.DrawText(0.2,0.675,"LHCb Simulation")

    latex2 = ROOT.TLatex() 
    latex2.SetNDC() 
    latex2.SetTextSize(0.03)  
    plot_time = time.strftime("%d %m %y", time.localtime())

    latex2.DrawLatex(0.1, 0.09, f"J.McQueen({plot_time})")

    
    legend.Draw()

    rich_window_timings_strings = [str(timing) for timing in rich_window_timings]
    rich_window_timings_string = "_".join(rich_window_timings_strings)

    velo_timings_strings = [str(timing) for timing in velo_timings]
    velo_timings_string = "_".join(velo_timings_strings)
    
    pid_strings = [str(status) for status in pid_status]
    pid_status_string = "_".join(pid_strings)
    
    current_time = time.strftime("%Y-%m-%d_%H", time.localtime())
    hist_canvas.SaveAs(f"ComparisonPlots/D_VELO{velo_timings_string}RICH{rich_window_timings_string}PID{pid_status_string}_{current_time}.png")

ascii_art = """
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    ___  ________  ________  ___  __    ________  ___       ________  _________   @
@   |\  \|\   __  \|\   ____\|\  \|\  \ |\   __  \|\  \     |\   __  \|\___   ___\ @
@   \ \  \ \  \|\  \ \  \___|\ \  \/  /|\ \  \|\  \ \  \    \ \  \|\  \|___ \  \_| @
@ __ \ \  \ \   __  \ \  \    \ \   ___  \ \   ____\ \  \    \ \  \\\  \   \ \  \  @
@|\  \\_\  \ \  \ \  \ \  \____\ \  \\ \  \ \  \___|\ \  \____\ \  \\\  \   \ \  \ @
@\ \________\ \__\ \__\ \_______\ \__\\ \__\ \__\    \ \_______\ \_______\   \ \__\@
@ \|________|\|__|\|__|\|_______|\|__| \|__|\|__|     \|_______|\|_______|    \|__|@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
print(ascii_art)
