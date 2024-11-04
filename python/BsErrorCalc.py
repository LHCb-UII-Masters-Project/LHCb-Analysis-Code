#region IMPORTS
import ROOT
from Selections import load_event_library
load_event_library()
from ROOT import uParticle
from ROOT import TFile, gSystem, gInterpreter
from ROOT import TH1D, TH2D, TCanvas, TChain, TTree, TString, TFile
import time
from math import * 
import pandas as pd
import sys
import numpy as np
from os import path, listdir
import os
from array import array

tree_file = ROOT.TFile.Open("t=300/PID1/BsReconstructor_v1_TreeSize2000_Seed_1.7839683789066355e+24_04-11-24_13:34:09.root", "READ")

tree = tree_file.Get("Tree")
max = tree.GetMaximum("file_number")
for i in range(1,int(tree.GetMaximum("file_number"))+1):
    print(i)
    tree.Draw("bs_mass >> hist", f"file_number=={i}")
