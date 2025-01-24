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

basedir=path.dirname(path.realpath(__file__))

sys.path.insert(0,basedir) 
from MCTools import * 
gInterpreter.AddIncludePath( f'{basedir}/../include')
gSystem.Load( f'{basedir}/../build/libEvent.so') # add the event library to the python path

events = TChain("Events") # connects all the events into a single data set

# can be changed to look at different timing resolutions and detector geometries
dir=f"/disk/moose/lhcb/djdt/photonics/stackNov24/masters_XiccTest/largeRun_Xicc++/sym/"
onlyfiles = [f for f in listdir(dir) if path.isfile(path.join(dir, f))]

for i in range(5):
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
  
  # scaled_tracks = []
  # for track in event.Particles : 
  #   track.scale_uncertainty(1, 5)   
  #   scaled_tracks.append( track ) 
  
  lambdac_tracks = ROOT.select( event.Particles, event.Vertices, 200, 1000,6) # select particles, verticies, min_pt, min_p,min_ipChi2_4d
  # selects acceptable particles for analysis min_pt, min_p, min_ipchi2_4d
  full_tracks = ROOT.select( event.Particles, event.Vertices, 0, 0, 0 )

  # print( "{} {}".format( scaled_tracks[0].firstState.cov(5,5), event.Particles[0].firstState.cov(5,5) ) ) 

  num_event_lambdac_pions = 0
  num_event_lambdac_kaons = 0
  num_event_lambdac_protons = 0
  num_event_xilambdac_pions = 0
  num_event_xilambdac_kaons = 0
  num_event_xilambdac_protons = 0
  num_event_xi_pions = 0
  num_event_xi_kaons = 0
  num_event_xi_protons = 0

  investigated_tracks = full_tracks  # Toggle between track selections

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

print("_______")
for number, count in zip(unique_numbers, counts):
    if abs(number) == 211.0: 
      print(f"{count} occurrences of Pion")
      print(f"{num_lambdac_pions} occurrences of LambdacPion")
      print(f"{num_xilambdac_pions} occurrences of XiLambdacPion")
      print(f"{num_xi_pions} occurrences of Xicc++Pion")
      print("_______")
    elif abs(number) == 321.0: 
      print(f"{count} occurrences of Kaon")
      print(f"{num_lambdac_kaons} occurrences of LambdacKaon")
      print(f"{num_xilambdac_kaons} occurrences of XiLambdacKaon")
      print(f"{num_xi_kaons} occurrences of Xicc++Kaon")
      print("_______")
    elif abs(number) == 2212.0: 
      print(f"{count} occurrences of Proton")
      print(f"{num_lambdac_protons} occurrences of LambdacProton")
      print(f"{num_xilambdac_protons} occurrences of XiLambdacProton")
      print("_______")

print(f"{max_num_lambdac} Lambdac made")
print(f"{max_num_xilambdac} XiLambdac made")
print(f"{max_num_Xiccdouble} Xicc++ possible")

# 5 file, full-tracks values
ftrack_num_lambdac = 56939
ftrack_num_xilambdac = 56266
ftrack_num_xikaons = 258
ftrack_num_xipion = 506
ftrack_num_xi = 203

print("\n_______")
print(f"{max_num_lambdac/ftrack_num_lambdac} Lambdacs Made")
print(f"{max_num_xilambdac/ftrack_num_xilambdac} XiLambdacs Made")
print(f"{num_xi_kaons/ftrack_num_xikaons} XiKaons Made")
print(f"{num_xi_pions/ftrack_num_xipion} XiKaons Made")
print(f"{max_num_Xiccdouble/ftrack_num_xi} Xi Made")
