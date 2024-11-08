#!/bin/bash
export USER="293"
shopt -s expand_aliases
source /cvmfs/lhcb.cern.ch/lib/LbEnv
export LC_ALL=C
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt
export PYTHONPATH=$PYTHONPATH:/home/user293/Documents/selections
cp /home/user293/Documents/selections/python/BsReconstructor.py /home/user293/Documents/selections/python/BatchOutputs/BatchRun_07-11-24_18:06:25/.
cd /home/user293/Documents/selections/python/BatchOutputs/BatchRun_07-11-24_18:06:25
 python BsReconstructor.py  | tee /home/user293/Documents/selections/python/BatchOutputs/BatchRun_07-11-24_18:06:25/tempOutputFile.txt
echo "Job completed successfully, deleting temporary output file"
rm /home/user293/Documents/selections/python/BatchOutputs/BatchRun_07-11-24_18:06:25/tempOutputFile.txt
