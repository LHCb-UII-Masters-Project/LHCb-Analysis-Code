#!/bin/bash
export USER="293"
shopt -s expand_aliases
source /cvmfs/lhcb.cern.ch/lib/LbEnv
export LC_ALL=C
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt
export PYTHONPATH=$PYTHONPATH:/disk/homedisk/home/user294/Documents/selections/python/..
cp /disk/homedisk/home/user294/Documents/selections/python/BsReconstructorBatch.py /home/user294/Documents/selections/python/Outputs/BatchOutputs/BatchRun_25-11-24_13:49:08_PID_2268/20:25/.
cd /home/user294/Documents/selections/python/Outputs/BatchOutputs/BatchRun_25-11-24_13:49:08_PID_2268/20:25
 python BsReconstructorBatch.py 20 25 300 50 1 1 Small None | tee /home/user294/Documents/selections/python/Outputs/BatchOutputs/BatchRun_25-11-24_13:49:08_PID_2268/20:25/tempOutputFile.txt
echo "Job completed successfully, deleting temporary output file"
rm /home/user294/Documents/selections/python/Outputs/BatchOutputs/BatchRun_25-11-24_13:49:08_PID_2268/20:25/tempOutputFile.txt