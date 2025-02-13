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
df = pd.read_csv(csv_path)
num_events = int(extract_middle(input_directory))

# Compute Efficiency and Purity
df["CutEfficiency"] = df["sig_remains"] / (df["sig_remains"] + df["sig_kills"])

df["AbsEfficiency"] = df["sig_remains"] / num_events

df["AbsPurity"] = (df["sig_remains"] /
                    (df["bkg_remains"] + df["sig_remains"]))

# Save updated CSV
updated_csv_path = f"{input_directory}/PECounter.csv"
df.to_csv(updated_csv_path, index=False)

print(f"Updated CSV saved to: {updated_csv_path}")

"""
cut_names = df["cut"]
eff_values = df["Efficiency"]
purity_values = df["Purity"]

import matplotlib.pyplot as plt
plt.figure(figsize=(25, 15))  # Adjust the width and height as needed
plt.step(purity_values,cut_names)
plt.savefig(f"{input_directory}/PurityPlot.png")
plt.close()
plt.figure(figsize=(25, 15))  # Adjust the width and height as needed
plt.step(eff_values,cut_names)
plt.savefig(f"{input_directory}/EfficiencyPlot.png")
plt.close()
"""
x_labels = df["cut"]
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.set_xlabel("Cuts")
ax1.set_ylabel("Efficiency", color="tab:blue")
ax1.plot(x_labels, df["AbsEfficiency"], marker="o", linestyle="-", color="tab:blue", label="Efficiency")
ax1.tick_params(axis="y", labelcolor="tab:blue")

ax2 = ax1.twinx()
ax2.set_ylabel("Purity", color="tab:red")
ax2.plot(x_labels, df["AbsPurity"], marker="s", linestyle="--", color="tab:red", label="Purity")
ax2.tick_params(axis="y", labelcolor="tab:red")

plt.xticks(rotation=45, ha="right")
plt.title("Absolute Efficiency & Purity vs Cuts")
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.savefig(f"{input_directory}/EfficiencyPlot.png")
plt.close()
