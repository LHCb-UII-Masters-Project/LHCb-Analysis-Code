import ROOT
from ROOT import TFile, TTree
import argparse
import numpy as np
import os

# --------------------------------- File Inputs ---------------------------------------------------
parser = argparse.ArgumentParser(description='Open a ROOT file and process data.')
parser.add_argument('input_file', type=str, help='Path to the input ROOT file') 
args = parser.parse_args()
input_directory = os.path.dirname(args.input_file)

# ------------------------------- Tree Reading ---------------------------------------------------
root_file = TFile.Open(args.input_file, "READ") 
run_diag = root_file.Get("RunDiagnostics")

# Dictionary to store extracted values
branches = [
    "lambdac_signal_combined_momentum_kills", "lambdac_bkg_combined_momentum_kills",
    "lambdac_mass_limit_signal_kills", "lambdac_mass_limit_bkg_kills",
    "lambdac_final_mass_cut_signal_kills", "lambdac_final_mass_cut_bkg_kills",
    "lambdac_vtx_chi2_ndof_signal_kills", "lambdac_vtx_chi2_ndof_bkg_kills",
    "lambdac_vtx_chi2_distance_sig_kills", "lambdac_vtx_chi2_distance_bac_kills",
    "lambdac_vtx_dira_sig_kills", "lambdac_vtx_dira_bac_kills",
    "xi_charge_conservation_signal_kills", "xi_charge_conservation_bkg_kills",
    "xi_vtx_chi2_ndof_sig_kills", "xi_vtx_chi2_ndof_bkg_kills",
    "xi_signal_minimum_momentum_kills", "xi_bkg_minimum_momentum_kills",
    "xi_vtx_chi2_distance_sig_kills", "xi_chi2_disatance_bac_kills",
    "xi_vtx_dira_sig_kills", "xi_vtx_dira_bkg_kills",
    "xi_mass_sig_kills", "xi_mass_bkg_kills"
]

# Create dictionaries to store values and set branch addresses
values = {branch: [] for branch in branches}
buffers = {branch: np.array([0], dtype=np.float32) for branch in branches}

for branch in branches:
    run_diag.SetBranchAddress(branch, buffers[branch])

# Loop over tree entries to extract values
n_entries = run_diag.GetEntries()
for i in range(n_entries):
    run_diag.GetEntry(i)
    for branch in branches:
        values[branch].append(buffers[branch][0])

# Compute max values
max_values = {branch: np.max(values[branch]) for branch in branches}

# Print results
print("Results:")
for i in range(0, len(branches), 2):
    print(f"{branches[i]}: {max_values[branches[i]]} : {max_values[branches[i+1]]}")

# Close file
root_file.Close()
