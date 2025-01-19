# region IMPORTS
import ROOT
from Variables import *
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

mode = input("Enter the mode (calc or refit): ").strip()
parser = argparse.ArgumentParser(description='Open a ROOT file and process data.')
parser.add_argument('input_file', type=str, help='Path to the input ROOT file') 
args = parser.parse_args()
input_directory = os.path.dirname(args.input_file)

file = ROOT.TFile(args.input_file)
w = file.Get("w")
run_tree = w["RunParams"]
timing = array('f', [0])
run_tree.SetBranchAddress("velo_timing", timing)
timing_value = (timing[0])


x = w["x"]
data = w["data"]
model = w["model"]

if mode == "calc":
  sig_frac = ROOT.RooFormulaVar("sig_frac", "signal fraction", "nsig/(nbkg+nsig)", ROOT.RooArgList(w["nsig"], w["nbkg"]))
  bkg_frac = ROOT.RooFormulaVar("bkg_frac", "background fraction", "nbkg/(nbkg+nsig)", ROOT.RooArgList(w["nsig"], w["nbkg"]))
  sig_frac.Print()
  bkg_frac.Print()
  model.Print("t")


if mode == "refit":
  number_of_bins = 50
  xmin =5.2
  xmax =5.5
  range = ROOT.RooFit.Range(xmin, xmax)
  minos_params = ROOT.RooArgSet(w["x"],w["sigma1"],w["nsig"],w["nbkg"])
  fit_result = model.fitTo(data, ROOT.RooFit.PrintLevel(-1), 
                          ROOT.RooFit.Strategy(2),
                            ROOT.RooFit.Minimizer("Minuit",'migradimproved'),
                            ROOT.RooFit.Extended(True),
                            ROOT.RooFit.Save(),
                            ROOT.RooFit.Minos(minos_params),
                            ROOT.RooFit.Optimize(True),
                            ROOT.RooFit.MaxCalls(5000000),
                            range)

  frame1 = x.frame(range)
  frame1.SetTitle("")
  data.plotOn(frame1,ROOT.RooFit.Name("data"),ROOT.RooFit.Binning(number_of_bins))
  model.plotOn(frame1,ROOT.RooFit.Name("sig+bkg"), ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.LineStyle(ROOT.kSolid))
  model.plotOn(frame1, ROOT.RooFit.Components("bkg"),ROOT.RooFit.Name("bkg"), ROOT.RooFit.LineColor(ROOT.kMagenta),ROOT.RooFit.LineStyle(ROOT.kDashed))
  model.plotOn(frame1, ROOT.RooFit.Components("sig"),ROOT.RooFit.Name("sig"), ROOT.RooFit.LineColor(ROOT.kRed), ROOT.RooFit.LineStyle(ROOT.kDotted),ROOT.RooFit.LineStyle(ROOT.kDotted))  # Overall DCB

  chi2 = frame1.chiSquare("sig+bkg", "data",9)
  hpull = frame1.pullHist("data", "sig+bkg")

  frame2 = x.frame(range)
  frame2.SetTitle("")
  frame2.addPlotable(hpull, "P")

  line = ROOT.TLine(frame2.GetXaxis().GetXmin(), 0, frame2.GetXaxis().GetXmax(), 0)
  line.SetLineColor(ROOT.kBlue)

  root_file = ROOT.TFile.Open(args.input_file, "READ") 
  origin_file_path = root_file.GetName()
  origin_file_name = os.path.basename(origin_file_path)
  origin_file_name_reduced = origin_file_name.replace("WSPACE", "REFIT")
  current_time = time.strftime("%H-%M-%S_%d-%m-%Y", time.localtime())

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
      frame1.GetXaxis().SetTitle("m(B_{s}^{0}) [GeV/c^{2}]")
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
      legend.AddEntry("sig+bkg", "Total", "l")  # Solid blue line

      # Dummy lines for correct styles in the legend
      dummy_bkg_line = ROOT.TLine()
      dummy_bkg_line.SetLineColor(ROOT.kMagenta)
      dummy_bkg_line.SetLineStyle(ROOT.kDashed)
      legend.AddEntry(dummy_bkg_line, "Background", "l")  # Green dashed line

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
      frame2.GetXaxis().SetTitle("m(B_{s}^{0}) [GeV/c^{2}]")
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
      c.SaveAs(f"{input_directory}/REFIT_{current_time}_{origin_file_name_reduced}.pdf","pdf 800")

  model.Print("t")
