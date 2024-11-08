from Selections import load_event_library 
load_event_library()

from ROOT import TFile, TH1D, TH2D, TCanvas, TChain
import ROOT
from math import * 
import sys
from os import path

basedir=path.dirname(path.realpath(__file__))
sys.path.insert(0,basedir) 
from MCTools import * 

events = TChain("Events")
events.AddFile("/eos/lhcb/user/t/tevans/public/VELOECAL/TimingScan/B2KstGamma_75ps_001_100.root")

# files = [
#    TFile("/eos/lhcb/user/t/tevans/public/VELOECAL/TimingScan/B2KstGamma_50ps_001_100.root","READ")
#    , TFile("/eos/lhcb/user/t/tevans/public/VELOECAL/TimingScan/B2KstGamma_50ps_001_100.root","READ")
#    , TFile("/eos/lhcb/user/t/tevans/public/VELOECAL/TimingScan/B2KstGamma_50ps_001_100.root","READ")
#    , TFile("/eos/lhcb/user/t/tevans/public/VELOECAL/TimingScan/B2KstGamma_50ps_001_100.root","READ") ]

hist_mB = TH1D("test_mB","; m(K^-\\pi^{+}\\gamma) [MeV/c^{2}]; \\text{Candidates} / 10 MeV /c^{2}",250,4900,5900)

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


def min_dist( particle, vertices ) :
  min_dist = 9999
  for v in vertices: 
    d = ( particle.firstState.x0 - v.x)**2 + ( particle.firstState.y0 - v.y)**2 + ( particle.firstState.z - vertex.z)**2 
    if d < min_dist : min_dist = d
  return sqrt( min_dist ) 

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

kstar_id = 313
b0_id    = 511

entry = 0 
counter = 0
counter_signal = 0
from_hf = 0
hist_displaced = ROOT.TH1D("ipchi2","",100,0,3) 
hist_all       = ROOT.TH1D("ipchi2_all","",100,0,3) 
hist_mkpi      = ROOT.TH1D("mkpi","",100,700,1000)
h_chi2_distance = SigVsBkg("chi2-distance",100,0,100)
p = SigVsBkg("p",100,0,250)
pt= SigVsBkg("pt",100,0,25)
eff_vs_npvs = ROOT.TEfficiency("eff_vs_npvs_num","",20,0.5,80.5)
npvs_den = ROOT.TH1D("npvs_den","",20,0.5,80.5)
res_t = ROOT.TH1D("res_t",";t - t_{true} [ns]; Entries",100,-150.0,150)

for event in events: 
  displaced_tracks = ROOT.select( event.Particles, event.Vertices, 500, 2500, 6 )

  #displaced_tracks = [ track for track in event.Particles if ( track.pt() > 500 and track.p() > 2500) and track.min_ipchi2_4d( event.Vertices) > 6.0  ]
  good_pions = [ track for track in displaced_tracks if abs( track.trueID ) == 211]
  good_kaons = [ track for track in displaced_tracks if abs( track.trueID ) == 321]
  
  doca_cut = 0.2 
  entry = entry + 1
  nPVs = npvs( event ) 
  found_signal = False
  kst_candidates = ROOT.combine( good_kaons, good_pions, doca_cut, 10, 0 )
  for kaon, pion, kpi, kpi_vtx in kst_candidates :
    
    kaon_at_vtx = ROOT.TrackState( kaon.firstState, kpi_vtx.z )
    pion_at_vtx = ROOT.TrackState( pion.firstState, kpi_vtx.z )
    dt = kaon_at_vtx.t - pion_at_vtx.t
  
    signal = is_from(kaon, event, kstar_id) and \
             is_from(pion, event, kstar_id)
  
    if kpi.mass < 700 or kpi.mass > 1000  : continue
    pv  = kpi.bpv_4d( event.Vertices ) 
    chi2_distance = kpi_vtx.chi2_distance(pv)
    
    dira = dira_bpv(kpi, event.Vertices, 0.050) 
    if not signal : hist_all.Fill( kpi.ip(pv) ) 
    else:  hist_displaced.Fill( kpi.ip(pv)  ) 
    if kpi.p4().P() < 7500 or kpi.p4().pt() < 2000 : continue 
    if dira < 0.99 or chi2_distance < 10 : continue
    counter = counter+1
  
    if signal : 
      found_signal = True
      counter_signal = counter_signal + 1 
      true_vtx      = true_origin_vertex( kaon, event )
      true_vtx_pion = true_origin_vertex( pion, event )
      if true_vtx != None and true_vtx.pos == true_vtx_pion.pos:
        res_t.Fill( 1000 * ( kpi_vtx.t - true_vtx.pos.t() ) )
    
      for i in range(0,5) : 
        print( "{} {} {} {} {}".format(kaon.firstState.cov(i,0), kaon.firstState.cov(i,1), kaon.firstState.cov(i,2), kaon.firstState.cov(i,3), kaon.firstState.cov(i,4)  ) )
    hist_mkpi.Fill( kpi.mass )
    fromBC = from_charm(kaon, event) or from_charm(pion, event) or \
             from_beauty(kaon, event) or from_beauty(pion, event)
  
    h_chi2_distance.Fill(chi2_distance, not fromBC )
    p.Fill( kpi.p4().P()/1000, signal )
    pt.Fill( kpi.p4().pt()/1000, signal )
    if not signal:
      if fromBC:
        from_hf = from_hf + 1 
      else: 
        print_mc_particle( kaon, event.MCParticles ) 
        print_mc_particle( pion, event.MCParticles )
  npvs_den.Fill( nPVs ) 
  eff_vs_npvs.Fill( found_signal, nPVs )
  print ("{} {} {}".format(entry, found_signal, nPVs) )
print( "nSignal = {} ; total = {}; from C, B= {}".format(counter_signal, counter, from_hf) )
canvas = TCanvas("c1","",1000,800)
# hist_mkpi.Draw()
# canvas.Divide(2,2)
# canvas.cd(1)
# h_chi2_distance.Draw()
# canvas.cd(2)
# p.Draw()
# canvas.cd(3)
# pt.Draw()
res_t.Draw() 
res_t.Fit("gaus")
# npvs_den.Draw()
# 
# hist_displaced.Draw()
# hist_all.SetLineColor(2)
# hist_all.Draw("same")
