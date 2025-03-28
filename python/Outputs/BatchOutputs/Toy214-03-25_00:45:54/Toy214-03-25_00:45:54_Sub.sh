#!/bin/bash
export USER="293"
shopt -s expand_aliases
source /cvmfs/lhcb.cern.ch/lib/LbEnv
export LC_ALL=C
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt
export PYTHONPATH=$PYTHONPATH:/home/user293/Documents/selections/python/..
cp /home/user293/Documents/selections/python/Fit/CrystalBall/Significance/Toy2.py /home/user293/Documents/selections/python/Outputs/BatchOutputs/Toy214-03-25_00:45:54/.
cd /home/user293/Documents/selections/python/Outputs/BatchOutputs/Toy214-03-25_00:45:54
 python Toy2.py ['source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt', 'export PYTHONPATH=$PYTHONPATH:/home/user293/Documents/selections/python/..'] | tee /home/user293/Documents/selections/python/Outputs/BatchOutputs/Toy214-03-25_00:45:54/tempOutputFile.txt
echo "Job completed successfully, deleting temporary output file"
rm /home/user293/Documents/selections/python/Outputs/BatchOutputs/Toy214-03-25_00:45:54/tempOutputFile.txt
