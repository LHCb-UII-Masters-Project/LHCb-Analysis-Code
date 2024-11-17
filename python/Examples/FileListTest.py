import os
import time
import subprocess
from os import path, listdir
import sys
import ROOT
from ROOT import TH1D, TChain, TTree, TFile
from multiprocessing import Process
import re

basedir=path.dirname(path.realpath(__file__))
sys.path.insert(0,basedir)
dir= "/disk/moose/lhcb/djdt/u2_globopt/Beam7000GeV-md100-nu38-VerExtAngle_vpOnly/13264021/VP_U2_ParamModel-SX/SX_10um50s_75umcylindr3p5_nu38_Bs2Dspi_2111/moore/"
onlyfiles = [f for f in listdir(dir) if path.isfile(path.join(dir, f))]

pattern = r"U2Tuple_u2_250um_4d-(\d+)-SX_10um\d+s_75umcylindr3p5_nu38_Bs2Dspi_\d+\.root"

# Process the filenames
onlyfileslive = []
for filename in onlyfiles:
    match = re.match(pattern, filename)
    if match:
        onlyfileslive.append(filename)  # Extract the number and convert to integer

print(len(onlyfileslive))
