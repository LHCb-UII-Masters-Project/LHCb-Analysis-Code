import ROOT
from ROOT import TFile, TTree
import argparse
import numpy as np
import os
from os import path
import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt
import lhcbstyle
from lhcbstyle import LHCbStyle

# Data values
x_labels = [30, 50, 70, 100]

# Control mode data (values and errors)
control_Earray = np.array([1.15, 1.13, 1.06, 1.06])
control_Eerror = np.array([0.03, 0.03, 0.03, 0.03])
control_Parray = np.array([30.33, 28.79, 26.71, 25.05])
control_Perror = np.array([0.22, 0.22, 0.22, 0.22])

# Signal mode data (values and errors)
signal_Earray = np.array([2.78, 2.59, 2.45, 2.24])
signal_Eerror = np.array([0.05, 0.05, 0.05, 0.05])
signal_Parray = np.array([27.01, 24.00, 17.42, 16.37])
signal_Perror = np.array([0.22, 0.22, 0.22, 0.22])


# Function to plot efficiency and purity
def plot_eff_purity(x_labels, efficiency, efficiency_err, purity, purity_err, title, filename):
    with LHCbStyle():
        fig, ax1 = plt.subplots(figsize=(8, 6))

        # Efficiency Plot (left axis)
        ax1.set_xlabel("Timing Resolution (ps)", fontsize=20, fontweight="bold")
        ax1.set_ylabel("Percentage Efficiency", color="tab:blue", fontsize=20, fontweight="bold")
        #ax1.errorbar(x_labels, efficiency, yerr=efficiency_err, fmt="o-", color="tab:blue", label="Efficiency")
        ax1.errorbar(
            x_labels,
            efficiency,
            yerr=efficiency_err,
            fmt="o-",  # Circle marker for efficiency
            color="tab:blue",
            label="Efficiency",
            markersize=5,  # Adjust marker size
            capsize=4  # Add caps to error bars and set size
        )
        ax1.tick_params(axis="y", labelcolor="tab:blue", labelsize=16)

        # Purity Plot (right axis)
        ax2 = ax1.twinx()
        ax2.set_ylabel("Percentage Purity", color="tab:red", fontsize=20, fontweight="bold")
        #ax2.errorbar(x_labels, purity, yerr=purity_err, fmt="s--", color="tab:red", label="Purity")
        ax2.errorbar(
            x_labels,
            purity,
            yerr=purity_err,
            fmt="s--",  # Square marker for purity remains the same
            color="tab:red",
            label="Purity",
            markersize=5,  # Adjust marker size
            capsize=4  # Add caps to error bars and set size
        )
        ax2.tick_params(axis="y", labelcolor="tab:red", labelsize=16)

        # Ensure zero is not suppressed
        # Find common y-axis limits
        min_y = min(np.min(efficiency - efficiency_err), np.min(purity - purity_err))
        max_y = max(np.max(efficiency + efficiency_err), np.max(purity + purity_err))
        ax1.set_ylim(min_y * 0.95, (max_y* 1.05)/20)  # Add some margin
        ax2.set_ylim(min_y * 0.95, max_y * 1.05)  # Same limits for both axes

        ax1.set_ylim(bottom=1)
        ax2.set_ylim(bottom=20)

        # Make x-axis labels bold
        ax1.tick_params(axis="x", labelsize=16)
        ax1.set_xticks(x_labels)
        ax1.set_xticklabels([str(label) for label in x_labels], fontweight="bold")

        # Ensure rounded y-axis tick labels
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.1f}"))
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}"))

        # Set title and grid
        plt.title(title, fontsize=20, fontweight="bold")
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

# Plot for control mode
plot_eff_purity(x_labels, control_Earray, control_Eerror, control_Parray, control_Perror,
                "", "Control_EPPlot.pdf")

# Plot for signal mode
plot_eff_purity(x_labels, signal_Earray, signal_Eerror, signal_Parray, signal_Perror,
                "Efficiency & Purity of Signal Mode Candidate Arrays", "Signal_EPPlot.pdf")
