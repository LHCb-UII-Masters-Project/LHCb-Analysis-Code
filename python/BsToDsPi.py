from ROOT import TFile, gSystem, gInterpreter
from ROOT import TH1D, TH2D, TCanvas, TChain
from math import * 
import sys
from os import path, listdir 


import ROOT
from Selections import load_event_library
load_event_library()
from ROOT import uParticle


basedir=path.dirname(path.realpath(__file__))

class SigVsBkg:
  def __init__(self, name, nBins, min, max):
    self.signal = ROOT.TH1D( name +"_signal","",nBins, min,max )
    self.background = ROOT.TH1D( name +"_bkg","",nBins, min,max)
  def Fill( self, x, isSignal ) : 
    if isSignal : self.signal.Fill(x)
    else:  self.background.Fill(x)
  def Draw(self ) :
    self.signal.Scale( 1 / self.signal.Integral() ) 
    self.background.Scale( 1 / self.background.Integral() ) 
    self.signal.Draw()
    self.background.SetLineColor(ROOT.kRed)
    self.background.Draw("same")

def dira_bpv( particle, vertices, max_dt):
  vertex = vertices[0]
  ipw = lambda particle, vertex : particle.ip(vertex) if particle.ip_t(vertex) < max_dt else 9999

  ip = ipw(particle, vertex ) 
  for index in range(1, len(vertices ) ) :
    if ipw(particle, vertices[index]) < ip : 
      vertex = vertices[index]
      ip = particle.ip(vertices[index])
  dx = particle.firstState.x0 - vertex.x 
  dy = particle.firstState.y0 - vertex.y 
  dz = particle.firstState.z  - vertex.z
  p = particle.p4()
  return (dx * p.x() + dy * p.y() + dz * p.z() ) / sqrt( (dx**2 + dy**2 + dz**2 )*p.P2() )

sys.path.insert(0,basedir) 
from MCTools import * 
gInterpreter.AddIncludePath( f'{basedir}/../include')
gSystem.Load( f'{basedir}/../build/libEvent.so')

events = TChain("Events")
dir="/disk/moose/general/djdt/lhcbUII_masters/dataStore/Beam7000GeV-md100-nu38-VerExtAngle_vpOnly/13264021/VP_U2_ParamModel-SX/SX_10um50s_75umcylindr3p5_nu38_Bs2Dspi_2111/moore/"
onlyfiles = [f for f in listdir(dir) if path.isfile(path.join(dir, f))]
print(onlyfiles)
#for file in onlyfiles : 
#events.AddFile( "root://eoslhcb.cern.ch//" + path.join(dir, file) ) 
events.AddFile( path.join(dir, onlyfiles[1]) ) 
print(path.join(dir, onlyfiles[1]))

entry=0
plot = ROOT.TH1D("m_ds","",100,1.8,2.1)
vtx_chi2 = SigVsBkg("vtx_chi2",100,0,100)

n_signal=0

for event in events: 
  # scaled_tracks = []
  # for track in event.Particles : 
  #   track.scale_uncertainty(1, 5)   
  #   scaled_tracks.append( track ) 
  
  displaced_tracks = ROOT.select( event.Particles, event.Vertices, 250, 1500, 6 )

  # print( "{} {}".format( scaled_tracks[0].firstState.cov(5,5), event.Particles[0].firstState.cov(5,5) ) ) 

  good_pions = [ track for track in displaced_tracks if abs( track.trueID ) == 211]
  good_kaons = [ track for track in displaced_tracks if abs( track.trueID ) == 321]
  kp = [track for track in good_kaons if track.charge() > 0 ]
  km = [track for track in good_kaons if track.charge() < 0 ]
  doca_cut = 0.10
  entry = entry + 1
  nPVs = npvs( event ) 
  found_signal = False
  print( f"{entry} {nPVs} {len(good_pions)} {len(good_kaons)}")
  phi_candidates = ROOT.combine( kp, km, doca_cut, 15, 0)
  for pion in good_pions : 
    for k1,k2,phi,phi_vtx in phi_candidates: 
      ds_vtx = ROOT.uVertex( [k1,k2,pion] )
      ds     = ROOT.uParticle( [k1,k2,pion] )
      is_signal = is_from(k1, event, 431) and is_from(k2, event, 431) and is_from(pion, event,431)
      vtx_chi2.Fill( ds_vtx.chi2 / ds_vtx.ndof, is_signal ) 
      if ds_vtx.chi2 / ds_vtx.ndof > 5 : continue
      if k1.pt() + k2.pt() + pion.pt() < 1800 : continue
      if ds.mass < 1800 or ds.mass  > 2100 : continue 

      pv  = ds.bpv_4d( event.Vertices ) 

#      vtx_chi2.Fill( ds_vtx.chi2_distance(pv), is_signal )
      if ds_vtx.chi2_distance(pv) < 50 : continue
      if dira_bpv(ds,event.Vertices,0.050)  < 0.9 : continue 

      # if is_signal : 
      plot.Fill( ds.mass * 0.001)
      found_signal |= is_signal 
      if not is_signal : 
        print( "Background")
        print_mc_particle( k1, event.MCParticles) 
        print_mc_particle( k2, event.MCParticles) 
        print_mc_particle( pion, event.MCParticles) 

  n_signal = n_signal + found_signal 

canvas = ROOT.TCanvas("canvas")
canvas.cd()
plot.Draw()
canvas.Print("m_ds50.pdf")
# vtx_chi2.Draw()
#print( n_signal ) 
#      print( "mass: {}".format( ds.p4().mass()) )
#      print_mc_particle( pion, event.MCParticles )     
#      print_mc_particle( k1, event.MCParticles )     
#      print_mc_particle( k2, event.MCParticles )     
