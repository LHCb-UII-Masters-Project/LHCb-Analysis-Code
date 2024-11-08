from Selections import load_event_library 
import ROOT 
from ROOT import TFile, TH1D, TH2D, TCanvas
from math import * 

load_event_library()

file = TFile("/eos/lhcb/user/t/tevans/HLT1/allen_zerobias.root","READ")

events = file.Events 

mass_hist = TH1D("mass_hist","; m(\\pi^-\\pi^{+}) [MeV/c^{2}]; \\text{Candidates} / 10 MeV /c^{2}",50,450,550)
ip_chi2   = TH1D("ipchi2"   ,"; \\chi^2_{IP}( \\pi_1 ); \\text{Candidates} / 10 MeV /c^{2}",50,-10,10)
def min_dist( particle, vertices ):
  min_dist = 9999
  for v in vertices: 
    d = ( particle.firstState.x0 - v.x)**2 + ( particle.firstState.y0 - v.y)**2 + ( particle.firstState.z - vertex.z)**2 
    if d < min_dist : min_dist = d
  return sqrt( min_dist ) 

def min_ipchi2(particle, vertices): 
  min_ipchi2  = 9999 
  for v in vertices: 
    ipchi2 = particle.ipchi2(v)
    if ipchi2 < min_ipchi2 : min_ipchi2 = ipchi2
  return min_ipchi2

def dira_bpv( particle, vertices, max_dt):
  vertex = vertices[0]
  ip = particle.ip(vertex) 
  for index in range(1, len(vertices ) ) :
    if particle.ip(vertices[index]) < ip : 
      vertex = vertices[index]
      ip = particle.ip(vertices[index])
  dx = particle.firstState.x0 - vertex.x 
  dy = particle.firstState.y0 - vertex.y 
  dz = particle.firstState.z  - vertex.z
  p = particle.p4()
  return (dx * p.x() + dy * p.y() + dz * p.z() ) / sqrt( (dx**2 + dy**2 + dz**2 )*p.P2() )

entry = 0 
for event in events: 
  if entry % 10000 == 0 : print("Processed {} entries".format(entry) )
  tracks = event.Particles
  if len( event.Vertices ) == 0 : continue 
  displaced_tracks = [ track for track in tracks if ( track.pt() > 500 
                                                  and track.p() > 1000) 
                                                  and min_ipchi2(track, event.Vertices) > 50 ]
  doca_cut = 0.2 
  entry = entry + 1
  for pi1 in displaced_tracks : 
    for pi2 in displaced_tracks :
      if pi1.charge() == pi2.charge() : continue
      if pi1.firstState.doca( pi2.firstState ) > doca_cut : continue 
      vtx = ROOT.uVertex( [pi1, pi2] )
      if vtx.chi2 / vtx.ndof > 10 : continue
      kpi = ROOT.uParticle( [pi1, pi2] )
      if kpi.mass > 700 : continue
      mass_hist.Fill( kpi.mass )
      ip_chi2.Fill( log( min_ipchi2( pi1, event.Vertices )) ) 

canvas = TCanvas("c1","",1000,800)
canvas.Divide(2,1)
canvas.cd(1) 
mass_hist.Draw() 
canvas.cd(2) 
ip_chi2.Draw() 

