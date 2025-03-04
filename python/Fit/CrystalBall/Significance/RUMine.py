import re
import ROOT
from ROOT import TH1D, TH2D, TCanvas, TChain, TTree, TString, TFile, gInterpreter, gSystem, RooMinimizer
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
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D  # Import Line2D for custom legend handles
import seaborn as sns

velo_timings = ["30 ps", "50 ps", "70 ps", "100 ps", "200 ps", "Run 2"]  # Y-axis categories
rvalues = [0.0967, 0.0994, 0.0990, 0.1035, 0.1031, 1]
rerrors = [0.0043, 0.0044, 0.0044, 0.0046, 0.0047,0]

# Example data (replace with actual values)

rvalues = np.array(rvalues, dtype=float)  # Deviation from theoretical R
rerrors = np.array(rerrors, dtype=float)  # Confidence intervals
theoretical_R = 0.2  # Reference value for theoretical

# Set Seaborn style
sns.set(style="ticks")

# Create figure and axis
fig, ax = plt.subplots(figsize=(7, 5))

# Move "Run 2" to the first position
velo_timings = ["Run 2", "30 ps", "50 ps", "70 ps", "100 ps", "200 ps"]
rvalues = np.array([1, 0.0967, 0.0994, 0.0990, 0.1035, 0.1031])
rerrors = np.array([0, 0.0043, 0.0044, 0.0044, 0.0046, 0.0047])  # No error for Run 2

# Define x positions for categorical data
x_positions = np.arange(len(velo_timings))

# Define colors (red for Run 2, blue for others)
colors = ['#B22222', '#4682B4', '#4682B4', '#4682B4', '#4682B4', '#4682B4']

# Add vertical bars **without error bars for Run 2**
bars = ax.bar(x_positions, rvalues, width=0.6, alpha=1, color=colors, label="Predicted Sensitivity")

# Add error bars only for non-Run2 values with **thinner error lines**


# Add reference horizontal line for theoretical R
ax.axhline(y=0.2, color='black', linestyle='-', linewidth=3, label="Theoretical R")

# Set labels
ax.set_xlabel("Timings", fontsize=16, fontweight='bold')
ax.set_ylabel("R", fontsize=16, fontweight='bold')

# Set x-axis ticks to categorical labels
ax.set_xticks(x_positions)
ax.set_xticklabels(velo_timings, fontsize=14, rotation=45, ha="right")

# Customize grid and limits
ax.set_ylim(0, 1.1 * max(rvalues + rerrors))  # Ensure error bars fit
ax.minorticks_on()
ax.tick_params(axis='both', which='major', labelsize=14, width=1, direction='in', length=10)
ax.tick_params(axis='both', which='minor', width=1, direction='in', length=5)

# Move legend to the right
line_handle = Line2D([0], [0], color='black', linewidth=3)  # Theoretical R
ax.legend([line_handle, bars[1], bars[0]], ['Theoretical R', 'R5 Sensitivity (Predicted)', 'Run 2 Sensitivity (95% CI)'],
          loc='upper right', fontsize=12, frameon=False)

# Save and show the plot
plt.tight_layout()
plt.savefig("/home/user293/Documents/selections/python/Fit/CrystalBall/Significance/waterfall_thinner_errors.png", format='png', dpi=350)
plt.show()
