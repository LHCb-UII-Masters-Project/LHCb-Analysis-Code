import ROOT
from Selections import load_event_library
load_event_library()
from ROOT import uParticle
from ROOT import TFile, gSystem, gInterpreter
from ROOT import TH1D, TH2D, TCanvas, TChain, TRandom
import time
from math import * 
import pandas as pd
import sys
import numpy as np
from os import path, listdir
import os
# Random number generator for introducing the detector efficiency
rand = ROOT.TRandom() # creates a random number engine
rand.SetSeed(int(time.time() * os.getpid())) # sets the random number engine to be time dependent and dependent
# on the process id - ensures randomness when ran in batch

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
for index,file in enumerate(onlyfiles, start=0):
  if index < 2:
    #events.AddFile( "root://eoslhcb.cern.ch//" + path.join(dir, file) ) 
    events.AddFile( path.join(dir, file) )  # Look at a file in the target directory for analysis
    print(path.join(dir, file))

entry=0
plot = ROOT.TH1D("m_ds","",100,1.8,2.1) # initiates the mass plot
vtx_chi2 = SigVsBkg("vtx_chi2",100,2,3) # initiates the signal vs background plot
b_plot = ROOT.TH1D("m_bs","",100,5.25,5.45)
b_plot.SetTitle("Reconstructed B^s Mass Plot " + "2") # Insert global variable here
b_plot.GetXaxis().SetTitle("Mass (MeV/c^2)")
b_plot.GetYaxis().SetTitle("Frequency")
b_vtx_chi2 = SigVsBkg("b_vtx_chi2",100,2,3)

n_signal=0


def eff_model(df):
  x, y = np.array(df.iloc[:, 0].astype(float)), np.array(df.iloc[:, 1].astype(float))
  scatter_plot = ROOT.TGraph(len(x), x, y)
  linear_function = ROOT.TF1("linear_function", "[0] + [1]*x", np.min(x), np.max(x))
  scatter_plot.Fit(linear_function)
  return(linear_function.GetParameter(0), linear_function.GetParameter(1))

if True == False:
  t_res_str = "300"
  boundaries = [3.3,10, 30, 60, 100]
else:
  t_res_str = "150"
  boundaries = [5, 30, 80, 200, 201]

r1_model = eff_model(pd.read_csv('PEff Kaons_'+t_res_str+'/Region 1.csv', skiprows=1))
r2_model = eff_model(pd.read_csv('PEff Kaons_'+t_res_str+'/Region 2.csv', skiprows=1))
r3_model = eff_model(pd.read_csv('PEff Kaons_'+t_res_str+'/Region 3.csv', skiprows=1))
r4_model = eff_model(pd.read_csv('PEff Kaons_'+t_res_str+'/Region 4.csv', skiprows=1))
r5_model = eff_model(pd.read_csv('PEff Kaons_'+t_res_str+'/Region 5.csv', skiprows=1))

for event in events: # loop through all events
  
  # scaled_tracks = []
  # for track in event.Particles : 
  #   track.scale_uncertainty(1, 5)   
  #   scaled_tracks.append( track ) 
  
  displaced_tracks = ROOT.select( event.Particles, event.Vertices, 250, 1500, 6 ) # select particles, verticies, min_pt, min_p,min_ipChi2_4d
  # selects acceptable particles for analysis

  # print( "{} {}".format( scaled_tracks[0].firstState.cov(5,5), event.Particles[0].firstState.cov(5,5) ) ) 

  good_pions = [ track for track in displaced_tracks if abs( track.trueID ) == 211 and int(rand.Integer(100))!=12 ] # 99/100 dertection chance
  bad_pions = [ track for track in displaced_tracks if abs( track.trueID ) != 211 and int(rand.Integer(100))==23 ] # 1/100 chance of a misconstructed "pion"
  pions = good_pions + bad_pions
  
  unadjusted_good_kaons = [ track for track in displaced_tracks if abs( track.trueID ) == 321] # all kaons
  good_kaons = [] # initialised list to be filled with good kaons
  for kaon in unadjusted_good_kaons:
    k_p = np.sqrt((kaon.p4().Px())**2 + (kaon.p4().Py())**2 + (kaon.p4().Pz())**2) # calculate the kaon momentum
    # Adjust conditions and use nested conditionals for efficiency
    if k_p < boundaries[0]*(10**3) and int(rand.Rndm()) <= (r1_model[1] * k_p + r1_model[0]):
        good_kaons.append(kaon)
    elif boundaries[0]*(10**3) <= k_p < boundaries[1]*(10**3) and int(rand.Rndm()) <= (r2_model[1] * k_p + r2_model[0]):
        good_kaons.append(kaon)
    elif boundaries[1]*(10**3) <= k_p and k_p < boundaries[2]*(10**3) and int(rand.Rndm()) <= (r3_model[1] * k_p + r3_model[0]):
        good_kaons.append(kaon)
    elif boundaries[2]*(10**3) <= k_p and k_p < boundaries[3]*(10**3) and int(rand.Rndm()) <= (r4_model[1] * k_p + r4_model[0]):
        good_kaons.append(kaon)
    elif boundaries[3]*(10**3) <= k_p and k_p < boundaries[4]*(10**3) and int(rand.Rndm()) <= (r5_model[1] * k_p + r5_model[0]):
        good_kaons.append(kaon)
    else:
       continue
 
  kp = [track for track in good_kaons if track.charge() > 0 ] # positively charged kaons
  km = [track for track in good_kaons if track.charge() < 0 ] # positively charged kaons
  doca_cut = 0.10 # distance of closest approach cutoff, maximum allowed closest approach for consideration
  
  nPVs = npvs( event ) # the number of primary verticies in an event
  found_signal = False # placeholder for when a signal is found, default of no signal found
  #print( f"{entry} {nPVs} {len(pions)} {len(good_kaons)}") # prints event information
  phi_candidates = ROOT.combine( kp, km, doca_cut, 15, 0) # inputs: all kp, all km, doca_max, chi2ndf_max, charge
  # returns:  four momenta of particle1, particle2 , a combined particle, and the vertex where combination occurs

  # create all phi candiates, two particles at a distance smaller than the maximum allowed distance, with acceptable chi2ndf and sum
  # to a charge of 0
  for pion in pions : 
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
      for pion2 in pions:
          bs_vtx = ROOT.uVertex( [ds, pion2] )
          bs = ROOT.uParticle( [ds,pion2] )
          is_b_signal = is_from(ds, event, 431) and is_from(pion2, event,431)

          b_vtx_chi2.Fill( bs_vtx.chi2 / bs_vtx.ndof, is_b_signal)
          if bs_vtx.chi2 / bs_vtx.ndof > 5 : continue # if the chi2/ndf is not acceptable, disgard possible particle
          if ds.pt() + pion2.pt() < 5000 : continue # insufficient momentum to create a phi, discard
          if bs.mass < 5250 or bs.mass  > 5450 : continue

          b_pv  = bs.bpv_4d( event.Vertices )
          if bs_vtx.chi2_distance(b_pv) < 50 : continue 
          if dira_bpv(bs,event.Vertices,0.050)  < 0.9 : continue
          b_plot.Fill(bs.mass * 0.001)
          entry = entry + 1 # entry is the event being examined

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
b_plot_canvas.Print("outputs/b_mass_plot " + time.strftime("%d-%m-%y %H:%M:%S", time.localtime()) + ".pdf")
# Insert global time resolution variable here


#print( n_signal ) 
#      print( "mass: {}".format( ds.p4().mass()) )
#      print_mc_particle( pion, event.MCParticles )     
#      print_mc_particle( k1, event.MCParticles )     
#      print_mc_particle( k2, event.MCParticles )     
