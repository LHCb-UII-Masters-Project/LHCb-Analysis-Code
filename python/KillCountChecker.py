import ROOT
from ROOT import TFile, TTree
import argparse
import numpy as np
import os
from os import path
import sys
import csv
import pandas as pd

basedir=path.dirname(path.realpath(__file__))
sys.path.append(f"{path.dirname(path.realpath(__file__))}/..")
batching = False
sys.path.insert(0,basedir)

# --------------------------------- File Inputs ---------------------------------------------------
parser = argparse.ArgumentParser(description='Open a ROOT file and process data.')
parser.add_argument('input_file', type=str, help='Path to the input ROOT file') 
args = parser.parse_args()
input_directory = os.path.dirname(args.input_file)

# ------------------------------- Tree Reading --------------------------------------------------

# Dictionary to store extracted values
branches = [
    "lambdac_signal_combined_momentum_kills",
    "lambdac_bkg_combined_momentum_kills",
    "lambdac_signal_combined_momentum_remaining",
    "lambdac_bkg_combined_momentum_remaining",

    "lambdac_signal_charge_kills",
    "lambdac_bkg_charge_kills",
    "lambdac_sig_charge_remaining",
    "lambdac_bkg_charge_remaining",

    "lambdac_mass_limit_signal_kills",
    "lambdac_mass_limit_bkg_kills",
    "lambdac_mass_limit_signal_remaining",
    "lambdac_mass_limit_bkg_remaining",

    "lambdac_vtx_chi2_ndof_signal_kills",
    "lambdac_vtx_chi2_ndof_bkg_kills",
    "lambdac_vtx_chi2_ndof_signal_remaining",
    "lambdac_vtx_chi2_ndof_bkg_remaining",

    "lambdac_vtx_chi2_distance_sig_kills",
    "lambdac_vtx_chi2_distance_bkg_kills",
    "lambdac_vtx_chi2_distance_sig_remaining",
    "lambdac_vtx_chi2_distance_bkg_remaining",

    "lambdac_vtx_dira_sig_kills",
    "lambdac_vtx_dira_bkg_kills",
    "lambdac_vtx_dira_sig_remaining",
    "lambdac_vtx_dira_bkg_remaining",

    "lambdac_final_mass_cut_signal_kills",
    "lambdac_final_mass_cut_bkg_kills",
    "lambdac_final_mass_cut_signal_remaining",
    "lambdac_final_mass_cut_bkg_remaining",

    "xiccpp_miss_combo_sig_kills",
    "xiccpp_miss_combo_bkg_kills",
    "xiccpp_miss_combo_sig_remaining",
    "xiccpp_miss_combo_bkg_remaining",

    "xi_charge_conservation_signal_kills",
    "xi_charge_conservation_bkg_kills",
    "xi_charge_conservation_signal_remaining",
    "xi_charge_conservation_bkg_remaining",

    "xi_charge_sig_kills",
    "xi_charge_bkg_kills",
    "xi_charge_sig_remaining",
    "xi_charge_bkg_remaining",

    "xi_signal_minimum_momentum_kills",
    "xi_bkg_minimum_momentum_kills",
    "xi_sig_minimum_momentum_remaining",
    "xi_bkg_minimum_momentum_remaining",

    "xi_mass_sig_kills",
    "xi_mass_bkg_kills",
    "xi_mass_sig_remaining",
    "xi_mass_bkg_remaining",

    "xi_vtx_chi2_ndof_sig_kills",
    "xi_vtx_chi2_ndof_bkg_kills",
    "xi_vtx_chi2_ndof_sig_remaining",
    "xi_vtx_chi2_ndof_bkg_remaining",

    "xi_vtx_chi2_distance_sig_kills",
    "xi_chi2_disatance_bkg_kills",
    "xi_vtx_chi2_distance_sig_remaining",
    "xi_chi2_disatance_bkg_remaining",

    "xi_vtx_dira_sig_kills",
    "xi_vtx_dira_bkg_kills",
    "xi_vtx_dira_sig_remaining",
    "xi_vtx_dira_bkg_remaining",
]

df = pd.read_csv(args.input_file, columns = branches)


