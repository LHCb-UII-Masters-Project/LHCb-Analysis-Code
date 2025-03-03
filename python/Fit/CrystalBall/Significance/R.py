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

def ExtractEff(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Regex pattern to match floating point numbers (including scientific notation)
    pattern = (
        r"Efficiency\s*=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*\+-\s*"
        r"([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)"
    )
    match = re.search(pattern, content)
    if match:
        efficiency = float(match.group(1))
        error = float(match.group(2))
        return efficiency, error
    else:
        raise ValueError("Efficiency data not found in the file.")


class GetVariables:
    def __init__(self, workspace_file, efficiency_purity_file):
        self.file = ROOT.TFile(workspace_file)
        self.w = self.file.Get("w")
        self.model = self.w["model"]
        self.data = self.w["data"]
        self.run_diagnostics = self.w["RunDiagnostics"]
        self.run_params = self.w["RunParams"]
        self.outputs = self.w["Outputs"]
       
        self.initial_signal = self.outputs.GetEntries()
        self.efficiency, self.efficiency_error = ExtractEff(efficiency_purity_file)
        self.nsig = self.w["nsig"].getVal()
        self.nsig_error_low = self.w["nsig"].getErrorLo()
        self.nsig_error_high = self.w["nsig"].getErrorHi()
        self.nsig_error_avg = self.w["nsig"].getError()
        self.nbkg = self.w["nbkg"].getVal()
        self.nbkg_error_low = self.w["nbkg"].getErrorLo()
        self.nbkg_error_high = self.w["nbkg"].getErrorHi()
        self.nbkg_error_avg = self.w["nbkg"].getError()
    
class Calculate:
    def __init__(self, signal, control):
        self.signal = signal
        self.control = control
        
        self.acceptance_control = 0.08888655271274595
        self.acceptance_control_error = 0.000377767084151423
        
        self.acceptance_signal = 0.08432470964835002
        self.acceptance_signal_error = 0.0003583034556616932
        
        self.run2_efficiency_ratio = 1.167
        self.run2_efficiency_ratio_error = 0.114        
       
        self.run2_r_limit = 0.035*5

        self.Run2Luminosity = 1.7+1.7+2.2
        self.Run5Luminosity = 300 # Check with Dan

    def Run5EffRatio(self):
        return ((self.control.efficiency*self.acceptance_control)/ (self.signal.efficiency*self.acceptance_signal))
        
    def LuminosityScale(self):
        return (self.Run5Luminosity/self.Run2Luminosity)
        
    def Run5Rlimit(self):
        return ((self.run2_r_limit * np.sqrt(self.Run5EffRatio() / self.run2_efficiency_ratio))/np.sqrt(self.LuminosityScale()))

    def Run5RlimitError(self):
        # R = (AB/CDE)
        A = self.control.efficiency
        Aerr = self.control.efficiency_error
        B =  self.acceptance_control
        Berr = self.acceptance_control_error
        C= self.signal.efficiency
        Cerr = self.signal.efficiency_error
        D= self.acceptance_signal
        Derr = self.acceptance_signal_error
        E = self.run2_efficiency_ratio
        Eerr = self.run2_efficiency_ratio_error
        numerator = A*B
        denominator = C*D*E
        numeratorErr = np.sqrt( Aerr**2*(B)**2 + Berr**2*(A)**2)
        denominatorErr = np.sqrt( Cerr**2*(D*E)**2 + Derr**2*(C*E)**2 + Eerr**2*(C*D)**2)
        finalErr = np.sqrt( numeratorErr**2*(1/numerator)**2 + denominatorErr**2*(numerator/(denominator)**2)**2)/np.sqrt(self.LuminosityScale())
        return finalErr



if __name__ == "__main__":

    velo_timings = [30,50,70,100]
    rvalues = []
    rerrors = []
    for time in velo_timings:
        signal =  GetVariables(f"/home/user294/Documents/selections/python/Outputs/XisToXis/Velo{time}DanFix/xiccp_5_sigma/WSPACE.root" , f"/home/user294/Documents/selections/python/Outputs/XisToXis/Velo{time}DanFix/xiccp_5_sigma/PurityEfficiency.txt")
        control = GetVariables(f"/home/user294/Documents/selections/python/Outputs/XisToLambdas/Velo{time}DanFix/xiccpp_5_sigma/WSPACE.root", f"/home/user294/Documents/selections/python/Outputs/XisToLambdas/Velo{time}DanFix/xiccpp_5_sigma/PurityEfficiency.txt")
        calc = Calculate(signal, control)
        rvalue = calc.Run5Rlimit()
        error = calc.Run5RlimitError()
        rvalues.append(rvalue)
        rerrors.append(error)
        print(f"Run 5 R Limit for Velo {time} = {rvalue:.4g} \u00B1 {error:.4g}")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D  # Import Line2D for custom legend handles
import seaborn as sns

rvalues.append(0.175)
rerrors.append(0)

# Example data (replace with actual values)
velo_timings = ["30 ps", "50 ps", "70 ps", "100 ps", "Run 2"]  # Y-axis categories
rvalues = np.array(rvalues, dtype=float)  # Deviation from theoretical R
rerrors = np.array(rerrors, dtype=float)  # Confidence intervals
theoretical_R = 0.04  # Reference value for theoretical

# Set Seaborn style
sns.set(style="ticks")

# Create figure and axis
fig, ax = plt.subplots(figsize=(7, 5))

# Define y positions for categorical data
y_positions = np.arange(len(velo_timings))

# Define bar left/right deviations from the theoretical R
bar_lefts = np.full_like(rvalues, theoretical_R)  # Start all bars from x=0.04
bar_widths = rvalues - theoretical_R  # Deviation from theoretical R

# Define colors (blue for R5, red for R2 sensitivity)
colors = ['#4682B4', '#4682B4', '#4682B4', '#4682B4', '#B22222']

# Add horizontal bars (Waterfall effect)
bars = ax.barh(y_positions, bar_widths, height=0.6, alpha=1, color=colors, left=bar_lefts, label="Predicted Sensitivity")

# Add error bars extending from the bar ends
ax.errorbar(rvalues, y_positions, xerr=rerrors, fmt='o', color='black', 
            elinewidth=1, capsize=3, capthick=1, ecolor='black', label="Predicted Sensitivity")

# Add reference vertical line for theoretical R
ax.axvline(x=theoretical_R, color='black', linestyle='-', linewidth=3, label="Theoretical R")

# Set labels
ax.set_ylabel("Timings", fontsize=16, fontweight='bold')
ax.set_xlabel("R", fontsize=16, fontweight='bold')

# Set y-axis ticks to categorical labels
ax.set_yticks(y_positions)
ax.set_yticklabels(velo_timings, fontsize=14)

# Customize grid and limits
ax.set_xlim(0, 0.18)
ax.minorticks_on()
ax.tick_params(axis='both', which='major', labelsize=14, width=1, direction='in', length=10)
ax.tick_params(axis='both', which='minor', width=1, direction='in', length=5)

# Add legend
line_handle = Line2D([0], [0], color='black', linewidth=3)  # Theoretical R
ax.legend([line_handle, bars[0], bars[4]], ['Theoretical R', 'R5 Sensitivity (Predicted)', 'R2 Sensitivity (95% CI)'],
          loc='upper left', fontsize=12, frameon=False)

# Save and show the plot
plt.tight_layout()
plt.savefig("/home/user294/Documents/selections/python/Fit/CrystalBall/Significance/waterfall_vertical.pdf", format='pdf')
plt.show()