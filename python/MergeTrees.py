import os
import time
import subprocess
from os import path, listdir
import sys
import ROOT
from ROOT import TH1D, TChain, TTree, TFile
from multiprocessing import Process
from collections import defaultdict
import csv
import pandas as pd

from os import listdir
from os.path import isfile, join
# Inputs
basedir = "/home/user293/Documents/selections/python"
num_range = []
for i in range(0,1000,5):
    num_range.append(f"{i}:{i+5}")
base_path = "/home/user293/Documents/selections/python/Outputs/XisToLambdas"
merge = "csv"

if merge == "tree":
    #region MERGE TREES
    # Sets base path to where trees are expected
    OutChain = ROOT.TChain("Outputs")
    RunPChain = ROOT.TChain("RunParams")
    RunLChain = ROOT.TChain("RunLimits")
    RunDChain = ROOT.TChain("RunDiagnostics")
    str_chain = []  # List of filepaths for os.removing later
    lambdac_hist_sum = None
    # Initialises chain for tree, chain for tree names and hist for combining
    onlyfiles = [join(base_path, f) for f in listdir(base_path) if isfile(join(base_path, f)) and f.endswith('Velo100.root')]
    for file_path in onlyfiles:

        if os.path.exists(file_path):
            # If repeats are successful or it existed to begin with:
            str_chain.append(file_path)
            OutChain.Add(file_path)
            RunPChain.Add(file_path)
            RunLChain.Add(file_path)
            RunDChain.Add(file_path)


            root_file = ROOT.TFile.Open(file_path, "READ") 
            diagnostics = root_file.Get("RunDiagnostics")
            diagnostics.SetDirectory(0)
            root_file.Close()

    OutTree = OutChain.CopyTree("")
    RunPTree = RunPChain.CopyTree("")
    RunLTree = RunLChain.CopyTree("")
    RunDTree = RunDChain.CopyTree("")
    OutTree.SetName("Outputs")
    RunPTree.SetName("RunParams")
    RunLTree.SetName("RunLimits")
    RunDTree.SetName("RunDiagnostics")

    # Full output file name given here
    output_file = ROOT.TFile(f'{basedir}/Outputs/XisToLambdas/TS_{str(OutTree.GetEntries())}_Time_{time.strftime("%d-%m-%y_%H:%M:%S", time.localtime())}Velo30.root', "RECREATE")
    # Writes to the output file
    output_file.cd()
    OutTree.Write("Outputs")
    RunPTree.Write("RunParams")
    RunLTree.Write("RunLimits")
    RunDTree.Write("RunDiagnostics")

    # Close the output file
    output_file.Write()
    output_file.Close()

    print(f"Made Tree")

elif merge == "csv":
    counters = defaultdict(lambda: {"sig_kills": 0, "bkg_kills": 0, "sig_remains": 0, "bkg_remains": 0})
    csv_list = []
    onlyfiles = [join(base_path, f) for f in listdir(base_path) if isfile(join(base_path, f)) and f.endswith('Velo30.csv')]
    for filename in onlyfiles:
        csv_list.append(filename)
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)  # Reads CSV as a dictionary
            for row in reader:
                key = row["cut"]
                counters[key]["sig_kills"] += int(row["sig_kills"])
                counters[key]["bkg_kills"] += int(row["bkg_kills"])
                counters[key]["sig_remains"] += int(row["sig_remains"])
                counters[key]["bkg_remains"] += int(row["bkg_remains"])

    # Write the combined results to a new CSV file
    csv_filename = f"CountersVelo30.csv"
    df = pd.DataFrame.from_dict(counters, orient="index")
    df.reset_index(inplace=True)
    df.rename(columns={"index": "cut", "sig_kills": "sig_kills", "bkg_kills": "bkg_kills", "sig_remain": "sig_remains", "bkg_remain": "bkg_remains"}, inplace=True)
    df.to_csv(csv_filename, index=False)

    print("Made CSV")