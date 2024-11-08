#!/bin/bash
export USER="293"
shopt -s expand_aliases
source /cvmfs/lhcb.cern.ch/lib/LbEnv
export LC_ALL=C
export PYTHONPATH=$PYTHONPATH:/home/user293/Documents/selections
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt
cp /home/user293/Documents/selections/python/TestRun.py /home/user293/Documents/selections/python/BatchOutputs/Test_07-11-24_12:57:28/.
cd /home/user293/Documents/selections/python/BatchOutputs/Test_07-11-24_12:57:28
 python TestRun.py  | tee /home/user293/Documents/selections/python/BatchOutputs/Test_07-11-24_12:57:28/tempOutputFile.txt
echo "Job completed successfully, deleting temporary output file"
rm /home/user293/Documents/selections/python/BatchOutputs/Test_07-11-24_12:57:28/tempOutputFile.txt
