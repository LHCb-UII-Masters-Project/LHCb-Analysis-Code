#!/bin/bash
export USER="293"
shopt -s expand_aliases
source /cvmfs/lhcb.cern.ch/lib/LbEnv
export LC_ALL=C
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt
export PYTHONPATH=$PYTHONPATH:/disk/homedisk/home/user293/Documents/selections/python/..
cp /disk/homedisk/home/user293/Documents/selections/python/BsReconstructorBatch.py /home/user293/Documents/selections/python/Outputs/BatchOutputs/BatchRun_22-03-25_07:40:11_PID_6510/270:275/.
cd /home/user293/Documents/selections/python/Outputs/BatchOutputs/BatchRun_22-03-25_07:40:11_PID_6510/270:275
 python BsReconstructorBatch.py 270 275 300 200 0 0 Large None | tee /home/user293/Documents/selections/python/Outputs/BatchOutputs/BatchRun_22-03-25_07:40:11_PID_6510/270:275/tempOutputFile.txt
echo "Job completed successfully, deleting temporary output file"
rm /home/user293/Documents/selections/python/Outputs/BatchOutputs/BatchRun_22-03-25_07:40:11_PID_6510/270:275/tempOutputFile.txt
