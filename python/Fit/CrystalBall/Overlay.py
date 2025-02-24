import ROOT
from Variables.Exp import variables, fit_initial_guess_tree
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
from Overlay.functions import ListFill as ListFill
from Overlay.functions import DataAndModels as DataAndModels
from Overlay.functions import Data as Data
from Overlay.functions import Models as Models
from Overlay.functions import Backgrounds as Backgrounds
from Overlay.functions import Signals as Signals




#-----------------------------MODE SELECTION AND INPUTS------------------------------------
parser = argparse.ArgumentParser(description='Open multiple ROOT files and process data.')
# Accept one or more input files
parser.add_argument('input_files', type=str, nargs='+', help='Paths to the input ROOT files')
parser.add_argument('--timings', type=float, nargs='+', help='List of timings')
args = parser.parse_args()
timings = args.timings
models = []
data_sets = []
x_models = []
nbkgs = []
nsigs = []
bkgs = []
dummy_objects = []

directory_path = f"/home/user294/Documents/selections/python/Fit/Comparison/Overlays/{timings}wide_range"
os.makedirs(directory_path, exist_ok=True)

ListFill(args.input_files,models,data_sets,x_models)
DataAndModels(x_models,models,data_sets,timings,dummy_objects,10,directory_path,"xiccp")
Data(x_models,models,data_sets,timings,dummy_objects,10,directory_path,"xiccpp")
Models(x_models,models,data_sets,timings,dummy_objects,10,directory_path,"xiccpp")
Backgrounds(x_models,models,data_sets,timings,dummy_objects,10,directory_path,"xiccpp")
Signals(x_models,models,data_sets,timings,dummy_objects,10,directory_path,"xiccpp")