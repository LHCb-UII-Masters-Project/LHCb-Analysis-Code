#!/bin/bash
export USER="293"
shopt -s expand_aliases
source /cvmfs/lhcb.cern.ch/lib/LbEnv
export LC_ALL=C
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt
export PYTHONPATH=$PYTHONPATH:/disk/homedisk/home/user294/Documents/selections/python/..
cp /disk/homedisk/home/user294/Documents/selections/python/BsReconstructorBatch.py /home/user294/Documents/selections/python/Outputs/BatchOutputs/BatchRun_25-11-24_13:55:26_PID_9116/35:40/.
cd /home/user294/Documents/selections/python/Outputs/BatchOutputs/BatchRun_25-11-24_13:55:26_PID_9116/35:40
 python BsReconstructorBatch.py 35 40 300 200 0 0 Small None | tee /home/user294/Documents/selections/python/Outputs/BatchOutputs/BatchRun_25-11-24_13:55:26_PID_9116/35:40/tempOutputFile.txt
echo "Job completed successfully, deleting temporary output file"
rm /home/user294/Documents/selections/python/Outputs/BatchOutputs/BatchRun_25-11-24_13:55:26_PID_9116/35:40/tempOutputFile.txt
