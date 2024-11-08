CMake Error: The source directory "/home/user293/Documents/selections/python" does not appear to contain CMakeLists.txt.
Specify --help for usage, or press the help button on the CMake GUI.
Error: /home/user293/Documents/selections/python/build is not a directory
/var/lib/condor/execute/dir_3238120/BatchRun_07-11-24_17:36:29_Sub.sh: line 11: cd: python: No such file or directory
Traceback (most recent call last):
  File "/disk/homedisk/home/user293/Documents/selections/python/BatchOutputs/BatchRun_07-11-24_17:36:29/BsReconstructor.py", line 190, in <module>
    from MCTools import * 
  File "/cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc12-opt/lib/ROOT/_facade.py", line 154, in _importhook
    return _orig_ihook(name, *args, **kwds)
ModuleNotFoundError: No module named 'MCTools'
