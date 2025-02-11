import ROOT
from ROOT import TFile, TTree
import argparse
import numpy as np
import os
from os import path
import sys
import csv
import pandas as pd
import pandas as pd
import time

basedir=path.dirname(path.realpath(__file__))
sys.path.append(f"{path.dirname(path.realpath(__file__))}/..")
batching = False
sys.path.insert(0,basedir)

# --------------------------------- File Inputs --------------------------------------------------
parser = argparse.ArgumentParser(description='Open a ROOT file and process data.')
parser.add_argument('input_file', type=str, help='Path to the input ROOT file') 
args = parser.parse_args()
input_directory = os.path.dirname(args.input_file)

# ------------------------------- Tree Reading --------------------------------------------------

# Dictionary to store extracted values
branches = [
    # Group 1: "combined_momentum"
    "lambdac_signal_combined_momentum_kills",
    "lambdac_bkg_combined_momentum_kills",
    "lambdac_signal_combined_momentum_remaining",
    "lambdac_bkg_combined_momentum_remaining",
    "lambdac_combined_momentum_purity",  # New column

    # Group 2: "charge"
    "lambdac_signal_charge_kills",
    "lambdac_bkg_charge_kills",
    "lambdac_sig_charge_remaining",
    "lambdac_bkg_charge_remaining",
    "lambdac_charge_efficiency",  # New column
    "lambdac_charge_purity",  # New column

    # Group 3: "mass_limit"
    "lambdac_mass_limit_signal_kills",
    "lambdac_mass_limit_bkg_kills",
    "lambdac_mass_limit_signal_remaining",
    "lambdac_mass_limit_bkg_remaining",
    "lambdac_mass_limit_efficiency",  # New column
    "lambdac_mass_limit_purity",  # New column

    # Group 4: "vtx_chi2_ndof"
    "lambdac_vtx_chi2_ndof_signal_kills",
    "lambdac_vtx_chi2_ndof_bkg_kills",
    "lambdac_vtx_chi2_ndof_signal_remaining",
    "lambdac_vtx_chi2_ndof_bkg_remaining",
    "lambdac_vtx_chi2_ndof_efficiency",  # New column
    "lambdac_vtx_chi2_ndof_purity",  # New column

    # Group 5: "vtx_chi2_distance"
    "lambdac_vtx_chi2_distance_sig_kills",
    "lambdac_vtx_chi2_distance_bkg_kills",
    "lambdac_vtx_chi2_distance_sig_remaining",
    "lambdac_vtx_chi2_distance_bkg_remaining",
    "lambdac_vtx_chi2_distance_efficiency",  # New column
    "lambdac_vtx_chi2_distance_purity",  # New column

    # Group 6: "vtx_dira"
    "lambdac_vtx_dira_sig_kills",
    "lambdac_vtx_dira_bkg_kills",
    "lambdac_vtx_dira_sig_remaining",
    "lambdac_vtx_dira_bkg_remaining",
    "lambdac_vtx_dira_efficiency",  # New column
    "lambdac_vtx_dira_purity",  # New column

    # Group 7: "final_mass_cut"
    "lambdac_final_mass_cut_signal_kills",
    "lambdac_final_mass_cut_bkg_kills",
    "lambdac_final_mass_cut_signal_remaining",
    "lambdac_final_mass_cut_bkg_remaining",
    "lambdac_final_mass_cut_efficiency",  # New column
    "lambdac_final_mass_cut_purity",  # New column

    # Group 8: "xiccpp_miss_combo"
    "xiccpp_miss_combo_sig_kills",
    "xiccpp_miss_combo_bkg_kills",
    "xiccpp_miss_combo_sig_remaining",
    "xiccpp_miss_combo_bkg_remaining",
    "xiccpp_miss_combo_efficiency",  # New column
    "xiccpp_miss_combo_purity",  # New column

    # Group 9: "xi_charge_conservation"
    "xi_charge_conservation_signal_kills",
    "xi_charge_conservation_bkg_kills",
    "xi_charge_conservation_signal_remaining",
    "xi_charge_conservation_bkg_remaining",
    "xi_charge_conservation_efficiency",  # New column
    "xi_charge_conservation_purity",  # New column

    # Group 10: "xi_charge"
    "xi_charge_sig_kills",
    "xi_charge_bkg_kills",
    "xi_charge_sig_remaining",
    "xi_charge_bkg_remaining",
    "xi_charge_efficiency",  # New column
    "xi_charge_purity",  # New column

    # Group 11: "xi_signal_minimum_momentum"
    "xi_signal_minimum_momentum_kills",
    "xi_bkg_minimum_momentum_kills",
    "xi_sig_minimum_momentum_remaining",
    "xi_bkg_minimum_momentum_remaining",
    "xi_minimum_momentum_efficiency",  # New column
    "xi_minimum_momentum_purity",  # New column

    # Group 12: "xi_mass"
    "xi_mass_sig_kills",
    "xi_mass_bkg_kills",
    "xi_mass_sig_remaining",
    "xi_mass_bkg_remaining",
    "xi_mass_efficiency",  # New column
    "xi_mass_purity",  # New column

    # Group 13: "xi_vtx_chi2_ndof"
    "xi_vtx_chi2_ndof_sig_kills",
    "xi_vtx_chi2_ndof_bkg_kills",
    "xi_vtx_chi2_ndof_sig_remaining",
    "xi_vtx_chi2_ndof_bkg_remaining",
    "xi_vtx_chi2_ndof_efficiency",  # New column
    "xi_vtx_chi2_ndof_purity",  # New column

    # Group 14: "xi_vtx_chi2_distance"
    "xi_vtx_chi2_distance_sig_kills",
    "xi_chi2_disatance_bkg_kills",
    "xi_vtx_chi2_distance_sig_remaining",
    "xi_chi2_disatance_bkg_remaining",
    "xi_vtx_chi2_distance_efficiency",  # New column
    "xi_vtx_chi2_distance_purity",  # New column

    # Group 15: "xi_vtx_dira"
    "xi_vtx_dira_sig_kills",
    "xi_vtx_dira_bkg_kills",
    "xi_vtx_dira_sig_remaining",
    "xi_vtx_dira_bkg_remaining",
    "xi_vtx_dira_efficiency",  # New column
    "xi_vtx_dira_purity"  # New column
]


df = pd.read_csv(args.input_file)  # Read all columns
df = df.assign(
    # Group 1: "combined_momentum"
    lambdac_combined_momentum_purity = 1 - (
        df["lambdac_bkg_combined_momentum_remaining"] /
        (df["lambdac_bkg_combined_momentum_remaining"] + df["lambdac_signal_combined_momentum_remaining"])
    ),

    # Group 2: "charge"
    lambdac_charge_efficiency = df["lambdac_sig_charge_remaining"] / df["lambdac_signal_combined_momentum_remaining"],
    lambdac_charge_purity = 1 - (
        df["lambdac_bkg_charge_remaining"] /
        (df["lambdac_bkg_charge_remaining"] + df["lambdac_sig_charge_remaining"])
    ),

    # Group 3: "mass_limit"
    lambdac_mass_limit_efficiency = df["lambdac_mass_limit_signal_remaining"] / df["lambdac_sig_charge_remaining"],
    lambdac_mass_limit_purity = 1 - (
        df["lambdac_mass_limit_bkg_remaining"] /
        (df["lambdac_mass_limit_bkg_remaining"] + df["lambdac_mass_limit_signal_remaining"])
    ),

    # Group 4: "vtx_chi2_ndof"
    lambdac_vtx_chi2_ndof_efficiency = df["lambdac_vtx_chi2_ndof_signal_remaining"] / df["lambdac_mass_limit_signal_remaining"],
    lambdac_vtx_chi2_ndof_purity = 1 - (
        df["lambdac_vtx_chi2_ndof_bkg_remaining"] /
        (df["lambdac_vtx_chi2_ndof_bkg_remaining"] + df["lambdac_vtx_chi2_ndof_signal_remaining"])
    ),

    # Group 5: "vtx_chi2_distance"
    lambdac_vtx_chi2_distance_efficiency = df["lambdac_vtx_chi2_distance_sig_remaining"] / df["lambdac_vtx_chi2_ndof_signal_remaining"],
    lambdac_vtx_chi2_distance_purity = 1 - (
        df["lambdac_vtx_chi2_distance_bkg_remaining"] /
        (df["lambdac_vtx_chi2_distance_bkg_remaining"] + df["lambdac_vtx_chi2_distance_sig_remaining"])
    ),

    # Group 6: "vtx_dira"
    lambdac_vtx_dira_efficiency = df["lambdac_vtx_dira_sig_remaining"] / df["lambdac_vtx_chi2_distance_sig_remaining"],
    lambdac_vtx_dira_purity = 1 - (
        df["lambdac_vtx_dira_bkg_remaining"] /
        (df["lambdac_vtx_dira_bkg_remaining"] + df["lambdac_vtx_dira_sig_remaining"])
    ),

    # Group 7: "final_mass_cut"
    lambdac_final_mass_cut_efficiency = df["lambdac_final_mass_cut_signal_remaining"] / df["lambdac_vtx_dira_sig_remaining"],
    lambdac_final_mass_cut_purity = 1 - (
        df["lambdac_final_mass_cut_bkg_remaining"] /
        (df["lambdac_final_mass_cut_bkg_remaining"] + df["lambdac_final_mass_cut_signal_remaining"])
    ),

    # Group 8: "xiccpp_miss_combo"
    xiccpp_miss_combo_efficiency = df["xiccpp_miss_combo_sig_remaining"] / df["lambdac_final_mass_cut_signal_remaining"],
    xiccpp_miss_combo_purity = 1 - (
        df["xiccpp_miss_combo_bkg_remaining"] /
        (df["xiccpp_miss_combo_bkg_remaining"] + df["xiccpp_miss_combo_sig_remaining"])
    ),

    # Group 9: "xi_charge_conservation"
    xi_charge_conservation_efficiency = df["xi_charge_conservation_signal_remaining"] / df["xiccpp_miss_combo_sig_remaining"],
    xi_charge_conservation_purity = 1 - (
        df["xi_charge_conservation_bkg_remaining"] /
        (df["xi_charge_conservation_bkg_remaining"] + df["xi_charge_conservation_signal_remaining"])
    ),

    # Group 10: "xi_charge"
    xi_charge_efficiency = df["xi_charge_sig_remaining"] / df["xi_charge_conservation_signal_remaining"],
    xi_charge_purity = 1 - (
        df["xi_charge_bkg_remaining"] /
        (df["xi_charge_bkg_remaining"] + df["xi_charge_sig_remaining"])
    ),

    # Group 11: "xi_signal_minimum_momentum"
    xi_minimum_momentum_efficiency = df["xi_sig_minimum_momentum_remaining"] / df["xi_charge_sig_remaining"],
    xi_minimum_momentum_purity = 1 - (
        df["xi_bkg_minimum_momentum_remaining"] /
        (df["xi_bkg_minimum_momentum_remaining"] + df["xi_sig_minimum_momentum_remaining"])
    ),

    # Group 12: "xi_mass"
    xi_mass_efficiency = df["xi_mass_sig_remaining"] / df["xi_sig_minimum_momentum_remaining"],
    xi_mass_purity = 1 - (
        df["xi_mass_bkg_remaining"] /
        (df["xi_mass_bkg_remaining"] + df["xi_mass_sig_remaining"])
    ),

    # Group 13: "xi_vtx_chi2_ndof"
    xi_vtx_chi2_ndof_efficiency = df["xi_vtx_chi2_ndof_sig_remaining"] / df["xi_mass_sig_remaining"],
    xi_vtx_chi2_ndof_purity = 1 - (
        df["xi_vtx_chi2_ndof_bkg_remaining"] /
        (df["xi_vtx_chi2_ndof_bkg_remaining"] + df["xi_vtx_chi2_ndof_sig_remaining"])
    ),

    # Group 14: "xi_vtx_chi2_distance"
    xi_vtx_chi2_distance_efficiency = df["xi_vtx_chi2_distance_sig_remaining"] / df["xi_vtx_chi2_ndof_sig_remaining"],
    xi_vtx_chi2_distance_purity = 1 - (
        df["xi_chi2_disatance_bkg_remaining"] /
        (df["xi_chi2_disatance_bkg_remaining"] + df["xi_vtx_chi2_distance_sig_remaining"])
    ),

    # Group 15: "xi_vtx_dira"
    xi_vtx_dira_efficiency = df["xi_vtx_dira_sig_remaining"] / df["xi_vtx_chi2_distance_sig_remaining"],
    xi_vtx_dira_purity = 1 - (
        df["xi_vtx_dira_bkg_remaining"] /
        (df["xi_vtx_dira_bkg_remaining"] + df["xi_vtx_dira_sig_remaining"])
    )
)
df = df[branches]
# Assuming 'df' is your DataFrame with one row and the columns listed above:
df.to_csv(f"{input_directory}/CutPandE.csv", index = False)
df_transposed = df.T  # Transpose: rows become columns, columns become rows
# Reset the index to convert the original column names into a regular column
df_transposed = df_transposed.reset_index()
# Rename the columns to "Variable" (for the original column names) and "Value" (for the corresponding data)
df_transposed.columns = ["Variable", "Value"]
df_transposed.to_csv(f"{input_directory}/TCutPandE.csv",index = False)

eff_columns = [col for col in list(df.columns) if "efficiency" in col]
eff_values = df[eff_columns].iloc[0]

purity_columns = [col for col in list(df.columns) if "purity" in col]
purity_values = df[purity_columns].iloc[0]

import matplotlib.pyplot as plt
plt.figure(figsize=(25, 15))  # Adjust the width and height as needed
plt.step(purity_values,purity_columns)
plt.savefig(f"{input_directory}/PurityPlot.png")
plt.close()
plt.figure(figsize=(25, 15))  # Adjust the width and height as needed
plt.step(eff_values,eff_columns)
plt.savefig(f"{input_directory}/EfficiencyPlot.png")
plt.close()