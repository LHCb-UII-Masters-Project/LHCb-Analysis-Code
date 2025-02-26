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
import argparse

parser = argparse.ArgumentParser(description='Open multiple ROOT files and process data.')
parser.add_argument('workspace_file_signal', type=str, help='Paths to the signal workspace')
parser.add_argument('efficiency_file_signal', type=str, help='Paths to the signal efficiencyPurity,txt file')
parser.add_argument('workspace_file_control', type=str, help='Paths to the control workspace')
parser.add_argument('efficiency_file_control', type=str, help='Paths to the control efficiencyPurity,txt file')
args = parser.parse_args()
input_directory = os.path.dirname(args.workspace_file_signal)

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
        self.nbkg = self.w["nbkg"].getVal()
        self.nbkg_error_low = self.w["nbkg"].getErrorLo()
        self.nbkg_error_high = self.w["nbkg"].getErrorHi()
    
    class Calculate:
        def __init__(self, signal, control):
            self.signal = signal
            self.control = control
            
            self.run2_nsig = 1
            self.run2_nsig_error = 1
            self.run2_efficiency = 1
            self.run2_nbkg = 1
            self.run2_nbkg_error = 1
            
            self.acceptance_control = 1
            self.acceptance_control_error = 1
            self.acceptance_signal = 1
            self.acceptance_signal_error = 1

            self.Run2Luminosity = 1
            self.Run5Luminosity = 1
            
            def CorrectedSignal(self):
                return (self.signal.nsig / (self.signal.efficiency*self.acceptance_signal))
            
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

if __name__ == "__main__":
    signal =  GetVariables(args.workspace_file_signal, args.efficiency_file_signal)
    control = GetVariables(args.workspace_file_control, args.efficiency_file_control),

