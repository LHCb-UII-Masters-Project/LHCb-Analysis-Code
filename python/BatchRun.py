import os
import time
import subprocess
from os import path, listdir
import sys
import ROOT
from ROOT import TH1D, TChain, TTree, TFile
from multiprocessing import Process


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
        # If running locally, must use ret instead of condor_wait
        ret = subprocess.Popen(f'cd {subScript[:subScript.rfind("/")]} ; chmod +x {subScript} ; exec {subScript}',shell=True)
        time.sleep(3) #try to fix concurrency problem?
        return ret
    else:
        subprocess.Popen(f'cd {subScript[:subScript.rfind("/")]} ; chmod +x {subScript} ; /usr/local/bin/condor_submit {condorScript}',shell=True)
        time.sleep(3) #try to fix concurrency problem?
        return condorOut
    
def macro_batch(program="Run", comp="Local", size="Small", files_per_run=2, tot_num_files=4, rich_timing=300, 
                velo_time=50, pid_switch=1, kaon_switch=1, rand_seed=None):
    """
    Function that can be called by a procces in order to run multiple combinations of arguments simultaneously

    Parameters:
    program - Run or Test, Run is default and Test can be used to check on condor
    comp - Local or NonLocal, determines where the files are run
    size - Large or Small determines where the event files are pulled from (large or small store)
    files_per_run - Number of files allocated to each condor core
    tot_num_files - Total number of files to be run per combination of parameters
    et al. - Parameters for BsReconstructorBatch
    """

    start_time = time.time()  # Starts a timer for outputing
    basedir=path.dirname(path.realpath(__file__))
    sys.path.append(basedir)
    local = comp == "Local"  # True if Local, False if other


    if program == "Run":
        #region RUN SCRIPT

        # Define arguments for RunThisScript
        scriptPath = f"{basedir}/BsReconstructorBatch.py"
        batchJobName = "BatchRun_" + time.strftime("%d-%m-%y_%H:%M:%S", time.localtime()) + "_PID_" + str(os.getpid())[3:]
        # PID included as batched jobs start at same time
        pre_run = ["source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt", f"export PYTHONPATH=$PYTHONPATH:{basedir}/.."]
        run_args = f"{rich_timing} {velo_time} {pid_switch} {kaon_switch} {size} {rand_seed}"

        wait_id = []  # Holds the return that can be used to make program wait for completion
        num_range = []  # List of strings [0:5, 5:10 ,...]
        for i in range(0,tot_num_files, files_per_run):
            # print(f"{i}:{i+files_per_run}")

            wait_id.append(runThisScriptOnCondor(scriptPath, batchJobName, subJobName=f"{i}:{i+files_per_run}", extraSetupCommands=pre_run, extraArgs=f"{i} {i+files_per_run} {run_args}", is_local=local))
            # Runs with all arguments passed, inlcuding if to run local or on Condor
            num_range.append(f"{i}:{i+files_per_run}")

        if local is True:
            # Uses ret to wait if local
            for index, ret in enumerate(wait_id):
                print(f"Waiting for files {num_range[index]} to be processed...")
                ret.wait()
                time.sleep(1)
        else:
            # Uses condor_wait to wait if on condor
            for index, numbers in enumerate(num_range):
                print(f"Waiting for files {numbers} to be processed...")
                subprocess.run(['condor_wait', f'{wait_id[index]}.log'])
                time.sleep(1)

        #endregion RUN SCRIPT

        #region MERGE TREES
        base_path = f"{basedir}/Outputs/Rich{rich_timing}/PID{pid_switch}/Velo{velo_time}/Tree"
        # Sets base path to where trees are expected
        OutChain = ROOT.TChain("Outputs")
        RunPChain = ROOT.TChain("RunParams")
        RunLChain = ROOT.TChain("RunLimits")
        RunDChain = ROOT.TChain("RunDiagnostics")
        str_chain = []  # List of filepaths for os.removing later
        b_hist_sum = None
        d_hist_sum = None
        # Initialises chain for tree, chain for tree names and hist for combining

        for numbers in num_range:
            file_path = f"{base_path}{numbers}.root"  # Full path of one relevant file
            counter = 0
            while os.path.exists(file_path) == False and counter < 1:
                # Trys to repaeat tree creation twice if can't find it
                before_colon, after_colon = numbers.split(":")
                upper = int(after_colon)
                lower = int(before_colon)
                print(f"Redoing {lower}:{upper} redo {counter}")
                redo_id = runThisScriptOnCondor(scriptPath, batchJobName, subJobName=numbers, extraSetupCommands=pre_run, 
                                          extraArgs=f"{lower} {upper} {run_args}", is_local=local)
                subprocess.run(['condor_wait', f'{redo_id}.log'])
                counter += 1
                time.sleep(3)

            if os.path.exists(file_path):
                # If repeats are successful or it existed to begin with:
                str_chain.append(file_path)
                OutChain.Add(file_path)
                RunPChain.Add(file_path)
                RunLChain.Add(file_path)
                RunDChain.Add(file_path)

                # Open each file separately to retrieve the histogram
                f = ROOT.TFile.Open(file_path, "READ")
                b_hist = f.Get("B_Histogram")
                d_hist = f.Get("B_Histogram")
                b_hist.SetDirectory(0)
                d_hist.SetDirectory(0)
                f.Close()

                if b_hist_sum is None:
                    b_hist_sum = b_hist.Clone("hist")
                    b_hist_sum.SetDirectory(0)
                else:
                    b_hist_sum.Add(b_hist)
                    b_hist_sum.SetDirectory(0)
                if d_hist_sum is None:
                    d_hist_sum = d_hist.Clone("hist")
                    d_hist_sum.SetDirectory(0)
                else:
                    d_hist_sum.Add(d_hist)
                    d_hist_sum.SetDirectory(0)

        ## f"hadd {longFILENAME} {' '.join(str_chain)}"    

        OutTree = OutChain.CopyTree("bs_mass!=0")
        RunPTree = RunPChain.CopyTree("bs_mass!=0")
        RunLTree = RunLChain.CopyTree("bs_mass!=0")
        RunDTree = RunDChain.CopyTree("bs_mass!=0")
        OutTree.SetName("Outputs")
        RunPTree.SetName("RunParams")
        RunLTree.SetName("RunLimits")
        RunDTree.SetName("RunDiagnostics")
        
        # Replicates calling logic for file writing purposes
        pid_combine = 1 if pid_switch == 1 and kaon_switch == 1 else 0

        # Full output file name given here
        output_file = ROOT.TFile(f"{basedir}/Outputs/Rich" + str(rich_timing) + "/PID" + str(pid_combine) + "/Velo" + str(velo_time) + "/TS_" + str(OutTree.GetEntries()) + "_Time_" + time.strftime("%d-%m-%y_%H:%M:%S", time.localtime()) 
                                 + f"Rich{rich_timing}_PID{pid_combine}_Velo{velo_time}_Space10_COM14" + ".root", "RECREATE")
        # Writes to the output file
        output_file.cd()
        OutTree.Write("Outputs")
        RunPTree.Write("RunParams")
        RunLTree.Write("RunLimits")
        RunDTree.Write("RunDiagnostics")
        b_hist_sum.Write("B_Histogram")
        d_hist_sum.Write("D_Histogram")

        # Close the output file
        output_file.Write()
        output_file.Close()

        # Deletes the trees that made up the now combined tree
        for file_path in str_chain:
            os.remove(file_path)
        
        print(f"Made Tree" f"/TS_" + str(OutTree.GetEntries()) + "_Time_" + time.strftime("%d-%m-%y_%H:%M:%S", time.localtime()) 
                                 + f"Rich{rich_timing}_PID{pid_combine}_Velo{velo_time}")

        end_time = time.time()
        
        #endregion MERGE TREES

    elif program == "Test":
        pre_run = ["source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt", f"export PYTHONPATH=$PYTHONPATH:{basedir}/.."]
        runThisScriptOnCondor(f"{basedir}/Inputs/Test.py", "TestRun", extraSetupCommands=pre_run, is_local=local)
        end_time = time.time()

    # Timer output for interest
    time_taken = end_time - start_time
    minutes = int(time_taken // 60)
    seconds = int(time_taken % 60)
    print(f"Time taken: {minutes} minutes and {seconds} seconds")


if __name__ == "__main__":  # Stops the script from running if its imported as a module
    # Inputs for macrobatch
    program = "Run"
    comp = "NonLocal"
    size = "Small"
    files_per_run = 2
    tot_num_files = 6
    rand_seed = None

    #rich_options = [150, 300]
    rich_options = [300]

    # PID_switch = [0,1]
    PID_switch = [1]
    
    # velo_options = [50, 200]
    velo_options = [50]

    # Makes proccesses for all combinations of arguments
    process_store = []
    try:
    # process_store = []
        for rt in rich_options:
            for vt in velo_options:
                for PID in PID_switch:
                    k_switch = 1 if PID == 1 else 0
                    p = Process(target = macro_batch, args = (program, comp, size, files_per_run, tot_num_files, rt, 
                    vt, PID, k_switch, rand_seed))
                    process_store.append(p)
                    time.sleep(1)
                        
        # Starts proccesses and then waits for them to be complete
        for p in process_store:
            p.start()
        for p in process_store:
            p.join()
    
    except KeyboardInterrupt:
        try: 
            for p in process_store:
                p.kill()
            subprocess.run(["condor_rm", "user293"], check=True)
        except NameError:
            print("No Processes to Kill")
