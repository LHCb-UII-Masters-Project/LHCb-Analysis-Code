import ROOT
from ROOT import TFile, TTree
import argparse
import numpy as np
import os
import numpy as np
from scipy.stats import norm

binomialError = lambda eff,N : np.sqrt(eff*(1-eff)/N)
bayesianError = lambda eff,N : np.sqrt((N*eff+1)*(N*eff+2)/(N+2)/(N+3) - ((N*eff+1)/(N+2))**2)

def wilsonError(eff,N,level=0.68,bUpper=True):
    if N==0:
        if bUpper:
            return 1
        else:
            return 0
    
    alpha = (1-level)/2
    kappa = norm.ppf(1-alpha)
    mode = (eff*N+kappa**2/2)/(N+kappa**2)
    delta = kappa/(N+kappa**2)*np.sqrt(eff*N*(1-eff)+kappa**2/4)
    
    if bUpper:
        return (1 if mode+delta>1 else mode+delta)
    else:
        return (0 if mode-delta<0 else mode-delta)

def wilsonEffErr(eff,N,level=0.68,useWilsonAdjEff = False):
    upper = wilsonError(eff,N,level=level,bUpper=True)
    lower = wilsonError(eff,N,level=level,bUpper=False)
    if useWilsonAdjEff:
        return (upper + lower)/2 ,(upper - lower)/2
    else:
        return eff ,(upper - lower)/2

def wilsonEffGet(eff,N,level=0.68):
    upper = wilsonError(eff,N,level=level,bUpper=True)
    lower = wilsonError(eff,N,level=level,bUpper=False)
    return (upper + lower)/2

def wilsonErrGet(eff,N,level=0.68):
    upper = wilsonError(eff,N,level=level,bUpper=True)
    lower = wilsonError(eff,N,level=level,bUpper=False)
    return (upper - lower)/2

effErrTypeDict = {"binomial":binomialError, "bayesian":bayesianError,"wilson":wilsonErrGet}


def effError(efficiency, N, efficType="wilson"):
    '''
    Get efficiency error for a given efficiency calculation
    efficiency - Calculated value of efficiency
    N - denominator
    efficType - "binomial", "bayesian"
    '''


    return effErrTypeDict[efficType](efficiency,N)

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

pur_error = 0
effErr = effError(efficiency,len([val for val in values["xiccpp_mass"] if val > 0]))

with open(f"{input_directory}/PandE.txt", "w") as file:
    file.write(f"Purity = {purity}\n")
    file.write(f"Efficiency = {efficiency} +- {effErr}\n")
