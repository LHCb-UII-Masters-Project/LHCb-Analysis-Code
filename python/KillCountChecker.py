import ROOT
from ROOT import TFile, TTree
import argparse
import numpy as np
import os
from os import path
import sys
import csv

basedir=path.dirname(path.realpath(__file__))
sys.path.append(f"{path.dirname(path.realpath(__file__))}/..")
batching = False
sys.path.insert(0,basedir)

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

for i in range(0, len(branches), 4):
  data = [branches[i], 
  max_values[branches[i]],
  max_values[branches[i+1]],
  max_values[branches[i+2]], 
  max_values[branches[i+3]]]

  # Check if the file exists
  
  file_path = f"{basedir}/Outputs/XisToLambdas/KillCounter{(args.input_file)[-13:-5]}.csv"
  file_exists = path.isfile(file_path)
  
  # Open the file in append mode
  with open(file_path, mode='a', newline='') as file:
      writer = csv.writer(file)

      # Write header only if the file doesn't exist
      if not file_exists:
          writer.writerow(["Branch Name","SigKills", "BkgKills", "SigRemain", "BkgRemain"])

      # Append the data
      writer.writerow(data)


# Close file
root_file.Close()

## Quick Purity and Eff

root_file = TFile.Open(args.input_file, "READ") 
run_diag = root_file.Get("RunDiagnostics")

branches = [
    "xiccpp_mass",
    "lambdac_is_signal_mass_pre_selections",
    "lambdac_is_signal_mass_post_selections",
    "xiccpp_is_signal_mass_pre_selections",
    "xiccpp_is_bkg_mass_pre_selections",
    "xiccpp_is_signal_mass_post_selections",
    "xiccpp_is_bkg_mass_post_selections"

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

purity = len([val for val in values["xiccpp_is_signal_mass_post_selections"] if val > 0]) / len([val for val in values["xiccpp_mass"] if val > 0])
efficiency = len([val for val in values["xiccpp_mass"] if val > 0]) / n_entries

print(f"Purity = {purity}")
print(f"Efficiency = {efficiency}")
