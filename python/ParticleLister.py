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
dir="/disk/moose/general/djdt/lhcbUII_masters/dataStore/Beam7000GeV-md100-nu38-VerExtAngle_vpOnly/13264021/VP_U2_ParamModel-SX/SX_10um50s_75umcylindr3p5_nu38_Bs2Dspi_2111/moore/"
onlyfiles = [f for f in listdir(dir) if path.isfile(path.join(dir, f))]
events.AddFile( path.join(dir, onlyfiles[1]) )  # Look at a file in the target directory for analysis

tracks = np.array([])

for event in events: # loop through all events
  
  # scaled_tracks = []
  # for track in event.Particles : 
  #   track.scale_uncertainty(1, 5)   
  #   scaled_tracks.append( track ) 
  
  displaced_tracks = ROOT.select( event.Particles, event.Vertices, 250, 1500, 6 ) # select particles, verticies, min_pt, min_p,min_ipChi2_4d
  # selects acceptable particles for analysis min_pt, min_p, min_ipchi2_4d
  full_tracks = ROOT.select( event.Particles, event.Vertices, 0, 0, 4 )

  # print( "{} {}".format( scaled_tracks[0].firstState.cov(5,5), event.Particles[0].firstState.cov(5,5) ) ) 

  #good_pions = [ track for track in displaced_tracks if abs( track.trueID ) == 211] # narrows particels to only good pions or
  #good_ds = [ track for track in displaced_tracks if abs( track.trueID ) == 431] #  good Ds

  for track in full_tracks:
    tracks = np.append(tracks, abs(track.trueID))

tracks = tracks[tracks != 0]
unique_numbers, counts = np.unique(tracks, return_counts=True)

for number, count in zip(unique_numbers, counts):
    print(f"{count} occurrences of {number}")
