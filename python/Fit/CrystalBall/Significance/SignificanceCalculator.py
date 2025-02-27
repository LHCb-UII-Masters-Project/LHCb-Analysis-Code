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
    def __init__(self, signal, control, user):
        self.signal = signal
        self.control = control
        
        self.run2_nsig = 121+153+188
        self.run2_nsig_error = np.sqrt(19**2 + 22**2 + 24**2)
        self.run2_efficiency = 1.733 * (10**(-4))
        self.run2_efficiency_error = 0.038 * (10**(-4))
        self.run2_nbkg = 1#VALUES NEED UPDATING
        self.run2_nbkg_error = 1#VALUES NEED UPDATING
        
        self.acceptance_control = 0.08888655271274595
        self.acceptance_control_error = 0.000377767084151423

        if user == "Euan":
            self.xiccp_signal_acceptance =  0.09174444698877948
            self.xiccp_signal_acceptance_error = 0.00038853854575107705
            self.run2_efficiency_ratio = (1.17 * 1.7 + 1.91 * 1.7  + 1.99 * 2.2) / (1.17 + 1.91 + 1.99)
            self.run2_efficiency_ratio_error = np.sqrt(((1.7**2)*(0.11**2) + (1.7**2)*(0.11**2) + (2.2**2)*(0.12**2))/(2*(1.7**2)+2.2**2))
            self.run2_r_limit = 1
            self.run2_r_limit_error = 0.1 # If this exists?
        else:
            self.xiccp_signal_acceptance = 0.08432470964835002
            self.xiccp_signal_acceptance_error = 0.0003583034556616932
            self.run2_efficiency_ratio = 1
            self.run2_r_limit = 1
        # not given and not used
        # self.lambdac_signal_acceptance = 1
        # self.lambdac_signal_acceptance_error = 1

        self.Run2Luminosity = 1.7+1.7+2.2
        self.Run5Luminosity = 300 # Check with Dan

        # not given and not used
        self.BkgPvPerEvent = 39 # Guess
        self.BkgPVPerEventError = 39 # Guess
        
    def CorrectedSignal(self):
        return (self.signal.nsig / (self.signal.efficiency*self.xiccp_signal_acceptance))
    
    def CorrectedControl(self):
        return(self.control.nsig / (self.control.efficiency*self.acceptance_control))
    
    def CorrectedRun2(self):
        return(self.run2_nsig / self.run2_efficiency)

    def LuminosityScaleFactor(self):
        return (self.Run5Luminosity/ self.Run2Luminosity)

    def ControlScaleFactor(self):
        return (self.CorrectedControl() / self.CorrectedRun2())
    
    def SimulationR(self):
        return (self.CorrectedSignal() / self.CorrectedControl())
    
    def ScaledR(self):
        return (self.SimulationR() * self.ControlScaleFactor() * self.LuminosityScaleFactor())

    def Alpha(self):
        return (self.ScaledR() / self.signal.nsig)
    
    # 27/2/25

    def Run5EffRatio(self):
        return (self.signal.efficiency / self.control.efficiency)
    
    def Run5Rlimit(self):
        return (self.run2_r_limit / np.sqrt(self.Run5EffRatio() / self.run2_efficiency_ratio))


if __name__ == "__main__":

    velo_timings = [30,50,70,100,200]
    for time in velo_timings:
        signal =  GetVariables(f"/home/user293/Documents/selections/python/Outputs/EuanSignal/Velo{time}/Xi5Sigma/WSPACE.root" , f"/home/user293/Documents/selections/python/Outputs/EuanSignal/Velo{time}/Xi5Sigma/PurityEfficiency.txt")
        control = GetVariables(f"/home/user293/Documents/selections/python/Outputs/XisToLambdas/Velo{time}DanFix/xiccpp_5_sigma/WSPACE.root", f"/home/user293/Documents/selections/python/Outputs/XisToLambdas/Velo200DanFix/xiccpp_5_sigma/PurityEfficiency.txt")
        calc = Calculate(signal, control, user="Euan")
        rvalue = calc.Run5Rlimit()
        print(f"Run 5 R Limit for Velo {time} = {rvalue}")
