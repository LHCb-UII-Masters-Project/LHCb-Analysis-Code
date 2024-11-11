# region IMPORTS
import ROOT
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
sigma = ROOT.RooRealVar("sigma1","std of core gaussian 1", 0.015,0.001,1) # gaussina core std estimate
alphaL = ROOT.RooRealVar("alphaL","cut off gauss left", 1,0.5,8) # gaussian core limit 1 estimate
alphaR = ROOT.RooRealVar("alphaR","cut off gauss right", 1,0.5,8) # gaussian core limit 2 estimatre
nL = ROOT.RooRealVar("n1", "nleft of DCB", 1,0.001,10) # first power law exponent estimate
nR = ROOT.RooRealVar("n2", "nright of DCB", 1,0.001,3) # second power law exponent estimate

sig = ROOT.RooCrystalBall("sig", "double crystal ball",x,mu,sigma,alphaL,nL,alphaR,nR)

decay_constant = ROOT.RooRealVar("decay_constant", "decay_constant", -0.001, -5, 0)
bkg = ROOT.RooExponential("bkg", "Exponential Background", x, decay_constant)

#noisetosignalratio = ROOT.RooRealVar("noisetosignalratio", "fraction of noise in signal", 0.1, 0.0, 0.5)
nsig = ROOT.RooRealVar("nsig", "number of signal events", data.sumEntries()*0.75, 0, data.sumEntries())
nbkg = ROOT.RooRealVar("nbkg", "number of background events", data.sumEntries()*0.25, 0, data.sumEntries())

model = ROOT.RooAddPdf("model", "Signal + Background",ROOT.RooArgSet(bkg,sig),ROOT.RooArgList(nbkg, nsig))
#endregion DefPDF

# region FIT

fit_result = model.fitTo(data, ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Strategy(2), ROOT.RooFit.Minimizer("Minuit2"),ROOT.RooFit.Extended(True),ROOT.RooFit.Save(),ROOT.RooFit.Minos(True))



# Access the covariance matrix
covMatrix = fit_result.covarianceMatrix()

number_of_bins = 40

frame1 = x.frame()
frame1.SetTitle("")
data.plotOn(frame1,ROOT.RooFit.Name("data"),ROOT.RooFit.Binning(number_of_bins))
model.plotOn(frame1,ROOT.RooFit.Name("sig+bkg"), ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.LineStyle(ROOT.kSolid))
model.plotOn(frame1, ROOT.RooFit.Components("bkg"),ROOT.RooFit.Name("bkg"), ROOT.RooFit.LineColor(ROOT.kGreen),ROOT.RooFit.LineStyle(ROOT.kDashed))
model.plotOn(frame1, ROOT.RooFit.Components("sig"),ROOT.RooFit.Name("sig"), ROOT.RooFit.LineColor(ROOT.kRed), ROOT.RooFit.LineStyle(ROOT.kDotted),ROOT.RooFit.LineStyle(ROOT.kDotted))  # Overall DCB

chi2 = frame1.chiSquare("sig+bkg", "data",9)
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
    legend.AddEntry(dummy_sig_line, "Signal", "l")  # Red dotted line

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
mean_val = ROOT.std.vector('double')()
mean_err_high = ROOT.std.vector('double')()
mean_err_low = ROOT.std.vector('double')()

sigma_val = ROOT.std.vector('double')()
sigma_err_high = ROOT.std.vector('double')()
sigma_err_low = ROOT.std.vector('double')()

alphaL_val = ROOT.std.vector('double')()
alphaL_err_high = ROOT.std.vector('double')()
alphaL_err_low = ROOT.std.vector('double')()

alphaR_val = ROOT.std.vector('double')()
alphaR_err_high = ROOT.std.vector('double')()
alphaR_err_low = ROOT.std.vector('double')()

nL_val = ROOT.std.vector('double')()
nL_err_high = ROOT.std.vector('double')()
nL_err_low = ROOT.std.vector('double')()


nR_val = ROOT.std.vector('double')()
nR_err_high = ROOT.std.vector('double')()
nR_err_low = ROOT.std.vector('double')()

decay_constant_val = ROOT.std.vector('double')()
decay_constant_err_high = ROOT.std.vector('double')()
decay_constant_err_low = ROOT.std.vector('double')()

chi2_val = ROOT.std.vector('double')()

nsig_val = ROOT.std.vector('double')()
nsig_err_high = ROOT.std.vector('double')()
nsig_err_low = ROOT.std.vector('double')()

nbkg_val = ROOT.std.vector('double')()
nbkg_err_high = ROOT.std.vector('double')()
nbkg_err_low = ROOT.std.vector('double')()

timing_val = ROOT.std.vector('double')()
pid_kaon_flag = ROOT.std.vector('double')()
pid_pion_flag = ROOT.std.vector('double')()



mean_val.push_back(mu.getVal())
mean_err_high.push_back(mu.getAsymErrorHi())
mean_err_low.push_back(mu.getAsymErrorLo())

sigma_val.push_back(sigma.getVal())
sigma_err_high.push_back(sigma.getAsymErrorHi())
sigma_err_low.push_back(sigma.getAsymErrorLo())

alphaL_val.push_back(alphaL.getVal())
alphaL_err_high.push_back(alphaL.getAsymErrorHi())
alphaL_err_low.push_back(alphaL.getAsymErrorLo())

alphaR_val.push_back(alphaR.getVal())
alphaR_err_high.push_back(alphaR.getAsymErrorHi())
alphaR_err_low.push_back(alphaR.getAsymErrorLo())

nL_val.push_back(nL.getVal())
nL_err_high.push_back(nL.getAsymErrorHi())
nL_err_low.push_back(nL.getAsymErrorLo())

nR_val.push_back(nR.getVal())
nR_err_high.push_back(nR.getAsymErrorHi())
nR_err_low.push_back(nR.getAsymErrorLo())

decay_constant_val.push_back(decay_constant.getVal())
decay_constant_err_high.push_back(decay_constant.getAsymErrorHi())
decay_constant_err_low.push_back(decay_constant.getAsymErrorLo())

chi2_val.push_back(chi2)

nsig_val.push_back(nsig.getVal())
nsig_err_high.push_back(nsig.getAsymErrorHi())
nsig_err_low.push_back(nsig.getAsymErrorLo())

nbkg_val.push_back(nbkg.getVal())
nbkg_err_high.push_back(nbkg.getAsymErrorHi())
nbkg_err_low.push_back(nbkg.getAsymErrorLo())

timing_val.push_back(timing_value)
pid_kaon_flag.push_back(PID_kaon_value)
pid_pion_flag.push_back(PID_pion_value)


# Create branches in the tree
tree.Branch("timing",timing_val)
tree.Branch("pid_kaon_flag",pid_kaon_flag)
tree.Branch("pid_pion_flag",pid_pion_flag)

tree.Branch("mean", mean_val)
tree.Branch("mean_error_high", mean_err_high)
tree.Branch("mean_error_low", mean_err_low)

tree.Branch("sigma", sigma_val)
tree.Branch("sigma_error_high", sigma_err_high)
tree.Branch("sigma_error_low", sigma_err_low)

tree.Branch("alphaL", alphaL_val)
tree.Branch("alphaL_error_high", alphaL_err_high)
tree.Branch("alphaL_error_low", alphaL_err_low)

tree.Branch("alphaR", alphaR_val)
tree.Branch("alphaR_error_high", alphaR_err_high)
tree.Branch("alphaR_error_low", alphaR_err_low)

tree.Branch("nL", nL_val)
tree.Branch("nL_error_high", nL_err_high)
tree.Branch("nL_error_low", nL_err_low)

tree.Branch("nR", nR_val)
tree.Branch("nR_error_high", nR_err_high)
tree.Branch("nR_error_low", nR_err_low)

tree.Branch("decay_constant", decay_constant_val)
tree.Branch("decay_constant_error_high", decay_constant_err_high)
tree.Branch("decay_constant_error_low", decay_constant_err_low)

tree.Branch("chi2", chi2_val)

tree.Branch("nsig", nsig_val)
tree.Branch("nsig_error_high", nsig_err_high)
tree.Branch("nsig_error_low", nsig_err_low)

tree.Branch("nbkg", nbkg_val)
tree.Branch("nbkg_error_high", nbkg_err_high)
tree.Branch("nbkg_error_low", nbkg_err_low)

tree.Branch("timing", timing_val)
tree.Branch("pid_kaon_flag", pid_kaon_flag)
tree.Branch("pid_pion_flag", pid_pion_flag)


# Fill the tree with values
tree.Fill()

# Write the tree to the file
tree.Write()

# Close the ROOT file
output_file.Close()

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

print(sigma_err_high,sigma_err_low)







