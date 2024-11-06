# region IMPORTS
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
# endregion IMPORTS

# region READ
root_file = ROOT.TFile.Open("/home/user294/Documents/selections/python/t=300/PID1/BsReconstructor_v1_TreeSize47000_Seed_1.962846901466769e+24_06-11-24_12:26:49.root", "READ") 
tree = root_file.Get("Tree")
tree.SetDirectory(0)
root_file.Close()
#Use RDataFrame to access the data 
rdf = ROOT.RDataFrame(tree) 
# Convert the bs_mass branch to a Numpy array
unbinned_data = rdf.AsNumpy(columns=["bs_mass"])["bs_mass"]
# endregion READ


#region DefPDF
x = ROOT.RooRealVar("x", "x", min(unbinned_data), max(unbinned_data)) # x drawn from no distribution


# Create a RooDataSet to hold the data 
data = ROOT.RooDataSet("data", "dataset with x", ROOT.RooArgSet(x)) 
for dp in unbinned_data:
    x.setVal(dp) 
    data.add(ROOT.RooArgSet(x))

mu1 = ROOT.RooRealVar("mu1", "mean of CB1", 5.36,5.3,5.4) # gaussian core mean estimate
sigma1 = ROOT.RooRealVar("sigma1","std of core gaussian 1", 0.001,0.0001,1) # gaussina core std estimate
mu2 = ROOT.RooRealVar("mu2", "mean of CB2", 5.36,5.3,5.4) # gaussian core mean estimate
sigma2 = ROOT.RooRealVar("sigma2","std of core Gaussian2", 0.001,0.0001,1) # gaussina core std estimate
alpha1 = ROOT.RooRealVar("alpha1","cut off gauss 1", 1,0.5,8) # gaussian core limit 1 estimate
alpha2 = ROOT.RooRealVar("alpha2","cut off gauss 2", 1,0.5,8) # gaussian core limit 2 estimatre
n1 = ROOT.RooRealVar("n1", "n1 of DCB", 1,0.001,50) # first power law exponent estimate
n2 = ROOT.RooRealVar("n2", "n2 of DCB", 1,0.001,50) # second power law exponent estimate

cb1 = ROOT.RooCrystalBall("cb1", "cb1", x, mu1, sigma1, alpha1, n1) #create the 1st crystal ball model
cb2 = ROOT.RooCrystalBall("cb2", "cb2",x, mu2, sigma2, alpha2, n2) # create the 2nd crystal ball model

cb1frac = ROOT.RooRealVar("frac_cb1", "fraction of CB1", 0.5, 0.0, 1.0)

sig = ROOT.RooAddPdf("sig","double crystal ball",[cb1,cb2],[cb1frac]) # combine to 1 pdf for the double crystal ball


#a0 = ROOT.RooRealVar("a0", "a0", 0, -1.2, 0.8) # first polynomial coefficient, wide range
#a1 = ROOT.RooRealVar("a1", "a1", 0, -1.2, 0.8) # second polynomial coefficient, wide range
#a2 = ROOT.RooRealVar("a2", "a2", 0.0, -1.2, 0.8)

# Define the exponential background models with coefficients for each side
AL = ROOT.RooRealVar("AL", "AL", 1, 0, 10)  # Coefficient for left side
AR = ROOT.RooRealVar("AR", "AR", 1, 0, 10)  # Coefficient for right side
aL = ROOT.RooRealVar("aL", "aL", -0.1, -1, 0)  # Left side decay constant
aR = ROOT.RooRealVar("aR", "aR", -0.1, -1, 0)  # Right side decay constant
expL = ROOT.RooFormulaVar("expL", "AL*exp(aL*x)", ROOT.RooArgList(AL, aL, x))
expR = ROOT.RooFormulaVar("expR", "AR*exp(aR*x)", ROOT.RooArgList(AR, aR, x))
bkgL = ROOT.RooExponential("bkgL", "Left Exponential Background", x, expL)
bkgR = ROOT.RooExponential("bkgR", "Right Exponential Background", x, expR)

# Combine left and right backgrounds
bkgfrac = ROOT.RooRealVar("bkgfrac", "fraction of left background", 0.5, 0.0, 1.0)
bkg = ROOT.RooAddPdf("bkg", "Combined Exponential Background", ROOT.RooArgList(bkgL, bkgR), ROOT.RooArgList(bkgfrac))


noisetosignalratio = ROOT.RooRealVar("noisetosignalratio", "fraction of noise in signal", 0.1, 0.0, 0.5)

model = ROOT.RooAddPdf("model", "Signal + Background",[bkg,sig],[noisetosignalratio])
#endregion DefPDF

# region FIT
model.fitTo(data, ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Strategy(2), ROOT.RooFit.Minimizer("Minuit2"))


frame1 = x.frame()
frame1.SetTitle("")
data.plotOn(frame1,ROOT.RooFit.Name("data"))
model.plotOn(frame1,ROOT.RooFit.Name("sig+bkg"))
model.plotOn(frame1, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineColor(ROOT.kBlack), ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.Name("bkg"))
model.plotOn(frame1, ROOT.RooFit.Components("sig"), ROOT.RooFit.LineColor(ROOT.kRed), ROOT.RooFit.LineStyle(ROOT.kDotted),ROOT.RooFit.Name("sig"))  # Overall DCB

hpull = frame1.pullHist()
frame2 = x.frame()
frame2.SetTitle("")
frame2.addPlotable(hpull, "P")

line = ROOT.TLine(frame2.GetXaxis().GetXmin(), 0, frame2.GetXaxis().GetXmax(), 0)


c = ROOT.TCanvas("rf201_composite", "rf201_composite", 1600, 600)
c.Divide(2)
c.cd(1)
ROOT.gPad.SetLogy(True)
ROOT.gPad.SetLeftMargin(0.15)
frame1.GetYaxis().SetTitleOffset(1.6)
frame1.GetYaxis().SetTitle("Number of events")
frame1.GetXaxis().SetTitle("m_{B0} [GeV]")
frame1.GetYaxis().SetTitleOffset(2.0)
frame1.Draw()

c.cd(2)
ROOT.gPad.SetLeftMargin(0.15)
frame2.GetYaxis().SetTitleOffset(1.6)
frame2.GetYaxis().SetTitle("Pulls")
frame2.GetXaxis().SetTitle("m_{B0} [GeV]")
frame2.Draw()
line.Draw("same")

c.Draw()
c.SaveAs("rf201_composite.png")



# Print structure of composite pdf
model.Print("t")
# endregion FIT






