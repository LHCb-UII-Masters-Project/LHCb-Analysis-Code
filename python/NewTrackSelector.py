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
#dir="/disk/moose/lhcb/djdt/photonics/stackNov24/masters_XiccTest/largeRun_Xicc++/sym/"
dir="/disk/moose/lhcb/djdt/photonics/stackNov24/masters_XiccTest/largeRun_Xicc++/sym_10um50ps/"  # 4D on
onlyfiles = [f for f in listdir(dir) if path.isfile(path.join(dir, f))]

xiccpp_total_true_number = 0
xiccpp_true_tracks = 0
xilc_true_daughters_tracks = 0
xiccpp_total_tracks = 0
xilc_daughter_total_tracks = 0
xiccpp_background_tracks = 0
xilc_background_total_tracks = 0

pion_true_tracks = 0
xiccpp_true_pion_tracks = 0
true_bachelor_pion_tracks = 0
xiccpp_pion_tracks = 0
bachelor_pion_tracks = 0
pion_background_tracks = 0
pion_bachelor_background_tracks = 0

kaon_true_tracks = 0
xicpp_true_kaon_tracks = 0
true_bachelor_kaon_tracks = 0
xiccpp_kaon_tracks = 0
bachelor_kaon_tracks = 0
kaon_background_tracks= 0
kaon_bachelor_background_tracks = 0

for i in range(num_files):
  events.AddFile( path.join(dir, onlyfiles[i]) )  # Look at a file in the target directory for analysis

for event in events: # loop through all events
   #Lambdac
   xiccpp_true_number = [track for track in event.Particles if abs(track.trueID) == particle_dict['xicc++']]

   true_xiccpp = [track for track in event.Particles if is_from(track,event,particle_dict['xicc++'])]
   true_xilc_daughters = [track for track in event.Particles if (is_Gparent(track,event,particle_dict['xicc++']) and is_parent(track,event,particle_dict['lambdac']))]

   displaced_tracks = ROOT.select( event.Particles, event.Vertices, min_pt, min_p,min_ipChi2_4d) # select particles, verticies, min_pt, min_p,min_ipChi2_4d

   xiccpp_tracks = [ track for track in displaced_tracks if is_from(track,event,particle_dict['xicc++'])] # all proton^
   xilc_daughter_tracks = [ track for track in displaced_tracks if (is_Gparent(track,event,particle_dict['xicc++']) and is_parent(track,event,particle_dict['lambdac']))] # all proton^

   background_tracks = [ track for track in displaced_tracks if not is_from(track,event,particle_dict['xicc++'])]
   xilc_background_tracks = [ track for track in displaced_tracks if not (is_Gparent(track,event,particle_dict['xicc++']) and is_parent(track,event,particle_dict['lambdac']))]

   # Bachelor
   true_pions = [track for track in event.Particles if abs(track.trueID) == particle_dict['Pion']]

   true_xiccpp_pions = [track for track in true_pions if is_from(track,event,particle_dict['xicc++'])]
   true_bachelor_pions = [track for track in true_pions if (is_parent(track,event,particle_dict['xicc++']))]
   
   pions = [ track for track in ROOT.select( event.Particles, event.Vertices, min_pt, min_p, min_ipChi2_4d ) if  abs(track.trueID) == particle_dict['Pion']]

   xiccpp_pions = [ track for track in pions if is_from(track,event,particle_dict['xicc++'])] # all proton^
   bachelor_pions = [ track for track in pions if (is_parent(track,event,particle_dict['xicc++']))] # all proton^

   pion_background = [ track for track in pions if not is_from(track,event,particle_dict['xicc++'])] # all proton^
   bachelor_pion_background = [ track for track in pions if not (is_parent(track,event,particle_dict['xicc++']))] # all proton^

  # Bachelor
   true_kaons = [track for track in event.Particles if abs(track.trueID) == particle_dict['Kaon']]

   true_xiccpp_kaons = [track for track in true_kaons if is_from(track,event,particle_dict['xicc++'])]
   true_bachelor_kaons = [track for track in true_kaons if (is_parent(track,event,particle_dict['xicc++']))]

   kaons = [ track for track in ROOT.select( event.Particles, event.Vertices, min_pt, min_p, min_ipChi2_4d ) if  abs(track.trueID) == particle_dict['Kaon']] # needs changing from bs to xi limits

   xiccpp_kaons = [ track for track in kaons if is_from(track,event,particle_dict['xicc++'])] # all proton^
   bachelor_kaons = [ track for track in kaons if (is_parent(track,event,particle_dict['xicc++']))]

   kaon_background = [ track for track in kaons if not  is_from(track,event,particle_dict['xicc++'])] # all proton^
   bachelor_kaon_background = [ track for track in kaons if not (is_parent(track,event,particle_dict['xicc++']))] # all proton^

   xiccpp_total_true_number += len(xiccpp_true_number)
   xiccpp_true_tracks += len(true_xiccpp)
   xilc_true_daughters_tracks += len(true_xilc_daughters)
   xiccpp_total_tracks += len(xiccpp_tracks)
   xilc_daughter_total_tracks += len(xilc_daughter_tracks)
   xiccpp_background_tracks += len(background_tracks)
   xilc_background_total_tracks += len(xilc_background_tracks)
   
   pion_true_tracks += len(true_pions)
   xiccpp_true_pion_tracks += len(true_xiccpp_pions)
   true_bachelor_pion_tracks += len(true_bachelor_pions)
   xiccpp_pion_tracks += len(xiccpp_pions)
   bachelor_pion_tracks += len(bachelor_pions)
   pion_background_tracks += len(pion_background)
   pion_bachelor_background_tracks += len(bachelor_pion_background)
   
   kaon_true_tracks += len(true_kaons)
   xicpp_true_kaon_tracks += len(true_xiccpp_kaons)
   true_bachelor_kaon_tracks += len(true_bachelor_kaons)
   xiccpp_kaon_tracks += len(xiccpp_kaons)
   bachelor_kaon_tracks += len(bachelor_kaons)
   kaon_background_tracks += len(kaon_background)
   kaon_bachelor_background_tracks += len(bachelor_kaon_background)

data = [num_files, 
        min_pt,
          min_p,
            min_ipChi2_4d, 
           
            xiccpp_total_true_number,
            xiccpp_true_tracks,
            xilc_true_daughters_tracks,
            xiccpp_total_tracks,
            xilc_daughter_total_tracks,
            xiccpp_background_tracks,
            xilc_background_total_tracks,

            pion_true_tracks,
            xiccpp_true_pion_tracks,
            true_bachelor_pion_tracks,
            xiccpp_pion_tracks,
            bachelor_pion_tracks,
            pion_background_tracks,
            pion_bachelor_background_tracks,

            kaon_true_tracks,
            xicpp_true_kaon_tracks,
            true_bachelor_kaon_tracks,
            xiccpp_kaon_tracks,
            bachelor_kaon_tracks,
            kaon_background_tracks,
            kaon_bachelor_background_tracks,
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
                         "#1.TotalTrueXiLcDaughterTracks",
                         "#1.TotalXiccppTracks",
                         "#1.TotalXiLcDaughterTracks",
                         "#1.TotalBackgroundTracks",
                         "#1.TotalXiLcBackgroundTracks"

                         "#2.TotalTruePions", 
                         "#TotalTrueBachelorPionTracks",
                         "#2.TotalTrueXiccppPions",
                         "#2.TotalXiccppPions",
                         "#2.TotalBachelorPionTracks",
                         "#2.TotalBackgroundPions",
                         "#2.TotalBachelorPionBackgroundTracks",

                         "#3.TotalTrueKaons",
                         "#3.TotalTrueXiccppKaons",
                         "#3.TotalTrueBachelorKaonTracks"
                         "#3.TotalXiccppKaons",
                         "#3.TotalBachelorKaonTracks",
                         "#3.TotalBackgroundKaons"
                         "#3.TotalBackgroundBachelorKaons"])

    # Append the data
    writer.writerow(data)
