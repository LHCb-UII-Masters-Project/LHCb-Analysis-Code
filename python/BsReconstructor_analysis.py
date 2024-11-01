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

hist_file = ROOT.TFile.Open("t=300/PID1/BsReconstructor_v1_TreeSize2000_Seed_1.566617118163761e+24_01-11-24_14:13:14.root", "READ") 
data_hist = hist_file.Get("B_Histogram")
data_hist.SetDirectory(0)
hist_file.Close()

hist_canvas = ROOT.TCanvas("canvas")
hist_canvas.cd()
hist_canvas.SetLogy(True)

data_hist.SetLineWidth(1)
data_hist.SetStats(0) 
data_hist.SetLineColor(ROOT.kBlack)
data_hist.GetYaxis().SetTitle("Number of events")
data_hist.GetXaxis().SetTitle("m_{B0} [GeV]")


gaussFit = ROOT.TF1("gaussfit","gaus",5.20,5.60) # to fit a gaussian
data_hist.Fit(gaussFit ,"E")


# Create a new histogram to hold the fit values
fit_hist = data_hist.Clone("fit_hist")
fit_hist.Reset()

# Fill the new histogram with fit values
for i in range(1, fit_hist.GetNbinsX() + 1):
    x = fit_hist.GetBinCenter(i)
    fit_value = gaussFit.Eval(x)
    fit_hist.SetBinContent(i, fit_value)
    fit_hist.SetBinError(i, 0)  # No error bars for fit histogram

fit_hist.Divide(data_hist)
fit_hist.SetLineColor(ROOT.kRed)
hist_canvas.Clear()

pad1 = ROOT.TPad("pad1","pad1",0,0.3,1,1) 
pad1.SetLogy(True)
pad1.Draw()
pad1.cd()

data_hist.Draw("p") 
latex = ROOT.TLatex() 
latex.SetNDC() 
latex.SetTextSize(0.03)

chi2 = gaussFit.GetChisquare()
ndof = gaussFit.GetNDF()
mean = gaussFit.GetParameter(1)
width = gaussFit.GetParameter(2)

latex.DrawText(0.2,0.85,"Mean = %.3f GeV"%(mean)) 
latex.DrawText(0.2,0.80,"Width = %.3f GeV"%(width)) 
latex.DrawText(0.2,0.75,"chi2/ndof = %.1f/%d = %.1f"%(chi2,ndof,chi2/ndof))

latex.SetTextSize(0.06) 
latex.DrawText(0.7,0.83,"LHCb 2024") 
latex.SetTextSize(0.04) 
latex.DrawText(0.7,0.77,"B0 events")

legend = ROOT.TLegend(0.7,0.6,0.85,0.75) 
legend.AddEntry(data_hist ,"Data") 
legend.AddEntry(fit_hist ,"Fit") 
legend.SetLineWidth(0) 
legend.Draw("same")

hist_canvas.cd()
pad2 = ROOT.TPad("pad2","pad2",0,0.05,1,0.3) 
pad2.Draw()

pad1.SetBottomMargin(0)
pad2.SetTopMargin(0) 
pad2.SetBottomMargin(0.25)
data_hist.SetTitle("") 
data_hist.GetXaxis().SetLabelSize(0) 
data_hist.GetXaxis().SetTitleSize(0)
data_hist.GetYaxis().SetTitleSize(0.05)

fit_hist.SetTitle("")
fit_hist.GetXaxis().SetLabelSize(0.12) 
fit_hist.GetXaxis().SetTitleSize(0.12) 
fit_hist.GetYaxis().SetLabelSize(0.1) 
fit_hist.GetYaxis().SetTitleSize(0.15) 
fit_hist.GetYaxis().SetTitle("Data/Fit") 
fit_hist.GetYaxis().SetTitleOffset(0.3)
fit_hist.GetYaxis().SetRangeUser(0.5,1.5)
fit_hist.GetYaxis().SetNdivisions(207)

pad2.cd()
fit_hist.Draw("pt")

line = ROOT.TLine(fit_hist.GetXaxis().GetXmin(),1,fit_hist.GetXaxis().GetXmax(),1) 
line.SetLineColor(ROOT.kBlack)
line.SetLineWidth(1) 
line.Draw("same")


hist_canvas.Print("test.pdf")

  