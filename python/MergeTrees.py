import os
import time
import subprocess
from os import path, listdir
import sys
import ROOT
from ROOT import TH1D, TChain, TTree, TFile
from multiprocessing import Process

from os import listdir
from os.path import isfile, join
# Inputs
basedir = "/home/user294/Documents/selections/python"
num_range = []
for i in range(0,500,5):
    num_range.append(f"{i}:{i+5}")


#region MERGE TREES
base_path = "/home/user294/Documents/selections/python/Outputs/XisToLambdas/MergeZone"
# Sets base path to where trees are expected
OutChain = ROOT.TChain("Outputs")
RunPChain = ROOT.TChain("RunParams")
RunLChain = ROOT.TChain("RunLimits")
RunDChain = ROOT.TChain("RunDiagnostics")
str_chain = []  # List of filepaths for os.removing later
lambdac_hist_sum = None
# Initialises chain for tree, chain for tree names and hist for combining
onlyfiles = [join(base_path, f) for f in listdir(base_path) if isfile(join(base_path, f)) and f.endswith('.root')]
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
        """
        # Open each file separately to retrieve the histogram
        f = ROOT.TFile.Open(file_path, "READ")
        lambdac_hist = f.Get("Lambdac_Histogram")
        lambdac_hist.SetDirectory(0)
        f.Close()

        if lambdac_hist_sum is None:
            lambdac_hist_sum = lambdac_hist.Clone("hist")
            lambdac_hist_sum.SetDirectory(0)
        else:
            lambdac_hist_sum.Add(lambdac_hist)
            lambdac_hist_sum.SetDirectory(0)
        """

## f"hadd {longFILENAME} {' '.join(str_chain)}"    
import ROOT
import csv


# Dictionary to store the cumulative sum for each branch.
# We'll initialize it once we see the first valid tree.
branch_sums = {}

for file_name in onlyfiles:
    # Open the ROOT file
    root_file = ROOT.TFile.Open(file_name)
    
    # Retrieve the tree
    diagnostics = root_file.Get("RunDiagnostics")
    
    # Check if the tree is valid and has entries
    if diagnostics and diagnostics.GetEntries() > 0:
        n_entries = diagnostics.GetEntries()
        # Move to the last entry of the tree
        diagnostics.GetEntry(n_entries - 1)
        
        # Loop over all branches in this tree
        for branch in diagnostics.GetListOfBranches():
            branch_name = branch.GetName()
            value = getattr(diagnostics, branch_name)
            
            # Initialize the sum for this branch if it's the first time
            if branch_name not in branch_sums:
                branch_sums[branch_name] = 0
                
            # Add the value from the last entry of this tree
            branch_sums[branch_name] += value
    else:
        print(f"Tree 'RunDiagnostics' is empty or not found in {file_name}")
    
    # Close the ROOT file
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
output_file = ROOT.TFile(f'{basedir}/Outputs/XisToLambdas/TS_{str(OutTree.GetEntries())}_Time_{time.strftime("%d-%m-%y_%H:%M:%S", time.localtime())}.root', "RECREATE")
# Writes to the output file
output_file.cd()
OutTree.Write("Outputs")
RunPTree.Write("RunParams")
RunLTree.Write("RunLimits")
RunDTree.Write("RunDiagnostics")
# lambdac_hist_sum.Write("Lambdac_Histogram")

# Close the output file
output_file.Write()
output_file.Close()

# Deletes the trees that made up the now combined tree
#for file_path in str_chain:
    #os.remove(file_path)

print(f"Made Tree")

end_time = time.time()

# Write the summed results to a CSV file
csv_filename = f'{basedir}/Outputs/XisToLambdas/TS_{str(OutTree.GetEntries())}_Time_{time.strftime("%d-%m-%y_%H:%M:%S", time.localtime())}_Counters.csv'
with open(csv_filename, mode="w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=branch_sums.keys())
    writer.writeheader()         # Write header row with branch names
    writer.writerow(branch_sums)   # Write the summed values what have I done wrong with my file writing 