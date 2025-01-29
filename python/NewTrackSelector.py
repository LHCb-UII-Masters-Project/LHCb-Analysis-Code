import ROOT
from Selections import load_event_library
load_event_library()
from ROOT import uParticle
from ROOT import TFile, gSystem, gInterpreter
from ROOT import TH1D, TH2D, TCanvas, TChain
from math import * 
import sys
from os import path, listdir 
import numpy as np
import csv

particle_dict = {
  "Kaon":321,
  "Pion":211,
  "Proton":2212,
  "lambdac":4122,
  "xicc++":4222,
  "xicc+":4212,
  "xic+": 4232}

if path.dirname(path.realpath(__file__))[-6:] == "python": # Checks if path ends in "python"
  basedir=path.dirname(path.realpath(__file__))
  sys.path.append(f"{path.dirname(path.realpath(__file__))}/..")
  batching = False
  sys.path.insert(0,basedir)
else:
  basedir = f"{path.dirname(path.realpath(__file__))}/../../../.."
  sys.path.append(f"{path.dirname(path.realpath(__file__))}/../../../..")
  sys.path.insert(0,f"{basedir}/../../..")
  batching = True

def get_arg(index, default, args):  # Arg function that returns relevant arguments and deals with missing args
    try:
        return int(args[index])
    except (IndexError, ValueError, TypeError):
        return default
args = sys.argv
num_files = get_arg(1, 5, args)
min_pt = get_arg(2, 200, args)
min_p = get_arg(3, 1500, args)
min_ipChi2_4d = float(args[4])

from MCTools import * 
gInterpreter.AddIncludePath( f'{basedir}/../include')
gSystem.Load( f'{basedir}/../build/libEvent.so') # add the event library to the python path

events = TChain("Events") # connects all the events into a single data set

# can be changed to look at different timing resolutions and detector geometries
dir=f"/disk/moose/lhcb/djdt/photonics/stackNov24/masters_XiccTest/largeRun_Xicc++/sym/"
onlyfiles = [f for f in listdir(dir) if path.isfile(path.join(dir, f))]

xiccpp_total_true_number = 0
xiccpp_true_tracks = 0
xiccpp_total_tracks = 0
xiccpp_background_tracks = 0


pion_true_tracks = 0
xiccpp_true_pion_tracks =0
xiccpp_pion_tracks = 0
pion_background_tracks = 0

kaon_true_tracks = 0
xicpp_true_kaon_tracks = 0
xiccpp_kaon_tracks = 0
kaon_background_tracks= 0

for i in range(num_files):
  events.AddFile( path.join(dir, onlyfiles[i]) )  # Look at a file in the target directory for analysis

for event in events: # loop through all events
   xiccpp_true_number = [track for track in event.Particles if abs(track.trueID) == particle_dict['xicc++']]
   true_xiccpp = [track for track in event.Particles if is_from(track,event,particle_dict['xicc++'])]
   displaced_tracks = ROOT.select( event.Particles, event.Vertices, min_pt, min_p,min_ipChi2_4d) # select particles, verticies, min_pt, min_p,min_ipChi2_4d
   xiccpp_tracks = [ track for track in displaced_tracks if is_from(track,event,particle_dict['xicc++'])] # all proton^
   background_tracks = [ track for track in displaced_tracks if not is_from(track,event,particle_dict['xicc++'])]
   
   true_pions = [track for track in event.Particles if abs(track.trueID) == particle_dict['Pion']]
   true_xiccpp_pions = [track for track in true_pions if is_from(track,event,particle_dict['xicc++'])]
   pions = [ track for track in ROOT.select( event.Particles, event.Vertices, min_pt, min_p, min_ipChi2_4d ) if  abs(track.trueID) == particle_dict['Pion']]
   xiccpp_pions = [ track for track in pions if is_from(track,event,particle_dict['xicc++'])] # all proton^
   pion_background = [ track for track in pions if not is_from(track,event,particle_dict['xicc++'])] # all proton^

   true_kaons = [track for track in event.Particles if abs(track.trueID) == particle_dict['Kaon']]
   true_xiccpp_kaons = [track for track in true_kaons if is_from(track,event,particle_dict['xicc++'])]
   kaons = [ track for track in ROOT.select( event.Particles, event.Vertices, min_pt, min_p, min_ipChi2_4d ) if  abs(track.trueID) == particle_dict['Kaon']] # needs changing from bs to xi limits
   xiccpp_kaons = [ track for track in kaons if is_from(track,event,particle_dict['xicc++'])] # all proton^
   kaon_background = [ track for track in kaons if not  is_from(track,event,particle_dict['xicc++'])] # all proton^

   xiccpp_total_true_number += len(xiccpp_true_number)
   xiccpp_true_tracks += len(true_xiccpp)
   xiccpp_total_tracks += len(xiccpp_tracks)
   xiccpp_background_tracks += len(background_tracks)
   
   pion_true_tracks += len(true_pions)
   xiccpp_true_pion_tracks += len(true_xiccpp_pions)
   xiccpp_pion_tracks += len(xiccpp_pions)
   pion_background_tracks += len(pion_background)
   
   kaon_true_tracks += len(true_kaons)
   xicpp_true_kaon_tracks += len(true_xiccpp_kaons)
   xiccpp_kaon_tracks += len(xiccpp_kaons)
   kaon_background_tracks += len(kaon_background)

data = [num_files, 
        min_pt,
          min_p,
            min_ipChi2_4d, 
           
            xiccpp_total_true_number,
              xiccpp_true_tracks, 
              xiccpp_total_tracks, 
              xiccpp_background_tracks, 
              
              pion_true_tracks, 
              xiccpp_true_pion_tracks, 
              xiccpp_pion_tracks, 
              pion_background_tracks,
              
              kaon_true_tracks,
              xicpp_true_kaon_tracks,
              xiccpp_kaon_tracks,
              kaon_background_tracks
              ]


# Filepath for the CSV file
file_path = f"{basedir}/Outputs/TrackSelection/LambdacCompIP{min_ipChi2_4d}.csv"
#file_path = f"test.csv"


# Check if the file exists
file_exists = path.isfile(file_path)

# Open the file in append mode
with open(file_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    
    # Write header only if the file doesn't exist
    if not file_exists:
        writer.writerow(["NumFiles", 
                         "MinPT", 
                         "MinP", 
                         "MinIPChi2", 
                         "#1.TotalTrueXiccpp", 
                         "#1.TotalTrueXiccppTracks", 
                         "#1.TotalXiccppTracks",
                         "#1.TotalBackgroundTracks", 
                         "#2.TotalTruePions", 
                         "#2.TotalTrueXiccppPions",
                         "#2.TotalXiccppPions",
                         "#2.TotalBackgroundPions",
                         "#3.TotalTrueKaons",
                         "#3.TotalTrueXiccppKaons",
                         "#3.TotalXiccppKaons",
                         "#3.TotalBackgroundKaons"])
    
    # Append the data
    writer.writerow(data)




