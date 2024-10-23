import ROOT
from Selections import load_event_library
load_event_library()
from ROOT import uParticle
from ROOT import TFile, gSystem, gInterpreter
from ROOT import TH1D, TH2D, TCanvas, TChain
from math import * 
import sys
from os import path, listdir 

basedir=path.dirname(path.realpath(__file__))

class SigVsBkg:
  # Creates the signal vs background histograms
  
  def __init__(self, name, nBins, min, max):
    self.signal = ROOT.TH1D( name +"_signal","",nBins, min,max ) # initialises 1D histogram for signal
    self.background = ROOT.TH1D( name +"_bkg","",nBins, min,max) # initialises 1D histogram for the background
  def Fill( self, x, isSignal ) : 
    if isSignal : self.signal.Fill(x) # fills the signal histogram with values if it is the signal
    else:  self.background.Fill(x) # fills the background histogram with values if it is the background
  def Draw(self ) : # Draws the histogram
    self.signal.Scale( 1 / self.signal.Integral() )  # Normalises the histogram
    self.background.Scale( 1 / self.background.Integral() ) 
    self.signal.Draw() # Draws signal onto the canvas
    self.background.SetLineColor(ROOT.kRed)
    self.background.Draw("same") # Draws the background onto the same canvas as the signal used

def dira_bpv( particle, vertices, max_dt):

  # bpv means best possible vertex
  # cos(Angle) between the momentum vector and the line of the orignal momentum connecting the decay vertex and the primary vertex
  # cosine of the angle between the angle momentum and trajectory vectors is the direction angle (DIRA)
  vertex = vertices[0] # First vertex, is the primary vertex
  
  ipw = lambda particle, vertex : particle.ip(vertex) if particle.ip_t(vertex) < max_dt else 9999
  # consider a vertex passed to the function. Consider particles and find if its possible they came from the vertex
  # based on the "time" between the measurements. If possible return the time betweem the hit and the vertex
  
  ip = ipw(particle, vertex ) # save the ipw of the vertex being analysed
  for index in range(1, len(vertices ) ) : # runs through all the verticies 
    if ipw(particle, vertices[index]) < ip : # if the time is lower than the maximum allowed time save the vertex
      vertex = vertices[index] # saves the vertex
      ip = particle.ip(vertices[index]) # now take this as the best vertex and repeat until you have the best estimate
  dx = particle.firstState.x0 - vertex.x 
  dy = particle.firstState.y0 - vertex.y 
  dz = particle.firstState.z  - vertex.z
  p = particle.p4() # creates four vector of the decay particle
  
  # cos(Angle) between the momentum vector and the line of the orignal momentum connecting the decay vertex and the primary vertex
  return (dx * p.x() + dy * p.y() + dz * p.z() ) / sqrt( (dx**2 + dy**2 + dz**2 )*p.P2() ) 

sys.path.insert(0,basedir) 
from MCTools import * 
gInterpreter.AddIncludePath( f'{basedir}/../include')
gSystem.Load( f'{basedir}/../build/libEvent.so') # add the event library to the python path

events = TChain("Events") # connects all the events into a single data set

# can be changed to look at different timing resolutions and detector geometries
dir="/disk/moose/general/djdt/lhcbUII_masters/dataStore/Beam7000GeV-md100-nu38-VerExtAngle_vpOnly/13264021/VP_U2_ParamModel-SX/SX_10um50s_75umcylindr3p5_nu38_Bs2Dspi_2111/moore/"
onlyfiles = [f for f in listdir(dir) if path.isfile(path.join(dir, f))]
#print(onlyfiles)
#for file in onlyfiles : 
#events.AddFile( "root://eoslhcb.cern.ch//" + path.join(dir, file) ) 
events.AddFile( path.join(dir, onlyfiles[1]) )  # Look at a file in the target directory for analysis
#print(path.join(dir, onlyfiles[1]))

entry=0
plot = ROOT.TH1D("m_ds","",100,1.8,2.1) # initiates the mass plot
vtx_chi2 = SigVsBkg("vtx_chi2",100,2,3) # initiates the signal vs background plot
b_plot = ROOT.TH1D("m_bs","",100,1.8,9)
b_vtx_chi2 = SigVsBkg("b_vtx_chi2",100,2,3)

n_signal=0

for event in events: # loop through all events
  
  # scaled_tracks = []
  # for track in event.Particles : 
  #   track.scale_uncertainty(1, 5)   
  #   scaled_tracks.append( track ) 
  
  displaced_tracks = ROOT.select( event.Particles, event.Vertices, 250, 1500, 6 ) # select particles, verticies, min_pt, min_p,min_ipChi2_4d
  # selects acceptable particles for analysis

  # print( "{} {}".format( scaled_tracks[0].firstState.cov(5,5), event.Particles[0].firstState.cov(5,5) ) ) 

  good_pions = [ track for track in displaced_tracks if abs( track.trueID ) == 211] # narrows particels to only good pions or
  good_kaons = [ track for track in displaced_tracks if abs( track.trueID ) == 321] #  good kaons
  kp = [track for track in good_kaons if track.charge() > 0 ] # positively charged kaons
  km = [track for track in good_kaons if track.charge() < 0 ] # positively charged kaons
  doca_cut = 0.10 # distance of closest approach cutoff, maximum allowed closest approach for consideration
  entry = entry + 1 # entry is the event being examined
  nPVs = npvs( event ) # the number of primary verticies in an event
  found_signal = False # placeholder for when a signal is found, default of no signal found
  #print( f"{entry} {nPVs} {len(good_pions)} {len(good_kaons)}") # prints event information
  phi_candidates = ROOT.combine( kp, km, doca_cut, 15, 0) # inputs: all kp, all km, doca_max, chi2ndf_max, charge
  # returns:  four momenta of particle1, particle2 , a combined particle, and the vertex where combination occurs

  # create all phi candiates, two particles at a distance smaller than the maximum allowed distance, with acceptable chi2ndf and sum
  # to a charge of 0
  for pion in good_pions : 
    for k1,k2,phi,phi_vtx in phi_candidates: 
      # k1 is the four momenta of the positive kaons, k2 is the four momenta of the negative kaons, phi is the combined particle
      # created by the kaons, and phi_vtx is the vertex in which the combination occurs

      ds_vtx = ROOT.uVertex( [k1,k2,pion] ) # create a new vertex, using momentum of the first kaon or second kaon and a pion as
      # these recombine to create a B0 (see diagram)

      ds = ROOT.uParticle( [k1,k2,pion] ) # create a candiate particle for reconstruction. using either positive or negative kaon
      # and a pion

      is_signal = is_from(k1, event, 431) and is_from(k2, event, 431) and is_from(pion, event,431)
      # particle id 431 is for the D+, checks if the positive kaon is from an event with a D+ present, checks if the negative 
      # kaon is from an event with a D+ present, checks if the pions are from events with D+ present. (See diagram)
      
      vtx_chi2.Fill( ds_vtx.chi2 / ds_vtx.ndof, is_signal) # Fills the chi2 graph for the candiate signal 
      if ds_vtx.chi2 / ds_vtx.ndof > 5 : continue # if the chi2/ndf is not acceptable, disgard possible particle
      if k1.pt() + k2.pt() + pion.pt() < 1800 : continue # insufficient momentum to create a phi, discard
      if ds.mass < 1800 or ds.mass  > 2100 : continue # insufficient mass to create D particle, discard

      pv  = ds.bpv_4d( event.Vertices ) # pv: possible vertex, finds best possible vertex for the considered
      # particle (minimum Chi squared) 

#      vtx_chi2.Fill( ds_vtx.chi2_distance(pv), is_signal )
      if ds_vtx.chi2_distance(pv) < 50 : continue # if the product of the Chi squareds of the particle and the vertex
      # is greater than 50, discard
      if dira_bpv(ds,event.Vertices,0.050)  < 0.9 : continue # if the cos of the angle between momenta is less than 0.9 discard
      
      # dm_candidate = ROOT.combine( ds, pi, doca_cut, 15, -1)
      for pion2 in good_pions:
          bs_vtx = ROOT.uVertex( [ds, pion2] )
          bs = ROOT.uParticle( [ds,pion2] )
          is_b_signal = is_from(ds, event, 431) and is_from(pion2, event,431)

          b_vtx_chi2.Fill( bs_vtx.chi2 / bs_vtx.ndof, is_b_signal)
          if bs_vtx.chi2 / bs_vtx.ndof > 5 : continue # if the chi2/ndf is not acceptable, disgard possible particle
          if ds.pt() + pion2.pt() < 1800 : continue # insufficient momentum to create a phi, discard
          if bs.mass < 1800 or bs.mass  > 9000 : continue

          b_pv  = bs.bpv_4d( event.Vertices )
          if bs_vtx.chi2_distance(b_pv) < 50 : continue 
          if dira_bpv(bs,event.Vertices,0.050)  < 0.9 : continue
          print(bs.mass)
          b_plot.Fill(bs.mass * 0.001)

      # if is_signal : 
      #plot.Fill(ds.mass * 0.001) # found the allowed D particle and adds to the mass plot (see equations)
      found_signal |= is_signal 
      # if not is_signal : # if not a signal its background, print this
        # print( "Background")
        # print_mc_particle( k1, event.MCParticles) 
        # print_mc_particle( k2, event.MCParticles) 
        # print_mc_particle( pion, event.MCParticles) 

  n_signal = n_signal + found_signal 


### Plotting

b_plot_canvas = ROOT.TCanvas("canvas")
b_plot_canvas.cd()
b_plot.Draw()
b_plot.Print("outputs/b_mass_plot.pdf")


#print( n_signal ) 
#      print( "mass: {}".format( ds.p4().mass()) )
#      print_mc_particle( pion, event.MCParticles )     
#      print_mc_particle( k1, event.MCParticles )     
#      print_mc_particle( k2, event.MCParticles )     
