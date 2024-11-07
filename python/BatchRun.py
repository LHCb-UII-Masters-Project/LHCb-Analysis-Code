import os
import time
import subprocess


def runThisScriptOnCondor(scriptPath,batchJobName,extraArgs="",subJobName=None,
                            launchEnv="",extraSetupCommands = [],
                            condorSettings={"request_memory":"4000"},delayStart=None):
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
    jobDir = f"/home/user293/Documents/selections/python/BatchOutputs/{batchJobName}{f'/{subJobName}' if subJobName is not None else ''}"

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

    subprocess.Popen(f'cd {subScript[:subScript.rfind("/")]} ; chmod +x {subScript} ; /usr/local/bin/condor_submit {condorScript}',shell=True)

    time.sleep(3) #try to fix concurrency problem?

scriptPath = "/home/user293/Documents/selections/python/BsReconstructor.py"
batchJobName = "BatchRun_" + time.strftime("%d-%m-%y_%H:%M:%S", time.localtime())

pre_run = ["source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt", "export PYTHONPATH=$PYTHONPATH:/home/user293/Documents/selections"]
runThisScriptOnCondor(scriptPath, batchJobName, extraSetupCommands=pre_run)