# Upgrade2Selections

For experiments with Upgrade 2 selections using timing for VELO + ECAL. 


## Installation

To build the event library: 
```
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_101 x86_64-centos7-gcc10-opt ## any relatively recent environment should also be fine
cmake -B build
cmake --build build -j 10
```
Then to load the library from python, make sure that the build directory is included in the python path, so 
```
export PYTHONPATH=$PYTHONPATH:$HOME/Selections/build
```
and somewhere near the beginning of files that use these files, include the lines 
```
from Selections import load_event_library
load_event_library()
```

For example usage see python/BtoKpigamma.py

## 4D reconstruction 
To enable the `4D' reconstruction of secondary vertices, the library must be built with the RECO4D flag enabled, i.e. at the cmake step 

```
cmake -B build --DRECO4D=1
```
## Euan's Contribution
<i>Hello World\<i>

