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
import re
import matplotlib.pyplot as plt
import lhcbstyle
from lhcbstyle import LHCbStyle

basedir=path.dirname(path.realpath(__file__))
sys.path.append(f"{path.dirname(path.realpath(__file__))}/..")
batching = False
sys.path.insert(0,basedir)

def extract_middle(text):
    match = re.search(r"TS_(.*?)_Time", text)
    return match.group(1) if match else None

# --------------------------------- File Inputs --------------------------------------------------
parser = argparse.ArgumentParser(description='Open a ROOT file and process data.')
parser.add_argument('input_file', type=str, help='Path to the input ROOT file') 
args = parser.parse_args()
input_directory = os.path.dirname(args.input_file)

# ------------------------------- Tree Reading --------------------------------------------------
# Load CSV file
csv_path = args.input_file  # Update this path if necessary
raw_df = pd.read_csv(csv_path)
rem_cuts = ["lambdac_combined_momentum", "lambdac_charge", "xi_miss_combo", "xi_charge_conservation", "xi_charge", "xi_minimum_momentum"]
df = raw_df[~raw_df['cut'].isin(rem_cuts)]
num_events = int(extract_middle(input_directory))

# Compute Efficiency and Purity
df["CutEfficiency"] = df["sig_remains"] / (df["sig_remains"] + df["sig_kills"])

df["AbsEfficiency"] = df["sig_remains"] / num_events

df["AbsPurity"] = (df["sig_remains"] / (df["bkg_remains"] + df["sig_remains"]))

# Save updated CSV
updated_csv_path = f"{input_directory}/PECounter.csv"
df.to_csv(updated_csv_path, index=False)

print(f"Updated CSV saved to: {updated_csv_path}")

# Filter data for lambdac and xi cuts
df_lambdac = df[df["cut"].str.startswith("lambdac")].copy()
df_xi = df[df["cut"].str.startswith("xi")].copy()

# Remove prefixes for lambdac and xi
df_lambdac.loc[:, "cut"] = df_lambdac["cut"].str.replace("lambdac_", "", regex=False)
df_xi.loc[:, "cut"] = df_xi["cut"].str.replace("xi_", "", regex=False)

with LHCbStyle() as lbs:
    # Plot for lambdac cuts
    x_labels_lambdac = df_lambdac["cut"].str.replace("_", " ").str.title()
    x_labels_lambdac = x_labels_lambdac.str.replace("Chi2", r"$\\chi^{2}$", regex=True).str.replace("Vtx", "Vertex")
    x_labels_lambdac = x_labels_lambdac.str.replace(" Ndof", "/ndf").str.replace(" Cut", "")
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.set_xlabel("Selection", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Efficiency", color="tab:blue", fontsize=14, fontweight="bold")
    ax1.plot(x_labels_lambdac, df_lambdac["AbsEfficiency"], marker="o", linestyle="-", color="tab:blue", label="Efficiency")
    ax1.tick_params(axis="y", labelcolor="tab:blue", labelsize=12)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Purity", color="tab:red", fontsize=14, fontweight="bold")
    ax2.plot(x_labels_lambdac, df_lambdac["AbsPurity"], marker="s", linestyle="--", color="tab:red", label="Purity")
    ax2.tick_params(axis="y", labelcolor="tab:red", labelsize=12)

    # Make the tick labels bold for x-axis
    ax1.tick_params(axis="x", labelsize=12)  # Set the font size for x-axis ticks
    ax1.set_xticklabels(x_labels_lambdac, fontweight="bold")  # Make x-axis tick labels bold
    
    # Make the tick labels bold for y-axis (Efficiency)
    ax1.tick_params(axis="y", labelsize=12)  # Set the font size for y-axis ticks (Efficiency)
    ax2.tick_params(axis="y", labelsize=12)  # Set the font size for y-axis ticks (Purity)

    # Round tick positions to 2 decimal places before setting labels
    y_ticks_1 = ax1.get_yticks()
    y_ticks_2 = ax2.get_yticks()
    ax1.set_yticklabels([f"{tick:.2f}" for tick in y_ticks_1], fontweight="bold")  # Round and bold Efficiency ticks
    ax2.set_yticklabels([f"{tick:.2f}" for tick in y_ticks_2], fontweight="bold")  # Round and bold Purity ticks

    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.title(r"Absolute Efficiency & Purity for $\Lambda_{c}^{+}$ Cuts", fontsize=16, fontweight="bold")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(f"{input_directory}/LcEPPlot.png")
    plt.close()

    # Plot for xi cuts
    x_labels_xi = df_xi["cut"].str.replace("_", " ").str.title()
    x_labels_xi = x_labels_xi.str.replace("Chi2", r"$\\chi^{2}$", regex=True).str.replace("Vtx", "Vertex")
    x_labels_xi = x_labels_xi.str.replace(" Ndof", "/ndf")

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.set_xlabel("Selection", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Efficiency", color="tab:blue", fontsize=14, fontweight="bold")
    ax1.plot(x_labels_xi, df_xi["AbsEfficiency"], marker="o", linestyle="-", color="tab:blue", label="Efficiency")
    ax1.tick_params(axis="y", labelcolor="tab:blue", labelsize=12)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Purity", color="tab:red", fontsize=14, fontweight="bold")
    ax2.plot(x_labels_xi, df_xi["AbsPurity"], marker="s", linestyle="--", color="tab:red", label="Purity")
    ax2.tick_params(axis="y", labelcolor="tab:red", labelsize=12)

    # Make the tick labels bold for x-axis
    ax1.tick_params(axis="x", labelsize=12)  # Set the font size for x-axis ticks
    ax1.set_xticklabels(x_labels_xi, fontweight="bold")  # Make x-axis tick labels bold
    
    # Make the tick labels bold for y-axis (Efficiency)
    ax1.tick_params(axis="y", labelsize=12)  # Set the font size for y-axis ticks (Efficiency)
    ax2.tick_params(axis="y", labelsize=12)  # Set the font size for y-axis ticks (Purity)

    # Round tick positions to 2 decimal places before setting labels
    y_ticks_1 = ax1.get_yticks()
    y_ticks_2 = ax2.get_yticks()
    ax1.set_yticklabels([f"{tick:.2f}" for tick in y_ticks_1], fontweight="bold")  # Round and bold Efficiency ticks
    ax2.set_yticklabels([f"{tick:.2f}" for tick in y_ticks_2], fontweight="bold")  # Round and bold Purity ticks

    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.title(r"Absolute Efficiency & Purity for $\Xi_{cc}^{++}$ Cuts", fontsize=16, fontweight="bold")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(f"{input_directory}/XiEPPlot.png")
    plt.close()
