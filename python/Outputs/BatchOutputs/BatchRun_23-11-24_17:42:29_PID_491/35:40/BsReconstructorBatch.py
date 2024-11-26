#region IMPORTS
import ROOT
from Selections import load_event_library
load_event_library()
from ROOT import uParticle
from ROOT import TFile, gSystem, gInterpreter
from ROOT import TH1D, TH2D, TCanvas, TChain, TTree, TString, TFile
import time
from math import * 
import pandas as pd
import sys
import numpy as np
from os import path, listdir
import os
from array import array
import re
import sys

# endregion IMPORTS

#region RunParams
RunParams = ROOT.TTree("fit_parameters", "Fit Parameters Tree")
file_number = array('f', [0])
RunParams.Branch('file_number', file_number, 'file_number/F')
rand_seed = array('f', [0])
RunParams.Branch('rand_seed', rand_seed, 'rand_seed/F')
rand_seed = array('f', [0])
RunParams.Branch('rand_seed', rand_seed, 'rand_seed/F')
rich_window_timing = array('f', [0])
RunParams.Branch('rich_window_timing', rich_window_timing, 'rich_window_timing/F')
velo_timing = array('f', [0])
RunParams.Branch('velo_timing', velo_timing, 'velo_timing/F')
PID_pion = array('f', [0])
RunParams.Branch('PID_pion', PID_pion, 'PID_pion/F')
PID_kaon = array('f', [0])
RunParams.Branch('PID_kaon', PID_kaon, 'PID_kaon/F')
Doca_cut = array('f', [0])
RunParams.Branch('Doca_cut', Doca_cut, 'Doca_cut/F')
spacial_resolution = array('f', [0])
RunParams.Branch('spacial_resolution', spacial_resolution, 'spacial_resolution/F')
spacial_resolution[0] = 10
com_energy = array('f', [0])
RunParams.Branch('com_energy', com_energy, 'com_energy/F')
com_energy[0] = 14
#endregion RunParams

#region RunLimts
RunLimits = ROOT.TTree("Run Limits", "Run Limits")
ds_chi2_ndf_limit = array('f', [0]) # Formerly Chi2_ndf_limit
RunLimits.Branch('ds_chi2_ndf_limit', ds_chi2_ndf_limit, 'ds_chi2_ndf_limit/F')
Pphi_limit = array('f', [0])
RunLimits.Branch('Pphi_limit', Pphi_limit, 'Pphi_limit/F')
Ds_mass_upper_limit = array('f', [0])
RunLimits.Branch('Ds_mass_upper_limit', Ds_mass_upper_limit, 'Ds_mass_upper_limit/F')
Ds_mass_lower_limit = array('f', [0])
RunLimits.Branch('Ds_mass_lower_limit', Ds_mass_lower_limit, 'Ds_mass_lower_limit/F')
D_chi2_distance_limit = array('f', [0])
RunLimits.Branch('D_chi2_distance_limit', D_chi2_distance_limit, 'D_chi2_distance_limit/F')
D_dira_limit = array('f', [0])
RunLimits.Branch('D_dira_limit', D_dira_limit, 'D_dira_limit/F')
B_chi2_ndf_limit = array('f', [0])
RunLimits.Branch('B_chi2_ndf_limit', B_chi2_ndf_limit, 'B_chi2_ndf_limit/F')
Pb_limit = array('f', [0])
RunLimits.Branch('Pb_limit', Pb_limit, 'Pb_limit/F')
B_mass_upper_limit = array('f', [0])
RunLimits.Branch('B_mass_upper_limit', B_mass_upper_limit, 'B_mass_upper_limit/F')
B_mass_lower_limit = array('f', [0])
RunLimits.Branch('B_mass_lower_limit', B_mass_lower_limit, 'B_mass_lower_limit/F')
B_chi2_distance_limit = array('f', [0])
B_dira_limit = array('f', [0])
RunLimits.Branch('B_dira_limit', B_dira_limit, 'B_dira_limit/F')
#endregion RunLimts

#region RunDiagnostics
RunDiagnostics = TTree("Run Diagnostics","Run Diagnostics")
Chi2_ndf_kills = array('f', [0])
RunDiagnostics.Branch('Chi2_ndf_kills', Chi2_ndf_kills, 'Chi2_ndf_kills/F')
D_chi2_distance_kills = array('f', [0])
RunDiagnostics.Branch('D_chi2_distance_kills', D_chi2_distance_kills, 'D_chi2_distance_kills/F')
bs_chi2_distance_kills = array('f', [0])
RunDiagnostics.Branch('bs_chi2_distance_kills', bs_chi2_distance_kills, 'bs_chi2_distance_kills/F')
bs_chi2_kills = array('f', [0])
RunDiagnostics.Branch('bs_chi2_kills', bs_chi2_kills, 'bs_chi2_kills/F')
#endregion RunDiagnostics

#region Outputs
Outputs = TTree("Run Diagnostics","Run Diagnostics")
b_sig = array('f', [0])
Outputs.Branch('b_sig', b_sig, 'b_sig/F')
Num_pions = array('f', [0])
Outputs.Branch('Num_pions', Num_pions, 'Num_pions/F')
Num_kaons = array('f', [0])
Outputs.Branch('Num_kaons', Num_kaons, 'Num_kaons/F')
Num_pions_detected = array('f', [0])
Outputs.Branch('Num_pions_detected', Num_pions_detected, 'Num_pions_detected/F')
Num_kaons_detected = array('f', [0])
Outputs.Branch('Num_kaons_detected', Num_kaons_detected, 'Num_kaons_detected/F')
Num_phi_candidates = array('f', [0])
Outputs.Branch('Num_Phi_candidates', Num_phi_candidates, 'Num_Phi_candidates/F')
Num_pv = array('f', [0])
Outputs.Branch('Num_pv', Num_pv, 'Num_pv/F')
ds_chi_ndf = array('f', [0])
Outputs.Branch('ds_chi_ndf', ds_chi_ndf, 'ds_chi_ndf/F')
k1_pt = array('f', [0])
Outputs.Branch('k1_pt', k1_pt, 'k1_pt/F')
k1_eta = array('f', [0])
Outputs.Branch('k1_eta', k1_eta, 'k1_eta/F')
k2_pt = array('f', [0])
Outputs.Branch('k2_pt', k2_pt, 'k2_pt/F')
k2_eta = array('f', [0])
Outputs.Branch('k2_eta', k2_eta, 'k2_eta/F')
pi1_pt = array('f', [0])
Outputs.Branch('pi1_pt', pi1_pt, 'pi1_pt/F')
pi1_eta = array('f', [0])
Outputs.Branch('pi1_eta', pi1_eta, 'pi1_eta/F')
pi1_ID = array('f', [0])
Outputs.Branch('pi1_ID', pi1_ID, 'pi1_ID/F')
ds_mass = array('f', [0])
Outputs.Branch('ds_mass', ds_mass, 'ds_mass/F')
ds_chi2_distance = array('f', [0])
Outputs.Branch('ds_chi2_distance', ds_chi2_distance, 'ds_chi2_distance/F')
ds_dira= array('f', [0])
Outputs.Branch('ds_dira', ds_dira, 'ds_dira/F')
bs_chi2_ndf= array('f', [0])
Outputs.Branch('bs_chi2_ndf', bs_chi2_ndf, 'bs_chi2_ndf/F')
bs_chi2_kills = array('f', [0])
Outputs.Branch('bs_chi2_kills', bs_chi2_kills, 'bs_chi2_kills/F')
ds_pt= array('f', [0])
Outputs.Branch('ds_pt', ds_pt, 'ds_pt/F')
ds_eta = array('f', [0])
Outputs.Branch('ds_eta', ds_eta, 'ds_eta/F')
pi2_pt= array('f', [0])
Outputs.Branch('pi2_pt', pi2_pt, 'pi2_pt/F')
pi2_eta = array('f', [0])
Outputs.Branch('pi2_eta', pi2_eta, 'pi2_eta/F')
bs_mass= array('f', [0])
Outputs.Branch('bs_mass', bs_mass, 'bs_mass/F')
bs_chi2_distance= array('f', [0])
Outputs.Branch('bs_chi2_distance', bs_chi2_distance, 'bs_chi2_distance/F')
bs_dira= array('f', [0])
Outputs.Branch('bs_dira', bs_dira, 'bs_dira/F')
num_bs= array('f', [0])
Outputs.Branch('num_bs', num_bs, 'num_bs/F')
#endregion Outputs

#region USERINPUTS

def get_arg(index, default, args):  # Arg function that returns relevant arguments and deals with missing args
    try:
        return int(args[index])
    except (IndexError, ValueError, TypeError):
        return default

args = sys.argv
lower = get_arg(1, 0, args)  # Default timing argument if not provided
upper = get_arg(2, 2, args)  # Default timing argument if not provided
rich_timing = get_arg(3, 300, args)  # Default timing argument if not provided
velo_time = get_arg(4, 200, args)  # Default velo time argument if not provided
pid_switch = get_arg(5, 1, args)  # Default PID switch argument if not provided
kaon_switch = get_arg(6, 1, args)  # Default Kaon switch argument if not provided
run_size = args[7]  # Run size determines which event directory is read from
rand_seed_arg = get_arg(8, int(time.time() * os.getpid()), args)  # Default random seed if not provided

# Set tree values from user inputs
rich_window_timing[0] = rich_timing
velo_timing[0] = velo_time
rand_seed[0] = rand_seed_arg
PID_pion[0] = pid_switch
PID_kaon[0] = kaon_switch

# File is run in different place when batching and when not
if path.dirname(path.realpath(__file__))[-6:] == "python": # Checks if path ends in "python"
  basedir=path.dirname(path.realpath(__file__))
  sys.path.append(f"{path.dirname(path.realpath(__file__))}/..")
  batching = False
else:
  basedir = f"{path.dirname(path.realpath(__file__))}/../../../.."
  sys.path.append(f"{path.dirname(path.realpath(__file__))}/../../../..")
  batching = True

#endregion USERINPUTS

#region RANDOM NUMBER GENERATOR
rand = ROOT.TRandom() # creates a random number engine
rand.SetSeed(rand_seed_arg)
#endregion RANDOM NUMBER GENERATOR

#region FUNCTION DEFINITIONS
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

def get_file_number(file_name):
  """Takes the full file name and returns the number (what changes between each files)"""
  # Use regex to find the number after "4d-"
  match = re.search(r"4d-(\d+)", file_name)
  if match:
      # Return the matched number as an integer
      return int(match.group(1))
  else:
      return None  # Return None if the pattern is not found

def eff_model(df):
  x, y = np.array(df['Momentum'].astype(float))*(10**3), np.array(df['Efficiency'].astype(float))
  scatter_plot = ROOT.TGraph(len(x), x, y)
  linear_function = ROOT.TF1("linear_function", "[0] + [1]*x", np.min(x), np.max(x))
  scatter_plot.Fit(linear_function)
  return(linear_function.GetParameter(0), linear_function.GetParameter(1))

#endregion FUNCTION DEFINITIONS

#region FILE READING

sys.path.insert(0,basedir) 
from MCTools import * 
gInterpreter.AddIncludePath( f'{basedir}/../include')
gSystem.Load( f'{basedir}/../build/libEvent.so') # add the event library to the python path

events = TChain("Events") # connects all the events into a single data set

if run_size == "Large":
  # If using the large directory, have to filter to just the files we're interested in
  dir=f"/disk/moose/lhcb/djdt/u2_globopt/Beam7000GeV-md100-nu38-VerExtAngle_vpOnly/13264021/VP_U2_ParamModel-SX/SX_10um{velo_time}s_75umcylindr3p5_nu38_Bs2Dspi_2111/moore/"
  onlyfiles = [f for f in listdir(dir) if path.isfile(path.join(dir, f))]

  pattern = r"U2Tuple_u2_250um_4d-(\d+)-SX_10um\d+s_75umcylindr3p5_nu38_Bs2Dspi_\d+\.root"
  # All relevant files contain this string

  # Process the filenames
  onlyfileslive = []  # ;)
  for filename in onlyfiles:
    match = re.match(pattern, filename)
    if match:
      onlyfileslive.append(filename)
  onlyfiles = onlyfileslive
else:
  dir=f"/disk/moose/general/djdt/lhcbUII_masters/dataStore/Beam7000GeV-md100-nu38-VerExtAngle_vpOnly/13264021/VP_U2_ParamModel-SX/SX_10um{velo_time}s_75umcylindr3p5_nu38_Bs2Dspi_2111/moore/"
  onlyfiles = [f for f in listdir(dir) if path.isfile(path.join(dir, f))]

onlyfiles = onlyfiles[int(lower):int(upper)]
# Since list is formed in order for every run, this selects the relevant files to be run

for file in onlyfiles:
  events.AddFile( path.join(dir, file) )  # Look at a file in the target directory for analysis
entry=0
plot = ROOT.TH1D("m_ds","",100,1.8,2.1) # initiates the mass plot
vtx_chi2 = SigVsBkg("vtx_chi2",100,2,3) # initiates the signal vs background plot
b_plot = ROOT.TH1D("m_bs","",100,5.1,5.6)
b_plot.SetTitle("Reconstructed B^s Mass Plot t = " + str(rich_timing)) 
b_plot.GetXaxis().SetTitle("Mass (MeV/c^2)")
b_plot.GetYaxis().SetTitle("Frequency")

d_plot = ROOT.TH1D("m_ds","",100,5.1,5.6)
d_plot.SetTitle("Reconstructed d^s Mass Plot t = " + str(rich_timing)) 
d_plot.GetXaxis().SetTitle("Mass (MeV/c^2)")
d_plot.GetYaxis().SetTitle("Frequency")
b_vtx_chi2 = SigVsBkg("b_vtx_chi2",100,2,3)

n_signal=0

#endregion FILE READING

#region DETECTOR EFFICIENCY

eff_directory = os.path.join(basedir, f'Inputs/PEff Kaons_{rich_timing}')
# List all file paths
eff_dfs = [pd.read_csv(os.path.join(eff_directory, file)) for file in sorted(os.listdir(eff_directory))]
boundaries = np.array([eff_dfs[i]['Momentum'][0].astype(float) for i in range(1,len(eff_dfs))])*(10**3)

models = [eff_model(eff_dfs[0]), eff_model(eff_dfs[1]), eff_model(eff_dfs[2]), eff_model(eff_dfs[3]), eff_model(eff_dfs[4]) if rich_timing == 300 else None]

#endregion DETECTOR EFFICIENCY

#region EVENT LOOP

file_number[0] = 0 #  Initialises run number so += 1 can be used in event loop
current_file_name = "" #  Sets to empty string so first event loop changes it

for event in events: # loop through all events

  if events.GetFile().GetName() != current_file_name: #  If no longer in same file as before
    current_file_name = events.GetFile().GetName() #  Set file name to be the name of current file
    file_number[0] = get_file_number(current_file_name) #  Changes the file number to the new file number
    print(f"Current file name: \n{current_file_name} \nCurrent file number: \n{file_number[0]}")

  # scaled_tracks = []
  # for track in event.Particles : 
  #   track.scale_uncertainty(1, 5)   
  #   scaled_tracks.append( track ) 
  
  displaced_tracks = ROOT.select( event.Particles, event.Vertices, 250, 1500, 6 ) # select particles, verticies, min_pt, min_p,min_ipChi2_4d
  # selects acceptable particles for analysis

  # print( "{} {}".format( scaled_tracks[0].firstState.cov(5,5), event.Particles[0].firstState.cov(5,5) ) ) 
  total_pions = [track for track in displaced_tracks if abs( track.trueID ) == 211]
  # Uses proccess ID inefficiency if turned on, else keep all displaced pions and doesn't add misconstructs
  if pid_switch == 1:
    good_pions = [ track for track in displaced_tracks if abs( track.trueID ) == 211 and int(rand.Integer(100))!=12 ] # 99/100 dertection chance
    bad_pions = [ track for track in displaced_tracks if abs( track.trueID ) != 211 and int(rand.Integer(100))==23 ] # 1/100 chance of a misconstructed "pion"
    pions = good_pions + bad_pions
  elif pid_switch == 0: 
    pions = [ track for track in displaced_tracks if abs( track.trueID ) == 211] # 100% detection

  Num_pions[0] = len(total_pions)
  Num_pions_detected[0] = len(pions)
  
  all_kaons = [ track for track in displaced_tracks if abs( track.trueID ) == 321] # all kaons
  good_kaons = [] # initialised list to be filled with good kaons
  if kaon_switch == 1:
    for kaon in all_kaons:
      k_p = np.sqrt((kaon.p4().Px())**2 + (kaon.p4().Py())**2 + (kaon.p4().Pz())**2) # calculate the kaon momentum
      for i in range(len(boundaries)):
        # Finds appropriate model and uses rand number to apply efficiency  in that region
        if (boundaries[i-1] if i > 0 else 0) <= k_p < (boundaries[i] if i != len(boundaries) else np.inf) and (rand.Rndm()) <= (models[i][1] * k_p + models[i][0]):
          good_kaons.append(kaon)
          break
  else: 
    good_kaons = all_kaons

  Num_kaons[0] = len(all_kaons)
  Num_kaons_detected[0] = len(good_kaons)

  kp = [track for track in good_kaons if track.charge() > 0 ] # positively charged kaons
  km = [track for track in good_kaons if track.charge() < 0 ] # positively charged kaons
  doca_cut = 0.10 # distance of closest approach cutoff, maximum allowed closest approach for consideration
  Doca_cut[0] = doca_cut

  nPVs = npvs( event ) # the number of primary verticies in an event
  Num_pv[0] = nPVs
  found_signal = False # placeholder for when a signal is found, default of no signal found
  found_b_signal = False
  #print( f"{entry} {nPVs} {len(pions)} {len(good_kaons)}") # prints event information
  phi_candidates = ROOT.combine( kp, km, doca_cut, 15, 0) # inputs: all kp, all km, doca_max, chi2ndf_max, charge
  # returns:  four momenta of particle1, particle2 , a combined particle, and the vertex where combination occurs
  Num_phi_candidates[0] = len(phi_candidates)
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
      
      ds_chi_ndf[0] = ds_vtx.chi2 / ds_vtx.ndof
      k1_pt[0] = k1.pt()
      k1_eta[0] = k1.eta()
      k2_pt[0] = k2.pt()
      k2_eta[0] = k2.eta()
      pi1_pt[0] = pion.pt()
      pi1_eta[0] = pion.eta()
      pi1_ID[0] = abs(pion.trueID)
      ds_chi2_ndf_limit[0] = 5 # Formerly Chi2_ndf_limit
    
      if ds_vtx.chi2 / ds_vtx.ndof > 5 : 
        Chi2_ndf_kills[0] += 1
        continue # if the chi2/ndf is not acceptable, disgard possible particle
      Pphi_limit[0] = 1800
      if k1.pt() + k2.pt() + pion.pt() < 1800 : continue # insufficient momentum to create a phi, discard
      Ds_mass_lower_limit[0] = 1800
      Ds_mass_upper_limit[0] = 2100
      if ds.mass < 1800 or ds.mass  > 2100 : continue # insufficient mass to create D particle, discard

      pv  = ds.bpv_4d( event.Vertices ) # pv: possible vertex, finds best possible vertex for the considered
      # particle (minimum Chi squared) 

      ds_chi2_distance[0] = ds_vtx.chi2_distance(pv)
      ds_dira[0] = dira_bpv(ds,event.Vertices,0.050)

#     vtx_chi2.Fill( ds_vtx.chi2_distance(pv), is_signal )
      D_chi2_distance_limit[0] = 50
      if ds_vtx.chi2_distance(pv) < 50 : 
        D_chi2_distance_kills[0] += 1
        continue # if the product of the Chi squareds of the particle and the vertex
      # is greater than 50, discard
      B_dira_limit[0] = 0.9
      if dira_bpv(ds,event.Vertices,0.050)  < 0.9 : continue # if the cos of the angle between momenta is less than 0.9 discard
      
      ds_mass[0] = ds.mass
      ds_pt[0] = ds.pt()
      ds_eta[0] = ds.eta()
      d_plot.Fill(ds.mass*0.001)
      # dm_candidate = ROOT.combine( ds, pi, doca_cut, 15, -1)
      for pion2 in pions:
          if pion2 is not pion:
            bs_vtx = ROOT.uVertex( [pion, k1, k2, pion2] )
            bs = ROOT.uParticle( [pion, k1, k2, pion2] )
            is_b_signal = is_from(k1, event, 531) and is_from(k2, event, 531) and is_from(pion, event,531) and is_from(pion2, event,531)
            b_sig[0] = 1 if is_b_signal is True else 0
            
            bs_chi2_ndf[0] = bs_vtx.chi2 / bs_vtx.ndof
            pi2_pt[0] = pion2.pt()
            pi2_eta[0] = pion2.eta()

            b_vtx_chi2.Fill( bs_vtx.chi2 / bs_vtx.ndof, is_b_signal)
            B_chi2_ndf_limit[0] = 5
            if bs_vtx.chi2 / bs_vtx.ndof > 10 : 
              bs_chi2_kills[0] += 1
              continue # if the chi2/ndf is not acceptable, disgard possible particle
            Pb_limit[0] = 5000
            if ds.pt() + pion2.pt() < 5000 : continue # insufficient momentum to create a phi, discard
            B_mass_lower_limit[0] = 5100
            B_mass_upper_limit[0] = 5600
            if bs.mass < 5100 or bs.mass  > 5600 : continue

            b_pv  = bs.bpv_4d( event.Vertices )

            bs_chi2_distance[0] = bs_vtx.chi2_distance(b_pv) 
            bs_dira[0] = dira_bpv(bs,event.Vertices,0.050)

            B_chi2_distance_limit[0] = 100
            if bs_vtx.chi2_distance(b_pv) < 250 : 
              bs_chi2_distance_kills[0] += 1
              continue 
            B_dira_limit[0] = 0.9
            if dira_bpv(bs,event.Vertices,0.050)  < 0.9 : continue
            b_plot.Fill(bs.mass * 0.001)
            bs_mass[0] = bs.mass * 0.001
            entry += 1 # entry is the event being examined
            num_bs[0] = entry
            found_b_signal |= is_b_signal

      # if is_signal : 
      #plot.Fill(ds.mass * 0.001) # found the allowed D particle and adds to the mass plot (see equations)
      found_signal |= is_signal 
      # if not is_signal : # if not a signal its background, print this
        # print( "Background")
        # print_mc_particle( k1, event.MCParticles) 
        # print_mc_particle( k2, event.MCParticles) 
        # print_mc_particle( pion, event.MCParticles) 

  n_signal = n_signal + found_signal 
  
  RunParams.Fill()
  RunLimits.Fill()
  RunDiagnostics.Fill()
  Outputs.Fill()


  
#tree.Show(5)
#print(tree.GetEntries())

#endregion EVENT LOOP

file = TFile(f"{basedir}/Outputs/Rich" + str(rich_timing) + "/PID" + str(pid_switch) + "/Velo" + str(velo_time) +  f"/Tree{lower}:{upper}" + ".root", "RECREATE")
# Creates temporary tree (deleted when trees are combined)
file.WriteObject(Outputs, "Outputs")
file.WriteObject(RunParams, "RunParams")
file.WriteObject(RunLimits, "RunLimits")
file.WriteObject(RunDiagnostics, "RunDiagnostics")
file.WriteObject(b_plot, "B_Histogram")
file.WriteObject(d_plot, "D_Histogram")
file.Close()
