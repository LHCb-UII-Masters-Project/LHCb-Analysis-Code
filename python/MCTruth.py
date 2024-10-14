import ROOT
from ROOT import TFile, gSystem, gInterpreter
from ROOT import TH1D, TH2D, TCanvas

from Selections import load_event_library 
from math import * 
from MCTools import *

load_event_library()
file = TFile("test.root","READ")

mom_resolution = TH1D("dp","; p_x - p_x^{true} [MeV/c]; \\text{Candidates} / 10 MeV /c",50,-250,250)
events = file.Events 

entry = 0 
for event in events: 
  tracks = event.Particles
  for track in tracks : 
      if track.trueID == 0 : continue
      mc_particle = get_mc_particle(track, event)  
      mom_resolution.Fill( track.p4().x() - mc_particle.p4().x() )

mom_resolution.Draw()
