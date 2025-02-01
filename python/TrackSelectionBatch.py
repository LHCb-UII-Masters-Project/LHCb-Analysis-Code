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

def particle_selector(tracks, min_min_pt, max_min_pt, pt_interval):
  lc_daughters = np.zeros(int((max_min_pt - min_min_pt)/pt_interval))
  xi_lc_daughters = np.zeros_like(lc_daughters)
  xi_daughters = np.zeros_like(lc_daughters)
  particles = np.zeros_like(lc_daughters)

  for track in tracks:
    if is_parent(track, event, 4122):
      lc_daughters[i] += 1
      if is_Gparent(track, event, 4222):
        xi_lc_daughters[i] += 1
    elif is_parent(track, event, 4222):
      xi_daughters[i] += 1
    particles[i] += 1

    return lc_daughters, xi_lc_daughters, xi_daughters, particles

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
min_min_pt = get_arg(2, 200, args)
max_min_pt = get_arg(3, 1000, args)
pt_interval = get_arg(4, 100, args)
min_p = get_arg(5, 1500, args)
min_ipChi2_4d = float(args[6])

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

num_pion = 0
num_kaon = 0
num_proton = 0

max_num_lambdac_candidates = 0
max_num_lambdac = 0
max_num_xilambdac = 0
max_num_Xiccdouble = 0

for event in events: # loop through all events

  max_tracks = ROOT.select( event.Particles, event.Vertices, max_min_pt, min_p,min_ipChi2_4d) # select particles, verticies, min_pt, min_p,min_ipChi2_4d
  # selects acceptable particles for analysis min_pt, min_p, min_ipchi2_4d
  #full_tracks = ROOT.select( event.Particles, event.Vertices, 0, 0, 0 )
  # xi_tracks = ROOT.select( event.Particles, event.Vertices, 500, 1000, 3 )

  num_event_lambdac_pions = 0
  num_event_lambdac_kaons = 0
  num_event_lambdac_protons = 0
  num_event_xilambdac_pions = 0
  num_event_xilambdac_kaons = 0
  num_event_xilambdac_protons = 0
  num_event_xi_pions = 0
  num_event_xi_kaons = 0
  num_event_xi_protons = 0
  max_num_event_lambdac_candidates = 0
  max_num_event_lambdac = 0
  max_num_event_xilambdac = 0
  max_num_event_xi = 0

  investigated_tracks = max_tracks  # Toggle between track selections

  for track in investigated_tracks:
    tracks = np.append(tracks, abs(track.trueID))
  
  
  all_pions = [track for track in investigated_tracks if abs( track.trueID ) == 211]  # all pi
  pions = [ track for track in investigated_tracks if abs(track.trueID) == 211 and track.charge() > 0] # all pi+

  all_kaons = [ track for track in investigated_tracks if abs( track.trueID ) == 321] # all kaons
  kaons = [ track for track in investigated_tracks if abs(track.trueID) == 321 and track.charge() < 0] # all k^-

  all_protons = [track for track in investigated_tracks if abs( track.trueID ) == 2212]  # all p
  protons = [ track for track in investigated_tracks if abs(track.trueID) == 2212 and track.charge() > 0] # all p^+

  num_event_lambdac_pions, num_event_xilambdac_pions, num_event_xi_pions, num_pions = particle_selector(pions, min_min_pt, max_min_pt)
  num_event_lambdac_kaons, num_event_xilambdac_kaons, num_event_xi_kaons, num_kaons = particle_selector(kaons, min_min_pt, max_min_pt)
  num_event_lambdac_protons, num_event_xilambdac_protons, _, num_protons = particle_selector(protons, min_min_pt, max_min_pt)
  
  max_num_event_lambdac_candidates = num_pion * num_proton * num_kaon
  if num_event_lambdac_protons > 0 and num_event_lambdac_kaons > 0 and num_event_lambdac_protons > 0:
    max_num_event_lambdac = 1
  if num_event_xilambdac_protons > 0 and num_event_xilambdac_kaons > 0 and num_event_xilambdac_protons > 0:
    max_num_event_xilambdac = 1
    if num_event_xi_kaons > 0 and num_event_xi_pions > 1:
      max_num_event_xi = 1

  num_lambdac_kaons += num_event_lambdac_kaons
  num_lambdac_pions += num_event_lambdac_pions
  num_lambdac_protons += num_event_lambdac_protons

  num_xilambdac_kaons += num_event_xilambdac_kaons
  num_xilambdac_pions += num_event_xilambdac_pions
  num_xilambdac_protons += num_event_xilambdac_protons

  num_xi_protons += num_event_xi_protons
  num_xi_kaons += num_event_xi_kaons
  num_xi_pions += num_event_xi_pions

  max_num_lambdac_candidates += max_num_event_lambdac_candidates
  max_num_lambdac += max_num_event_lambdac
  max_num_xilambdac += max_num_event_xilambdac
  max_num_Xiccdouble += max_num_event_xi


print("\n_______")
print(f"{num_lambdac_pions} occurrences of LambdacPion")
print(f"{num_xilambdac_pions} occurrences of XiLambdacPion")
print(f"{num_xi_pions} occurrences of Xicc++Pion")
print(f"{num_pion} occurrences of Pion")
print("\n_______")
print(f"{num_lambdac_kaons} occurrences of LambdacKaon")
print(f"{num_xilambdac_kaons} occurrences of XiLambdacKaon")
print(f"{num_xi_kaons} occurrences of Xicc++Kaon")
print(f"{num_kaon} occurrences of Kaon")
print("\n_______")
print(f"{num_lambdac_protons} occurrences of LambdacProton")
print(f"{num_xilambdac_protons} occurrences of XiLambdacProton")
print(f"{num_proton} occurrences of Proton")
print("\n_______")

print(f"{max_num_lambdac_candidates} Lambdac candidates made")
print(f"{max_num_lambdac} Lambdac made")
print(f"{max_num_xilambdac} XiLambdac made")
print(f"{num_xi_kaons} XiKaons Made")
print(f"{num_xi_pions} XiPions Made")
print(f"{max_num_Xiccdouble} Xicc++ possible")

# 10 file, full-tracks values
# max_num_lambdac = 464
# max_num_xilambdac = 504
# num_xi_kaons = 493
# num_xi_pions = 973
# max_num_Xiccdouble = 399
# num_pions = 312407
# num_kaons = 44186
# num_proton = 34833

data = [num_files, min_pt, min_p, min_ipChi2_4d, max_num_lambdac_candidates, max_num_lambdac, max_num_xilambdac, 
        num_xi_kaons, num_xi_pions, max_num_Xiccdouble, num_pion, num_kaon, num_proton]

# Filepath for the CSV file
file_path = f"{basedir}/Outputs/TrackSelection/LambdacCompIP{min_ipChi2_4d}.csv"

# Check if the file exists
file_exists = path.isfile(file_path)

# Open the file in append mode
with open(file_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    
    # Write header only if the file doesn't exist
    if not file_exists:
        writer.writerow(["NumFiles", "MinPT", "MinP", "MinIPChi2", "#LambdaCandidates", "#Lambdas", "#XiLambdas", "#XiKaons",
                         "#XiPions", "#Xis", "#Pion", "#Kaon", "#Proton"])
    
    # Append the data
    writer.writerow(data)
