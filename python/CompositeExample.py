from Selections import load_event_library, get_secondary_vertices
import ROOT 
from ROOT import TFile, TH1D, TH2D, TCanvas
from math import * 

load_event_library()

file = TFile("/eos/lhcb/user/t/tevans/HLT1/allen_zerobias.root","READ")
events = file.Events 

rho   = TH1D("rho"   ,"; \\rho(SV) [mm]; \\text{Candidates} / 0.2 mm ",50,0,10)

def bpv( particle, vertices): 
    min_ip = 9999
    rt = 0
    for v in vertices : 
        ip = particle.ip(v)
        if ip < min_ip : 
            min_ip = ip
            rt = v 
    return rt 

entry = 0 
for event in events: 
  if entry % 10000 == 0 : print("Processed {} entries".format(entry) )
  if entry >= 1000000 : break 
  tracks = event.Particles
  svs    = get_secondary_vertices(event)  
  for sv in svs : 
    pv = bpv(sv, event.Vertices)
    if pv == 0 : continue
    rho_v = sqrt( ( sv.x  - pv.x ) **2 + (sv.y - pv.y )**2 + (sv.z - pv.z)**2 )
    rho.Fill( rho_v )
  entry=entry+1

canvas = TCanvas("c1","",1000,800)
rho.Draw() 
