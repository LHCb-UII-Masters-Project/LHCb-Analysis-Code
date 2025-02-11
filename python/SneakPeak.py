#---------------------------------Imports---------------------------------------------------
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

parser = argparse.ArgumentParser(description='Open a ROOT file and process data.')
parser.add_argument('input_file', type=str, help='Path to the input ROOT file') 
args = parser.parse_args()
input_directory = os.path.dirname(args.input_file)

root_file = ROOT.TFile.Open(args.input_file, "READ") 
run_tree = root_file.Get("RunParams")
outputs = root_file.Get("Outputs")
diagnostics = root_file.Get("RunDiagnostics")
run_tree.SetDirectory(0)
outputs.SetDirectory(0)
diagnostics.SetDirectory(0)
root_file.Close()
#Use RDataFrame to access the data 
rdf = ROOT.RDataFrame(outputs) 
rdf_diagnostics = ROOT.RDataFrame(diagnostics) 
# Convert the bs_mass branch to a Numpy array
#unbinned_data = rdf_diagnostics.AsNumpy()["xiccpp_mass"]
#filtered_data = unbinned_data[unbinned_data > 1]

xiccpp_data = rdf_diagnostics.AsNumpy()["xiccpp_mass"]
xiccpp_signal_data_post = rdf_diagnostics.AsNumpy()["xiccpp_is_signal_mass_post_selections"]
xiccpp_signal_data_pre = rdf_diagnostics.AsNumpy()["xiccpp_is_signal_mass_pre_selections"]
lambdac_data = rdf.AsNumpy()["lambdac_mass"]
lambdac_signal_data_post = rdf_diagnostics.AsNumpy()["lambdac_is_signal_mass_post_selections"]
lambdac_signal_data_pre = rdf_diagnostics.AsNumpy()["lambdac_is_signal_mass_pre_selections"]



filtered_xiccpp_data = xiccpp_data[xiccpp_data > 1]
filtered_xiccpp_signal_data_post = xiccpp_signal_data_post[xiccpp_signal_data_post>1]
filtered_xiccpp_signal_data_pre = xiccpp_signal_data_pre[xiccpp_signal_data_pre>1]
filtered_lambdac_data = lambdac_data[lambdac_data > 1]
filtered_lambdac_signal_data_post = lambdac_signal_data_post[lambdac_signal_data_post>1]
filtered_lambdac_signal_data_pre = lambdac_signal_data_pre[lambdac_signal_data_pre>1]



number_of_bins = 100

xiccpp_hist = TH1D("xiccpp_hist", "Xiccpp All", number_of_bins, min(filtered_xiccpp_data), max(filtered_xiccpp_data))
for dp in filtered_xiccpp_data:
    xiccpp_hist.Fill(dp)
xiccpp_hist.SetTitle("Xiccpp All")
xiccpp_hist.SetXTitle("Xiccpp Mass")
xiccpp_hist.SetYTitle("Counts")

xiccpp_signal_hist_post = TH1D("xiccpp_signal_hist_post", "Xiccpp Signal POST", number_of_bins, min(filtered_xiccpp_data), max(filtered_xiccpp_data))
for dp in filtered_xiccpp_signal_data_post:
    xiccpp_signal_hist_post.Fill(dp)
xiccpp_signal_hist_post.SetTitle("Xiccpp Signal")
xiccpp_signal_hist_post.SetXTitle("Xiccpp Signal Mass Post Checks")
xiccpp_signal_hist_post.SetYTitle("Counts")

"""
xiccpp_signal_hist_pre = TH1D("xiccpp_signal_hist_pre", "Xiccpp Signal Pre", number_of_bins, min(filtered_xiccpp_signal_data_pre), max(filtered_xiccpp_signal_data_pre))
for dp in filtered_xiccpp_signal_data_pre:
    xiccpp_signal_hist_pre.Fill(dp)
xiccpp_signal_hist_pre.SetTitle("Xiccpp Signal Pre Checks")
xiccpp_signal_hist_pre.SetXTitle("Xiccpp Signal Mass Pre Checks")
xiccpp_signal_hist_pre.SetYTitle("Counts")
"""

lambdac_hist = TH1D("lambdac_hist", "Lambdac All", number_of_bins, min(filtered_lambdac_data), max(filtered_lambdac_data))
for dp in filtered_lambdac_data:
    lambdac_hist.Fill(dp)
lambdac_hist.SetTitle("Lambdac All")
lambdac_hist.SetXTitle("Lambdac Mass")
lambdac_hist.SetYTitle("Counts")

lambdac_signal_hist_post = TH1D("lambdac_signal_hist_post", "Lambdac Signal POST", number_of_bins, min(filtered_lambdac_data) , max(filtered_lambdac_data))
for dp in filtered_lambdac_signal_data_post:
    lambdac_signal_hist_post.Fill(dp)
lambdac_signal_hist_post.SetTitle("Lambdac Signal Post Checks")
lambdac_signal_hist_post.SetXTitle("Lambdac Signal Mass Post Checks")
lambdac_signal_hist_post.SetYTitle("Counts")

lambdac_signal_hist_pre = TH1D("lambdac_signal_pre", "Lambdac Signal Pre", number_of_bins, min(filtered_lambdac_data), max(filtered_lambdac_data))
for dp in filtered_lambdac_signal_data_pre:
    lambdac_signal_hist_pre.Fill(dp)
lambdac_signal_hist_pre.SetTitle("Lambdac Signal Pre Checks")
lambdac_signal_hist_pre.SetXTitle("Lambdac Signal Mass Pre Checks")
lambdac_signal_hist_pre.SetYTitle("Counts")



with LHCbStyle() as lbs:
    c = ROOT.TCanvas("rf201_composite", "rf201_composite", 800, 1000)
    c.Divide(2,2)
    # First pad
    c.cd(1)
    xiccpp_hist.Draw("HIST")
    
    c.cd(2)
    xiccpp_signal_hist_post.Draw("HIST")

    #c.cd(3)
    #xiccpp_signal_hist_pre.Draw("HIST")

    c.cd(3)
    lambdac_hist.Draw("HIST")
    
    c.cd(4)
    lambdac_signal_hist_post.Draw("HIST")

    #c.cd(6)
    #lambdac_signal_hist_pre.Draw("HIST")
    
    c.cd()
    c.Update()
    c.Draw()
    c.SaveAs(f"{input_directory}/sneakypeaky.pdf","pdf 500")
