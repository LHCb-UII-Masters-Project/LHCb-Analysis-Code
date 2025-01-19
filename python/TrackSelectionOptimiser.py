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
dir=f"/disk/moose/lhcb/djdt/photonics/stackNov24/masters_XiccTest/largeRun_Xicc+/sym/"
onlyfiles = [f for f in listdir(dir) if path.isfile(path.join(dir, f))]
events.AddFile( path.join(dir, onlyfiles[1]) )  # Look at a file in the target directory for analysis

tracks = np.array([])

for event in events: # loop through all events
  
  # scaled_tracks = []
  # for track in event.Particles : 
  #   track.scale_uncertainty(1, 5)   
  #   scaled_tracks.append( track ) 
  
  lambdac_tracks = ROOT.select( event.Particles, event.Vertices, 250, 1500, 3 ) # select particles, verticies, min_pt, min_p,min_ipChi2_4d
  # selects acceptable particles for analysis min_pt, min_p, min_ipchi2_4d
  full_tracks = ROOT.select( event.Particles, event.Vertices, 0, 0, 2 )

  # print( "{} {}".format( scaled_tracks[0].firstState.cov(5,5), event.Particles[0].firstState.cov(5,5) ) ) 

  #good_pions = [ track for track in displaced_tracks if abs( track.trueID ) == 211] # narrows particels to only good pions or
  #good_ds = [ track for track in displaced_tracks if abs( track.trueID ) == 431] #  good Ds

  for track in full_tracks:
    tracks = np.append(tracks, abs(track.trueID))


    total_pions = [track for track in lambdac_tracks if abs( track.trueID ) == 211]  # all pi
    pions = [ track for track in lambdac_tracks if abs(track.trueID) == 211 and track.charge() > 0] # all pi+
    
    all_kaons = [ track for track in lambdac_tracks if abs( track.trueID ) == 321] # all kaons
    good_kaons = [] # initialised list to be filled with good kaons
    good_kaons = [ track for track in lambdac_tracks if abs(track.trueID) == 321 and track.charge() < 0] # all k^-

    total_protons = [track for track in lambdac_tracks if abs( track.trueID ) == 2212]  # all p
    protons = [ track for track in lambdac_tracks if abs(track.trueID) == 2212 and track.charge() > 0] # all p^+
    num_lambdac_pions = 0
    num_lambdac_kaons = 0
    num_lambdac_protons = 0
    num_Xicdouble_pions = 0
    num_Xicdouble_kaons = 0
    num_Xicdouble_protons = 0
  
  for pion in pions:
    if is_from(pion, event, 4122):
      num_lambdac_pions += 1
    if is_from(pion, event, 4412):
      num_Xicdouble_pions += 1
  
  for kaon in all_kaons:
    if is_from(kaon, event, 4122):
      num_lambdac_kaons += 1
    if is_from(kaon, event, 4412):
      num_Xicdouble_kaons += 1
          
  for proton in total_protons:
    if is_from(proton, event, 4122):
      num_lambdac_protons += 1
    if is_from(proton, event, 4412):
      num_Xicdouble_protons += 1
                
max_num_lambdac = min(num_lambdac_kaons, num_lambdac_pions, num_lambdac_protons)

tracks = tracks[tracks != 0]
unique_numbers, counts = np.unique(tracks, return_counts=True)

for number, count in zip(unique_numbers, counts):
    if number == 211.0: 
      print(f"{count} occurrences of Pion")
      print(f"{num_lambdac_pions} occurrences of LambdacPion")
      num_pions = count
    elif number == 321.0: 
      print(f"{count} occurrences of Kaon")
      print(f"{num_lambdac_kaons} occurrences of LambdacKaon")
      num_kaon = count
    elif number == 2212.0: 
      print(f"{count} occurrences of Proton")
      print(f"{num_lambdac_protons} occurrences of LambdacProton")
      num_proton = count

max_num_bad_lambdac = min(num_pions, num_kaon, num_proton)
print(f"{max_num_lambdac} Lambdac made")
if max_num_lambdac != 0:
  print(f"Approx SNR of {max_num_lambdac/(max_num_lambdac)}")
else:
  print("There are no good Lambdac candidates")
