# region IMPORTS
import ROOT
from ROOT import TH1D, TH2D, TCanvas, TChain, TTree, TString, TFile,gInterpreter,gSystem
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

# TO DO: SIGNAL + BCKG - BCKG PLOT AND YIELD!
parser = argparse.ArgumentParser(description='Open a ROOT file and process data.')
parser.add_argument('input_file', type=str, help='Path to the input ROOT file') 
args = parser.parse_args()

class LHCbStyle:
    def __init__(self, print_msg=False):
        """
        Load the macro if not already loaded.
        Provide easy access to the pointers declared in the LHCbStyle namespace.
        """
        self._print_msg = print_msg
        if not hasattr(self._ROOT, "lhcbStyle"):
            with importlib.resources.path("lhcbstyle", "lhcbStyle.C") as path:
                self._ROOT.gROOT.LoadMacro(str(path))
        self.lhcbStyle = self._ROOT.LHCbStyle.lhcbStyle
        self.create_label = self._ROOT.LHCbStyle.create_label
        self.lhcbLabel = self._ROOT.LHCbStyle.lhcbLabel
        self.lhcbLatex = self._ROOT.LHCbStyle.lhcbLatex

    def __enter__(self):
        """
        For context management, store the original global style so it can be reset later
        """
        self.old_style = self._ROOT.gStyle.GetName()
        self.apply()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Return the global style to its original state
        """
        self._ROOT.gROOT.SetStyle(self.old_style)

    def apply(self):
        """
        Execute the main function of the macro, which sets the global style to LHCbStyle
        """
        self._ROOT.lhcbStyle(self._print_msg)

    @property
    def _ROOT(self):
        """
        Property to avoid importing ROOT until absolutely necessary
        """
        import ROOT

        return ROOT


# endregion IMPORTS

# region READ
root_file = ROOT.TFile.Open(args.input_file, "READ") 
tree = root_file.Get("Tree")
tree.SetDirectory(0)
root_file.Close()
#Use RDataFrame to access the data 
rdf = ROOT.RDataFrame(tree) 
# Convert the bs_mass branch to a Numpy array
unbinned_data = rdf.AsNumpy(columns=["bs_mass"])["bs_mass"]


# Create a variable to hold the value
timing = array('f', [0])
PID_pion = array('f', [0])
PID_kaon= array('f', [0])

# Set branch address
tree.SetBranchAddress("timing_res", timing)
tree.SetBranchAddress("PID_pion", PID_pion)
tree.SetBranchAddress("PID_kaon", PID_kaon)
tree.GetEntry(0)


timing_value = (timing[0])
PID_pion_value = (PID_pion[0])
PID_kaon_value = (PID_kaon[0])
# endregion READ


#region DefPDF
# Define the variable x
x = ROOT.RooRealVar("x", "x", min(unbinned_data), max(unbinned_data))

rice_bins = int(np.ceil(2 * np.cbrt(len(unbinned_data))))

# Create a histogram to bin the data
hist = ROOT.TH1F("hist", "histogram", rice_bins, min(unbinned_data), max(unbinned_data))
for dp in unbinned_data:
    hist.Fill(dp)

# Filter the data to exclude bins with fewer than 10 entries
filtered_data = []
for dp in unbinned_data:
    bin_index = hist.FindBin(dp)
    if hist.GetBinContent(bin_index) >= 10:
        filtered_data.append(dp)

# Convert the filtered data to a RooDataSet
data = ROOT.RooDataSet("data", "dataset with x", ROOT.RooArgSet(x))
for dp in unbinned_data: # change to filtered data for filtering
    x.setVal(dp)
    data.add(ROOT.RooArgSet(x))


mu = ROOT.RooRealVar("mu1", "mean of CB1", 5.40,5.20,5.50) # gaussian core mean estimate
sigma = ROOT.RooRealVar("sigma1","std of core gaussian 1", 0.001,0.0001,2) # gaussina core std estimate
alphaL = ROOT.RooRealVar("alphaL","cut off gauss left", 1,0.5,8) # gaussian core limit 1 estimate
alphaR = ROOT.RooRealVar("alphaR","cut off gauss right", 1,0.5,8) # gaussian core limit 2 estimatre
nL = ROOT.RooRealVar("n1", "nleft of DCB", 1,0.001,10) # first power law exponent estimate
nR = ROOT.RooRealVar("n2", "nright of DCB", 1,0.001,3) # second power law exponent estimate

sig = ROOT.RooCrystalBall("sig", "double crystal ball",x,mu,sigma,alphaL,nL,alphaR,nR)

decay_constant = ROOT.RooRealVar("decay_constant", "decay_constant", -0.001, -5, 0)
bkg = ROOT.RooExponential("bkg", "Exponential Background", x, decay_constant)

noisetosignalratio = ROOT.RooRealVar("noisetosignalratio", "fraction of noise in signal", 0.1, 0.0, 0.5)

model = ROOT.RooAddPdf("model", "Signal + Background",ROOT.RooArgSet(bkg,sig),ROOT.RooArgSet(noisetosignalratio))
#endregion DefPDF

# region FIT
fit_result = model.fitTo(data, ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Strategy(2), ROOT.RooFit.Minimizer("Minuit2"),ROOT.RooFit.Save())

number_of_bins = 50
frame1 = x.frame()
frame1.SetTitle("")
data.plotOn(frame1,ROOT.RooFit.Name("data"),ROOT.RooFit.Binning(number_of_bins))
model.plotOn(frame1,ROOT.RooFit.Name("sig+bkg"), ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.LineStyle(ROOT.kSolid))
model.plotOn(frame1, ROOT.RooFit.Components("bkg"),ROOT.RooFit.Name("bkg"), ROOT.RooFit.LineColor(ROOT.kGreen),ROOT.RooFit.LineStyle(ROOT.kDashed))
model.plotOn(frame1, ROOT.RooFit.Components("sig"),ROOT.RooFit.Name("sig"), ROOT.RooFit.LineColor(ROOT.kRed), ROOT.RooFit.LineStyle(ROOT.kDotted))  # Overall DCB

# Reduce the dataset to the specified signal range without redefining x


chi2 = frame1.chiSquare("sig+bkg", "data",8)
hpull = frame1.pullHist("data", "sig+bkg")

frame2 = x.frame()
frame2.SetTitle("")
frame2.addPlotable(hpull, "P")

line = ROOT.TLine(frame2.GetXaxis().GetXmin(), 0, frame2.GetXaxis().GetXmax(), 0)
line.SetLineColor(ROOT.kBlue)

origin_file_path = root_file.GetName()
origin_file_name = os.path.basename(origin_file_path)
origin_file_name_reduced = origin_file_name.replace(".root", "")
current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

with LHCbStyle() as lbs:
    c = ROOT.TCanvas("rf201_composite", "rf201_composite", 1600, 600)
    c.Divide(2)

    # First pad
    c.cd(1)
    latex = ROOT.TLatex() 
    latex.SetNDC() 
    latex.SetTextSize(0.05)     
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetLogy() # Turn on logarithmic scale for Y-axis
    frame1.GetYaxis().SetTitle("Entries")
    frame1.GetXaxis().SetTitle("m_{B0} [GeV/c^{2}]")
    frame1.GetYaxis().SetTitleOffset(1)
    frame1.GetXaxis().SetTitleOffset(1)

    frame1.GetYaxis().SetTitleSize(0.05) # Increase this value to make the font size larger
    frame1.GetXaxis().SetTitleSize(0.05) # Increase this value to make the font size larger
    frame1.Draw()

    # Add the legend with LaTeX formatting, without a legend box, and matching LaTeX font
    legend = ROOT.TLegend(0.175, 0.6, 0.5, 0.80)
    legend.SetLineColor(0)  # Remove the legend border
    legend.SetLineStyle(0)  # Ensure no border line style
    legend.SetLineWidth(0)  # Set line width to 0
    legend.SetFillColor(0)  # Remove any fill color
    legend.SetFillStyle(0)  # Ensure no fill style
    legend.SetTextFont(42)  # Helvetica, normal
    legend.SetTextSize(0.03)  # Adjust text size as needed


    legend.AddEntry("data", "Data", "lep")  # Points with error bars
    legend.AddEntry("sig+bkg", "Total", "l")  # Solid blue line

    # Dummy lines for correct styles in the legend
    dummy_bkg_line = ROOT.TLine()
    dummy_bkg_line.SetLineColor(ROOT.kGreen)
    dummy_bkg_line.SetLineStyle(ROOT.kDashed)
    legend.AddEntry(dummy_bkg_line, "Background", "l")  # Green dashed line

    dummy_sig_line = ROOT.TLine()
    dummy_sig_line.SetLineColor(ROOT.kRed)
    dummy_sig_line.SetLineStyle(ROOT.kDotted)
    legend.AddEntry(dummy_sig_line, "DCB", "l")  # Red dotted line

    latex.DrawText(0.2,0.875,"LHCb Simulation")
    latex.DrawLatex(0.2, 0.825, "%d \\mu s" % timing_value) 



    legend.Draw()

    c.cd(2)
    ROOT.gPad.SetLeftMargin(0.15)
    frame2.GetYaxis().SetTitle("Pulls")
    frame2.GetXaxis().SetTitle("m_{B0} [GeV/c^{2}]")
    frame2.GetYaxis().SetTitleOffset(1)
    frame2.GetXaxis().SetTitleOffset(1)
    frame2.GetYaxis().SetTitleSize(0.05) # Increase this value to make the font size larger
    frame2.GetXaxis().SetTitleSize(0.05) # Increase this value to make the font size larger
    frame2.Draw()
    line.Draw("same")

    current_date = datetime.now().strftime("%d/%m/%y")

    latex.DrawText(0.2,0.875,f"JM {current_date}")

    
    c.cd()
    c.Update()
    c.Draw()
    c.SaveAs(f"FitOutputs/{origin_file_name_reduced}_fitted_{current_time}.png")
    # Create a ROOT file

output_file = ROOT.TFile(f"FitOutputs/{origin_file_name_reduced}_fitted_{current_time}.root", "RECREATE")

# Write the canvas to the file
c.Write()

# Create a tree to store the fit parameters and their errors
tree = ROOT.TTree("fit_parameters", "Fit Parameters Tree")

# Create variables to hold the parameters and their errors
mean_val = ROOT.std.vector('float')()
mean_err = ROOT.std.vector('float')()
sigma_val = ROOT.std.vector('float')()
sigma_err = ROOT.std.vector('float')()
alphaL_val = ROOT.std.vector('float')()
alphaL_err = ROOT.std.vector('float')()
alphaR_val = ROOT.std.vector('float')()
alphaR_err = ROOT.std.vector('float')()
nL_val = ROOT.std.vector('float')()
nL_err = ROOT.std.vector('float')()
nR_val = ROOT.std.vector('float')()
nR_err = ROOT.std.vector('float')()
decay_constant_val = ROOT.std.vector('float')()
decay_constant_err = ROOT.std.vector('float')()
chi2_val = ROOT.std.vector('float')()

mean_val.push_back(mu.getVal())
mean_err.push_back(mu.getError())
sigma_val.push_back(sigma.getVal())
sigma_err.push_back(sigma.getError())
alphaL_val.push_back(alphaL.getVal())
alphaL_err.push_back(alphaL.getError())
alphaR_val.push_back(alphaR.getVal())
alphaR_err.push_back(alphaR.getError())
nL_val.push_back(nL.getVal())
nL_err.push_back(nL.getError())
nR_val.push_back(nR.getVal())
nR_err.push_back(nR.getError())
decay_constant_val.push_back(decay_constant.getVal())
decay_constant_err.push_back(decay_constant.getError())
chi2_val.push_back(chi2)

# Create branches in the tree
tree.Branch("mean", mean_val)
tree.Branch("mean_error", mean_err)
tree.Branch("sigma", sigma_val)
tree.Branch("sigma_error", sigma_err)
tree.Branch("alphaL", alphaL_val)
tree.Branch("alphaL_error", alphaL_err)
tree.Branch("alphaR", alphaR_val)
tree.Branch("alphaR_error", alphaR_err)
tree.Branch("nL", nL_val)
tree.Branch("nL_error", nL_err)
tree.Branch("nR", nR_val)
tree.Branch("nR_error", nR_err)
tree.Branch("decay_constant", decay_constant_val)
tree.Branch("decay_constant_error", decay_constant_err)
tree.Branch("chi2", chi2_val)


# Fill the tree with values
tree.Fill()

# Write the tree to the file
tree.Write()

# Close the ROOT file
output_file.Close()

ascii_art = """
 ___  ________  ________  ___  __    ________ ___  _________   
   |\  \|\   __  \|\   ____\|\  \|\  \ |\  _____\\  \|\___   ___\ 
   \ \  \ \  \|\  \ \  \___|\ \  \/  /|\ \  \__/\ \  \|___ \  \_| 
 __ \ \  \ \   __  \ \  \    \ \   ___  \ \   __\\ \  \   \ \  \  
|\  \\_\  \ \  \ \  \ \  \____\ \  \\ \  \ \  \_| \ \  \   \ \  \ 
\ \________\ \__\ \__\ \_______\ \__\\ \__\ \__\   \ \__\   \ \__\
 \|________|\|__|\|__|\|_______|\|__| \|__|\|__|    \|__|    \|__|

"""

print(ascii_art)








