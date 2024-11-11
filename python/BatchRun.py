import os
import time
import subprocess
from os import path, listdir
import sys
import ROOT
from ROOT import TH1D, TChain, TTree, TFile


def runThisScriptOnCondor(scriptPath,batchJobName,extraArgs="",subJobName=None,
                            launchEnv="",extraSetupCommands = [],
                            condorSettings={"request_memory":"4000", "request_cpus":"1"},delayStart=None, is_local=False):
    #having created a notebook that we want to run on condor, write a bash file and submit it.
    
    '''
    Instructions:
    This script sets everything up to run condor jobs on python files.

It creates an output directory with given names, writes up an executable that will actually be run by the condor node and then prepares a submission script that launches the job.

Few things to note:
- extraSetupCommands are where your usual source commands should go that make sure you have the right LCG versions etc.
- you may need to request more memory
- you don't need to run the alma9 command, look at the "RequestChroot" section of the code, this sets up the right image.

Parameters:
scriptPath - the full path of the python script you want to run
batchJobName - The top level title for the tests to be run
extraArgs - Space-separated arguments to feed into the python file. These are often file names or special keys that the python script understands what to do with
subJobName - if this job is one of many similar jobs, new directorys will be made under the {batchJobName} directory with this subjobname. e.g subJobName = "SubJob0"
launchEnv - If you want to run the python script with a specific set of commands run before, each line in this list will be run. (This is where to put your ["source /...",] commands)
condorSettings - dictionary of request commands to send to condor, more can be found on the condor docs
delayStart - put this many seconds of delay into the script, sometimes useful if we have concurrency errors
    '''
    
    #will create a general condor out folder that stores all the results and details
    jobDir = f"/home/user293/Documents/selections/python/Outputs/BatchOutputs/{batchJobName}{f'/{subJobName}' if subJobName is not None else ''}"

    os.makedirs(jobDir,exist_ok=True,)
    #now empty dir if there is anything in there!
    
    
    subScript=f"{jobDir}/{batchJobName.replace('/','_')}{('_'+subJobName) if subJobName is not None else ''}_Sub.sh"
    with open(subScript,"w") as f:
        f.write('#!/bin/bash\n')#'#!/cvmfs/lhcbdev.cern.ch/conda/envs/default/2021-06-29_07-31/linux-64/bin/bash\n')
        f.write('export USER="293"\nshopt -s expand_aliases\nsource /cvmfs/lhcb.cern.ch/lib/LbEnv\nexport LC_ALL=C\n')
        for e in extraSetupCommands:
            f.write(e+'\n')
        f.write(f"cp {scriptPath} {jobDir}/.\n")
        f.write(f"cd {jobDir}\n")
        if delayStart is not None:
            f.write(f"echo Sleeping for {delayStart} seconds\n")
            f.write(f"sleep {delayStart}\n")
        f.write(f"{launchEnv} python {scriptPath[scriptPath.rfind('/')+1:]} {extraArgs} | tee {jobDir}/tempOutputFile.txt\n")
        f.write(f'echo "Job completed successfully, deleting temporary output file"\n')
        f.write(f"rm {jobDir}/tempOutputFile.txt\n")

    condorScript=f"{jobDir}/{batchJobName.replace('/','_')}_condor.cndr"
    condorOut=f"{jobDir}/{batchJobName.replace('/','_')}{('_'+subJobName) if subJobName is not None else ''}"
    
    for a in ["o","e","log"]:
        if os.path.exists(condorOut+"."+a):
            os.remove(condorOut+"."+a)
    
    with open(condorScript,"w") as f:
        f.write(f'Executable = {subScript}\n')
        f.write(f'output = {condorOut}.o\nerror = {condorOut}.e\nlog = {condorOut}.log\n')
        f.write('getenv = True\n')
        for a,b in condorSettings.items():
            f.write(f"{a} = {b}\n")
        f.write('+SingularityImage = "/image/alma9-image"\n')
        # f.write('+RequestedChroot="cc7"\n' if not turnOffCC7 else '')
        f.write("queue\n")

    if is_local is True:
        ret = subprocess.Popen(f'cd {subScript[:subScript.rfind("/")]} ; chmod +x {subScript} ; exec {subScript}',shell=True)
        time.sleep(3) #try to fix concurrency problem?
        return ret
    else:
        subprocess.Popen(f'cd {subScript[:subScript.rfind("/")]} ; chmod +x {subScript} ; /usr/local/bin/condor_submit {condorScript}',shell=True)
        time.sleep(3) #try to fix concurrency problem?
        return condorOut
    
    

basedir=path.dirname(path.realpath(__file__))
sys.path.append(basedir)
args = sys.argv

if args[1] == "Run":
    local = False
    files_per_run = int(args[2])
    tot_num_files = int(args[3])
    scriptPath = f"{basedir}/BsReconstructorBatch.py"
    batchJobName = "BatchRun_" + time.strftime("%d-%m-%y_%H:%M:%S", time.localtime())
    pre_run = ["source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt", f"export PYTHONPATH=$PYTHONPATH:{basedir}/.."]

    log_id = []
    num_range = []
    for i in range(0,tot_num_files, files_per_run):
        # print(f"{i}:{i+files_per_run}")

        log_id.append(runThisScriptOnCondor(scriptPath, batchJobName, subJobName=f"{i}:{i+files_per_run}", extraSetupCommands=pre_run, extraArgs=f"{i} {i+files_per_run}", is_local=local))
        num_range.append(f"{i}:{i+files_per_run}")

    final_files = log_id[len(log_id)-1:][0]
    final_numbers = num_range[len(num_range)-1:][0]
    if local is True:
        for index, ret in enumerate(log_id):
            print(f"Waiting for files {num_range[index]} to be processed...")
            ret.wait()
            # time.sleep(3)
    else:
        for index, numbers in enumerate(num_range):
            print(f"Waiting for files {numbers} to be processed...")
            subprocess.run(['condor_wait', f'{log_id[index]}.log'])
    
    timing = 150
    pid_switch = 1

    base_path = f"{basedir}/Outputs/t=150/PID1/Tree" #  Fix me!
    # output_file = ROOT.TFile("MergedOutput.root", "RECREATE")

    chain = ROOT.TChain("Tree")
    hist_sum = None

    for numbers in num_range:
        file_path = f"{base_path}{numbers}.root"
        # print(file_path)
        chain.Add(file_path)

        # Open each file separately to retrieve the histogram
        f = ROOT.TFile.Open(file_path, "READ")
        hist = f.Get("B_Histogram")
        hist.SetDirectory(0)
        f.Close()

        if hist_sum is None:
            hist_sum = hist.Clone("hist")
            hist_sum.SetDirectory(0)
        else:
            hist_sum.Add(hist)
            hist_sum.SetDirectory(0)


    

    # Merge the TTrees
    merge_tree = chain.CopyTree("", "")
    merge_tree.SetName("Tree")
    
    

    output_file = ROOT.TFile(f"{basedir}/Outputs/t=" + str(timing) + "/PID" + str(pid_switch) + "/TreeSize" + str(merge_tree.GetEntries()) + time.strftime("%d-%m-%y_%H:%M:%S", time.localtime()) + ".root", "RECREATE")
    output_file.cd()

    merge_tree.Write("Tree")
    hist_sum.Write()

    # Close the output file
    output_file.Write()
    output_file.Close()

    print("Merged TTrees and TH1D histograms")

elif args[1] == "Test":
    pre_run = ["source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt", f"export PYTHONPATH=$PYTHONPATH:{basedir}/.."]
    runThisScriptOnCondor(f"{basedir}/Inputs/Test.py", "TestRun", extraSetupCommands=pre_run)
