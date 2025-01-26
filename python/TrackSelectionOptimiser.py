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
min_ipChi2_4d = get_arg(4, 6, args)

from MCTools import * 
gInterpreter.AddIncludePath( f'{basedir}/../include')
gSystem.Load( f'{basedir}/../build/libEvent.so') # add the event library to the python path

events = TChain("Events") # connects all the events into a single data set

# can be changed to look at different timing resolutions and detector geometries
dir=f"/disk/moose/lhcb/djdt/photonics/stackNov24/masters_XiccTest/largeRun_Xicc++/sym/"
onlyfiles = [f for f in listdir(dir) if path.isfile(path.join(dir, f))]

for i in range(num_files):
  events.AddFile( path.join(dir, onlyfiles[i]) )  # Look at a file in the target directory for analysis

tracks = np.array([])

num_lambdac_pions = 0
num_lambdac_kaons = 0
num_lambdac_protons = 0
num_xilambdac_pions = 0
num_xilambdac_kaons = 0
num_xilambdac_protons = 0
num_xi_pions = 0
num_xi_kaons = 0
num_xi_protons = 0

max_num_event_lambdac = 0
max_num_event_xilambdac = 0
max_num_event_xi = 0
max_num_lambdac = 0
max_num_xilambdac = 0

for event in events: # loop through all events

  lambdac_tracks = ROOT.select( event.Particles, event.Vertices, min_pt, min_p,min_ipChi2_4d) # select particles, verticies, min_pt, min_p,min_ipChi2_4d
  # selects acceptable particles for analysis min_pt, min_p, min_ipchi2_4d
  full_tracks = ROOT.select( event.Particles, event.Vertices, 0, 0, 0 )

  num_event_lambdac_pions = 0
  num_event_lambdac_kaons = 0
  num_event_lambdac_protons = 0
  num_event_xilambdac_pions = 0
  num_event_xilambdac_kaons = 0
  num_event_xilambdac_protons = 0
  num_event_xi_pions = 0
  num_event_xi_kaons = 0
  num_event_xi_protons = 0

  investigated_tracks = lambdac_tracks  # Toggle between track selections

  for track in investigated_tracks:
    tracks = np.append(tracks, abs(track.trueID))
  
  
  all_pions = [track for track in investigated_tracks if abs( track.trueID ) == 211]  # all pi
  pions = [ track for track in investigated_tracks if abs(track.trueID) == 211 and track.charge() > 0] # all pi+

  all_kaons = [ track for track in investigated_tracks if abs( track.trueID ) == 321] # all kaons
  kaons = [ track for track in investigated_tracks if abs(track.trueID) == 321 and track.charge() < 0] # all k^-

  all_protons = [track for track in investigated_tracks if abs( track.trueID ) == 2212]  # all p
  protons = [ track for track in investigated_tracks if abs(track.trueID) == 2212 and track.charge() > 0] # all p^+

  for pion in pions:
    if is_parent(pion, event, 4122):
      num_event_lambdac_pions += 1
      if is_Gparent(pion, event, 4222):
        num_event_xilambdac_pions += 1
    elif is_parent(pion, event, 4222):
      num_event_xi_pions += 1

  for kaon in kaons:
    if is_parent(kaon, event, 4122):
      num_event_lambdac_kaons += 1
      if is_Gparent(kaon, event, 4222):
        num_event_xilambdac_kaons += 1
    elif is_parent(kaon, event, 4222):
      num_event_xi_kaons += 1

  for proton in protons:
    if is_parent(proton, event, 4122):
      num_event_lambdac_protons += 1
      if is_Gparent(proton, event, 4222):
        num_event_xilambdac_protons += 1
  
  if num_event_lambdac_protons > 0 and num_event_lambdac_kaons > 0 and num_event_lambdac_protons > 0:
    max_num_event_lambdac += 1
  if num_event_xilambdac_protons > 0 and num_event_xilambdac_kaons > 0 and num_event_xilambdac_protons > 0:
    max_num_event_xilambdac += 1
    if num_event_xi_kaons > 0 and num_event_xi_pions > 1:
      max_num_event_xi += 1

  num_lambdac_kaons += num_event_lambdac_kaons
  num_lambdac_pions += num_event_lambdac_pions
  num_lambdac_protons += num_event_lambdac_protons

  num_xilambdac_kaons += num_event_xilambdac_kaons
  num_xilambdac_pions += num_event_xilambdac_pions
  num_xilambdac_protons += num_event_xilambdac_protons

  num_xi_protons += num_event_xi_protons
  num_xi_kaons += num_event_xi_kaons
  num_xi_pions += num_event_xi_pions

  max_num_lambdac += max_num_event_lambdac
  max_num_xilambdac += max_num_event_xilambdac
  max_num_Xiccdouble = max_num_event_xi

tracks = tracks[tracks != 0]
unique_numbers, counts = np.unique(tracks, return_counts=True)

print("\n_______")
for number, count in zip(unique_numbers, counts):
    if abs(number) == 211.0: 
      print(f"{count} occurrences of Pion")
      num_pion = count
      print(f"{num_lambdac_pions} occurrences of LambdacPion")
      print(f"{num_xilambdac_pions} occurrences of XiLambdacPion")
      print(f"{num_xi_pions} occurrences of Xicc++Pion")
      print("\n_______")
    elif abs(number) == 321.0: 
      print(f"{count} occurrences of Kaon")
      num_kaon = count
      print(f"{num_lambdac_kaons} occurrences of LambdacKaon")
      print(f"{num_xilambdac_kaons} occurrences of XiLambdacKaon")
      print(f"{num_xi_kaons} occurrences of Xicc++Kaon")
      print("\n_______")
    elif abs(number) == 2212.0: 
      print(f"{count} occurrences of Proton")
      num_proton = count
      print(f"{num_lambdac_protons} occurrences of LambdacProton")
      print(f"{num_xilambdac_protons} occurrences of XiLambdacProton")
      print("\n_______")

print(f"{max_num_lambdac} Lambdac made")
print(f"{max_num_xilambdac} XiLambdac made")
print(f"{max_num_Xiccdouble} Xicc++ possible")

# 5 file, full-tracks values
"""
frac_track_num_lambdac = max_num_lambdac/56939
frac_track_num_xilambdac = max_num_xilambdac/56266
frac_track_num_xikaons = num_xi_kaons/258
frac_track_num_xipion = num_xi_pions/506
frac_track_num_xi = max_num_Xiccdouble/203
"""

# 10 file, full-tracks values
frac_track_num_lambdac = max_num_lambdac/236842
frac_track_num_xilambdac = max_num_xilambdac/233171
frac_track_num_xikaons = num_xi_kaons/493
frac_track_num_xipion = num_xi_pions/973
frac_track_num_xi = max_num_Xiccdouble/399
# num_pions = 622662
# num_kaons = 88970
# num_proton = 66641

print("\n_______")
print(f"{frac_track_num_lambdac} Lambdacs Made")
print(f"{frac_track_num_xilambdac} XiLambdacs Made")
print(f"{frac_track_num_xikaons} XiKaons Made")
print(f"{frac_track_num_xipion} XiKaons Made")
print(f"{frac_track_num_xi} Xi Made")


data = [num_files, min_pt, min_p, min_ipChi2_4d, frac_track_num_lambdac, frac_track_num_xilambdac, 
        frac_track_num_xikaons, frac_track_num_xipion, frac_track_num_xi, num_pion, num_kaon, num_proton]

# Filepath for the CSV file
file_path = f"{basedir}/Outputs/TrackSelection/LambdacCompIP{min_ipChi2_4d}.csv"

# Check if the file exists
file_exists = path.isfile(file_path)

# Open the file in append mode
with open(file_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    
    # Write header only if the file doesn't exist
    if not file_exists:
        writer.writerow(["NumFiles", "MinPT", "MinP", "MinIPChi2", "#Lambdas", "#XiLambdas", "#XiKaons",
                         "#XiPions", "#Xis", "#Pion", "#Kaon", "#Proton"])
    
    # Append the data
    writer.writerow(data)
