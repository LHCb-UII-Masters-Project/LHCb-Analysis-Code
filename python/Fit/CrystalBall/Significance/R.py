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
       
        self.run2_r_limit = 5

    def Run5EffRatio(self):
        return ((self.control.efficiency*self.acceptance_control)/ (self.signal.efficiency*self.acceptance_signal))
        
    def Run5Rlimit(self):
        return (self.run2_r_limit * np.sqrt(self.Run5EffRatio() / self.run2_efficiency_ratio))
    
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
        finalErr = np.sqrt( numeratorErr**2*(1/numerator)**2 + denominatorErr**2*(numerator/(denominator)**2)**2)
        return finalErr



if __name__ == "__main__":

    velo_timings = [30,50,70,100,200]
    for time in velo_timings:
        signal =  GetVariables(f"/home/user294/Documents/selections/python/Outputs/XisToXis/Velo{time}DanFix/xiccp_5_sigma/WSPACE.root" , f"/home/user294/Documents/selections/python/Outputs/XisToXis/Velo{time}DanFix/xiccp_5_sigma/PurityEfficiency.txt")
        control = GetVariables(f"/home/user294/Documents/selections/python/Outputs/XisToLambdas/Velo{time}DanFix/xiccpp_5_sigma/WSPACE.root", f"/home/user294/Documents/selections/python/Outputs/XisToLambdas/Velo{time}DanFix/xiccpp_5_sigma/PurityEfficiency.txt")
        calc = Calculate(signal, control)
        rvalue = calc.Run5Rlimit()
        error = calc.Run5RlimitError()
        print(f"Run 5 R Limit for Velo {time} = {rvalue:.4g} \u00B1 {error:.4g}")

