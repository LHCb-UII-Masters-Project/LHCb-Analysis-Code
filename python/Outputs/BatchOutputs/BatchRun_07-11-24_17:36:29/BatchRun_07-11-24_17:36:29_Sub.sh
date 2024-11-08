#!/bin/bash
export USER="293"
shopt -s expand_aliases
source /cvmfs/lhcb.cern.ch/lib/LbEnv
export LC_ALL=C
cd /home/user293/Documents/selections/python
rm -rf build
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt
cmake -B build
cmake --build build -j 5
cd python
export PYTHONPATH=$PYTHONPATH:/home/user293/Documents/selections
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt
cp /home/user293/Documents/selections/python/BsReconstructor.py /home/user293/Documents/selections/python/BatchOutputs/BatchRun_07-11-24_17:36:29/.
cd /home/user293/Documents/selections/python/BatchOutputs/BatchRun_07-11-24_17:36:29
 python BsReconstructor.py  | tee /home/user293/Documents/selections/python/BatchOutputs/BatchRun_07-11-24_17:36:29/tempOutputFile.txt
echo "Job completed successfully, deleting temporary output file"
rm /home/user293/Documents/selections/python/BatchOutputs/BatchRun_07-11-24_17:36:29/tempOutputFile.txt
