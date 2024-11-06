#!/bin/bash
export USER="293"
shopt -s expand_aliases
source /cvmfs/lhcb.cern.ch/lib/LbEnv
export LC_ALL=C
cp /home/user293/Documents/selections/python/TestRun.py /home/user293/Documents/selections/python/BatchOutputs/Test_06-11-24_13:27:36/.
cd /home/user293/Documents/selections/python/BatchOutputs/Test_06-11-24_13:27:36
['export PYTHONPATH=$PYTHONPATH:/home/user293/Documents/selections/build', 'source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt'] python TestRun.py  | tee /home/user293/Documents/selections/python/BatchOutputs/Test_06-11-24_13:27:36/tempOutputFile.txt
echo "Job completed successfully, deleting temporary output file"
rm /home/user293/Documents/selections/python/BatchOutputs/Test_06-11-24_13:27:36/tempOutputFile.txt
