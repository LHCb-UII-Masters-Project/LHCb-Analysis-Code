import os
import time
import subprocess
from os import path, listdir
import sys
import ROOT
from ROOT import TH1D, TChain, TTree, TFile
from multiprocessing import Process

# Inputs
basedir = "/home/user293/Documents/selections/python"
num_range = []
for i in range(0,50,2):
    num_range.append(f"{i}:{i+2}")


#region MERGE TREES
base_path = f"{basedir}/Outputs/XisToLambdas/Tree"
# Sets base path to where trees are expected
OutChain = ROOT.TChain("Outputs")
RunPChain = ROOT.TChain("RunParams")
RunLChain = ROOT.TChain("RunLimits")
RunDChain = ROOT.TChain("RunDiagnostics")
str_chain = []  # List of filepaths for os.removing later
lambdac_hist_sum = None
# Initialises chain for tree, chain for tree names and hist for combining

for numbers in num_range:
    file_path = f"{base_path}{numbers}.root"  # Full path of one relevant file
    counter = 0
    # Temporariliy comented out for while it works
    # while os.path.exists(file_path) == False and counter < 1:
        # Trys to repaeat tree creation twice if can't find it
        #before_colon, after_colon = numbers.split(":")
        #upper = int(after_colon)
        #lower = int(before_colon)
        #print(f"Redoing {lower}:{upper} redo {counter}")
        #redo_id = runThisScriptOnCondor(scriptPath, batchJobName, subJobName=numbers, extraSetupCommands=pre_run, 
        #                          extraArgs=f"{lower} {upper} {run_args}", is_local=local)
        #subprocess.run(['condor_wait', f'{redo_id}.log'])
        #counter += 1
        #time.sleep(3)

    if os.path.exists(file_path):
        # If repeats are successful or it existed to begin with:
        str_chain.append(file_path)
        OutChain.Add(file_path)
        RunPChain.Add(file_path)
        RunLChain.Add(file_path)
        RunDChain.Add(file_path)

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

OutTree = OutChain.CopyTree("xiccpp_mass!=0")
RunPTree = RunPChain.CopyTree("xiccpp_mass!=0")
RunLTree = RunLChain.CopyTree("xiccpp_mass!=0")
RunDTree = RunDChain.CopyTree("xiccpp_mass!=0")
OutTree.SetName("Outputs")
RunPTree.SetName("RunParams")
RunLTree.SetName("RunLimits")
RunDTree.SetName("RunDiagnostics")

# Full output file name given here
output_file = ROOT.TFile(f"{basedir}/Outputs/XisToLambdas/{str(OutTree.GetEntries())}.root", "RECREATE")
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

#endregion MERGE TREES