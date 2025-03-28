#!/bin/bash
export USER="293"
shopt -s expand_aliases
source /cvmfs/lhcb.cern.ch/lib/LbEnv
export LC_ALL=C
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt
export PYTHONPATH=$PYTHONPATH:/disk/homedisk/home/user293/Documents/selections/python/..
cp /disk/homedisk/home/user293/Documents/selections/python/BsReconstructorBatch.py /home/user293/Documents/selections/python/Outputs/BatchOutputs/BatchRun_22-03-25_07:40:11_PID_6508/290:295/.
cd /home/user293/Documents/selections/python/Outputs/BatchOutputs/BatchRun_22-03-25_07:40:11_PID_6508/290:295
 python BsReconstructorBatch.py 290 295 300 50 0 0 Large None | tee /home/user293/Documents/selections/python/Outputs/BatchOutputs/BatchRun_22-03-25_07:40:11_PID_6508/290:295/tempOutputFile.txt
echo "Job completed successfully, deleting temporary output file"
rm /home/user293/Documents/selections/python/Outputs/BatchOutputs/BatchRun_22-03-25_07:40:11_PID_6508/290:295/tempOutputFile.txt
