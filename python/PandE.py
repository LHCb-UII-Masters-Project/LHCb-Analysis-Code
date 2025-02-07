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