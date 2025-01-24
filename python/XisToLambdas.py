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
RunParams = ROOT.TTree("RunParams", "RunParams")
file_number = array('f', [0])
RunParams.Branch('file_number', file_number, 'file_number/F')
rand_seed = array('f', [0])
RunParams.Branch('rand_seed', rand_seed, 'rand_seed/F')
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
Lambdac_mass= array('f', [0])
RunParams.Branch('Lambdac_mass', Lambdac_mass, 'Lambdac_mass/F')
com_energy[0] = 14
#endregion RunParams

#region RunLimts
RunLimits = ROOT.TTree("RunLimits", "RunLimits")
Lambda_chi2_limit = array('f', [0]) # Formerly Chi2_ndf_limit
RunLimits.Branch('Lambda_chi2_limit', Lambda_chi2_limit, 'Lambda_chi2_limit/F')
Lambdac_Pcomposite_limit = array('f', [0])
RunLimits.Branch('Lambdac_Pcomposite_limit', Lambdac_Pcomposite_limit, 'Lambdac_Pcomposite_limit/F')
Lambdac_mass_upper_limit = array('f', [0])
RunLimits.Branch('Lambdac_mass_upper_limit', Lambdac_mass_upper_limit, 'Lambdac_mass_upper_limit/F')
Lambdac_mass_lower_limit = array('f', [0])
RunLimits.Branch('Lambdac_mass_lower_limit', Lambdac_mass_lower_limit, 'Lambdac_mass_lower_limit/F')
Lambdac_chi2_distance_limit = array('f', [0])
RunLimits.Branch('Lambdac_chi2_distance_limit', Lambdac_chi2_distance_limit, 'Lambdac_chi2_distance_limit/F')
Lambdac_dira_limit = array('f', [0])
RunLimits.Branch('Lambdac_dira_limit', Lambdac_dira_limit, 'Lambdac_dira_limit/F')
Xi_chi2_limit = array('f', [0])
RunLimits.Branch('Xi_chi2_limit', Xi_chi2_limit, 'Xi_chi2_limit/F')
Xi_Pcomposite_limit = array('f', [0])
RunLimits.Branch('Xi_Pcomposite_limit', Xi_Pcomposite_limit, 'Xi_Pcomposite_limit/F')
Xi_mass_upper_limit = array('f', [0])
RunLimits.Branch('Xi_mass_upper_limit', Xi_mass_upper_limit, 'Xi_mass_upper_limit/F')
Xi_mass_lower_limit = array('f', [0])
RunLimits.Branch('Xi_mass_lower_limit', Xi_mass_lower_limit, 'Xi_mass_lower_limit/F')
Xi_chi2_distance_limit = array('f', [0])
Xi_dira_limit = array('f', [0])
RunLimits.Branch('Xi_dira_limit', Xi_dira_limit, 'Xi_dira_limit/F')
RunLimits.Branch('Lambdac_mass', Lambdac_mass, 'Lambdac_mass/F')
#endregion RunLimts

#region RunDiagnostics
RunDiagnostics = TTree("RunDiagnostics","RunDiagnostics")
Lambdac_Pcomposite_sig_kills = array('f', [0]) # Formerly Chi2_ndf_limit
RunDiagnostics.Branch('Lambdac_Pcomposite_sig_kills', Lambdac_Pcomposite_sig_kills, 'Lambdac_Pcomposite_sig_kills/F')
Lambdac_Pcomposite_bac_kills = array('f', [0]) # Formerly Chi2_ndf_limit
RunDiagnostics.Branch('Lambdac_Pcomposite_bac_kills', Lambdac_Pcomposite_bac_kills, 'Lambdac_Pcomposite_bac_kills/F')
Lambdac_mass_sig_kills = array('f', [0]) # Formerly Chi2_ndf_limit
RunDiagnostics.Branch('Lambdac_mass_sig_kills', Lambdac_mass_sig_kills, 'Lambdac_mass_sig_kills/F')
Lambdac_mass_bac_kills = array('f', [0]) # Formerly Chi2_ndf_limit
RunDiagnostics.Branch('Lambdac_mass_bac_kills', Lambdac_mass_bac_kills, 'Lambdac_mass_bac_kills/F')
Lambdac_mass2_sig_kills = array('f', [0]) # Formerly Chi2_ndf_limit
RunDiagnostics.Branch('Lambdac_mass2_sig_kills', Lambdac_mass2_sig_kills, 'Lambdac_mass2_sig_kills/F')
Lambdac_mass2_bac_kills = array('f', [0]) # Formerly Chi2_ndf_limit
RunDiagnostics.Branch('Lambdac_mass2_bac_kills', Lambdac_mass2_bac_kills, 'Lambdac_mass2_bac_kills/F')
Lambdac_chi2_sig_kills = array('f', [0])
RunDiagnostics.Branch('Lambdac_chi2_sig_kills', Lambdac_chi2_sig_kills, 'Lambdac_chi2_sig_kills/F')
Lambdac_chi2_bac_kills = array('f', [0])
RunDiagnostics.Branch('Lambdac_chi2_bac_kills', Lambdac_chi2_bac_kills, 'Lambdac_chi2_bac_kills/F')
Lambdac_chi2_distance_sig_kills = array('f', [0])
RunDiagnostics.Branch('Lambdac_chi2_distance_sig_kills', Lambdac_chi2_distance_sig_kills, 'Lambdac_chi2_distance_sig_kills/F')
Lambdac_chi2_distance_bac_kills = array('f', [0])
RunDiagnostics.Branch('Lambdac_chi2_distance_bac_kills', Lambdac_chi2_distance_bac_kills, 'Lambdac_chi2_distance_bac_kills/F')
Lambdac_dira_sig_kills = array('f', [0])
RunDiagnostics.Branch('Lambdac_dira_sig_kills', Lambdac_dira_sig_kills, 'Lambdac_dira_sig_kills/F')
Lambdac_dira_bac_kills = array('f', [0])
RunDiagnostics.Branch('Lambdac_dira_bac_kills', Lambdac_dira_bac_kills, 'Lambdac_dira_bac_kills/F')

Xi_sign_sig_kills = array('f', [0])
RunDiagnostics.Branch('Xi_sign_sig_kills', Xi_sign_sig_kills, 'Xi_sign_sig_kills/F')
Xi_sign_bac_kills = array('f', [0])
RunDiagnostics.Branch('Xi_sign_bac_kills', Xi_sign_bac_kills, 'Xi_sign_bac_kills/F')
Xi_chi2_sig_kills = array('f', [0])
RunDiagnostics.Branch('Xi_chi2_sig_kills', Xi_chi2_sig_kills, 'Xi_chi2_sig_kills/F')
Xi_chi2_bac_kills = array('f', [0])
RunDiagnostics.Branch('Xi_chi2_bac_kills', Xi_chi2_bac_kills, 'Xi_chi2_bac_kills/F')
Xi_Pcomposite_sig_kills = array('f', [0])
RunDiagnostics.Branch('Xi_Pcomposite_sig_kills', Xi_Pcomposite_sig_kills, 'Xi_Pcomposite_sig_kills/F')
Xi_Pcomposite_bac_kills = array('f', [0])
RunDiagnostics.Branch('Xi_Pcomposite_bac_kills', Xi_Pcomposite_bac_kills, 'Xi_Pcomposite_bac_kills/F')
Xi_chi2_distance_sig_kills = array('f', [0])
RunDiagnostics.Branch('Xi_chi2_distance_sig_kills', Xi_chi2_distance_sig_kills, 'Xi_chi2_distance_sig_kills/F')
Xi_chi2_disatance_bac_kills = array('f', [0])
RunDiagnostics.Branch('Xi_chi2_disatance_bac_kills', Xi_chi2_disatance_bac_kills, 'Xi_chi2_disatance_bac_kills/F')
Xi_dira_sig_kills = array('f', [0])
RunDiagnostics.Branch('Xi_dira_sig_kills', Xi_dira_sig_kills, 'Xi_dira_sig_kills/F')
Xi_dira_bac_kills = array('f', [0])
RunDiagnostics.Branch('Xi_dira_bac_kills', Xi_dira_bac_kills, 'Xi_dira_bac_kills/F')
Xi_mass_sig_kills = array('f', [0])
RunDiagnostics.Branch('Xi_mass_sig_kills', Xi_mass_sig_kills, 'Xi_mass_sig_kills/F')
Xi_mass_bac_kills = array('f', [0])
RunDiagnostics.Branch('Xi_mass_bac_kills', Xi_mass_bac_kills, 'Xi_mass_bac_kills/F')

RunDiagnostics.Branch('Lambdac_mass', Lambdac_mass, 'Lambdac_mass/F')
#endregion RunDiagnostics

#region Outputs
Outputs = TTree("Run Diagnostics","Run Diagnostics")
xi_sig = array('f', [0])
Outputs.Branch('xi_sig', xi_sig, 'xi_sig/F')
Num_pions_detected = array('f', [0])
Outputs.Branch('Num_pions_detected', Num_pions_detected, 'Num_pions_detected/F')
Num_kaons_detected = array('f', [0])
Outputs.Branch('Num_kaons_detected', Num_kaons_detected, 'Num_kaons_detected/F')
Num_pions_detected = array('f', [0])
Outputs.Branch('Num_pions_detected', Num_pions_detected, 'Num_pions_detected/F')
Num_protons_detected = array('f', [0])
Outputs.Branch('Num_protons_detected', Num_protons_detected, 'Num_protons_detected/F')
Num_lambda_container = array('f', [0])
Outputs.Branch('Num_lambda_container', Num_lambda_container, 'Num_lambda_container/F')
Num_pv = array('f', [0])
Outputs.Branch('Num_pv', Num_pv, 'Num_pv/F')
Lambda_chi2 = array('f', [0])
Outputs.Branch('Lambda_chi2', Lambda_chi2, 'Lambda_chi2/F')
p_pt = array('f', [0])
Outputs.Branch('p_pt', p_pt, 'p_pt/F')
p_eta = array('f', [0])
Outputs.Branch('p_eta', p_eta, 'p_eta/F')
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
Lambdac_mass = array('f', [0])
Outputs.Branch('Lambdac_mass', Lambdac_mass, 'Lambdac_mass/F')
Lambdac_chi2_distance = array('f', [0])
Outputs.Branch('Lambdac_chi2_distance', Lambdac_chi2_distance, 'Lambdac_chi2_distance/F')
Lambdac_dira= array('f', [0])
Outputs.Branch('Lambdac_dira', Lambdac_dira, 'Lambdac_dira/F')
Xi_chi2 = array('f', [0])
Outputs.Branch('Xi_chi2', Xi_chi2, 'Xi_chi2/F')
lambdac_pt= array('f', [0])
Outputs.Branch('lambdac_pt', lambdac_pt, 'lmabdas_pt/F')
Lambdac_eta = array('f', [0])
Outputs.Branch('Lambdac_eta', Lambdac_eta, 'Lambdac_eta/F')
pi2_pt= array('f', [0])
Outputs.Branch('pi2_pt', pi2_pt, 'pi2_pt/F')
pi2_eta = array('f', [0])
Outputs.Branch('pi2_eta', pi2_eta, 'pi2_eta/F')
Xi_chi2_distance= array('f', [0])
Outputs.Branch('Xi_chi2_distance', Xi_chi2_distance, 'Xi_chi2_distance/F')
Xi_dira= array('f', [0])
Outputs.Branch('Xi_dira', Xi_dira, 'Xi_dira/F')
num_lambdac= array('f', [0])
Outputs.Branch('num_lambdac', num_lambdac, 'num_lambdac/F')
Outputs.Branch('Lambdac_mass', Lambdac_mass, 'Lambdac_mass/F')
num_xiccpp= array('f', [0])
xiccpp_mass= array('f', [0])
Outputs.Branch('num_xiccpp', num_xiccpp, 'num_xiccpp/F')
Outputs.Branch('xiccpp_mass', xiccpp_mass, 'xiccpp_mass/F')
#endregion Outputs
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
rand_seed_arg = get_arg(3, int(time.time() * os.getpid()), args)  # Default random seed if not provided

# Set tree values from user inputs

rand_seed[0] = rand_seed_arg

max_timing = 0.050
lambdacMass = 2286.46
XiccMass = 3621.6




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
  match = re.search(r"tuple_(\d+)", file_name)
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

p_dict = {
  "Kaon":321,
  "Pion":211,
  "Proton":2212,
  "Lambdac":4122,
  "Xicc++":4222,
  "Xicc+":4212,
  "Xic+": 4232
}

#endregion FUNCTION DEFINITIONS

#region FILE READING

sys.path.insert(0,basedir) 
from MCTools import * 
gInterpreter.AddIncludePath( f'{basedir}/../include')
gSystem.Load( f'{basedir}/../build/libEvent.so') # add the event library to the python path

events = TChain("Events") # connects all the events into a single data set

dir=f"/disk/moose/lhcb/djdt/photonics/stackNov24/masters_XiccTest/largeRun_Xicc++/sym/"
onlyfiles = [f for f in listdir(dir) if path.isfile(path.join(dir, f))]

onlyfiles = onlyfiles[int(lower):int(upper)]
# Since list is formed in order for every run, this selects the relevant files to be run

for file in onlyfiles:
  events.AddFile( path.join(dir, file) )  # Look at a file in the target directory for analysis

# plot = ROOT.TH1D("m_ds","",100,1.8,2.1) # initiates the mass plot
vtx_chi2 = SigVsBkg("vtx_chi2",100,2,3) # initiates the signal vs background plot
lambdac_plot = ROOT.TH1D("m_lambdac","",100,5.1,5.6)
lambdac_plot.SetTitle("Reconstructed Lambdac Mass Plot") 
lambdac_plot.GetXaxis().SetTitle("Mass (MeV/c^2)")
lambdac_plot.GetYaxis().SetTitle("Frequency")

xi_plot = ROOT.TH1D("m_xis","",100,1.8,2.1)
xi_plot.SetTitle("Reconstructed Xi Mass Plot") 
xi_plot.GetXaxis().SetTitle("Mass (MeV/c^2)")
xi_plot.GetYaxis().SetTitle("Frequency")
xi_vtx_chi2 = SigVsBkg("xi_vtx_chi2",100,2,3)

entry=0
n_signal=0

#endregion FILE READING

#region DETECTOR EFFICIENCY
# Switched off as per Dan'd instructions

# eff_directory = os.path.join(basedir, f'Inputs/PEff Kaons_{rich_timing}')
# List all file paths
# eff_dfs = [pd.read_csv(os.path.join(eff_directory, file)) for file in sorted(os.listdir(eff_directory))]
# boundaries = np.array([eff_dfs[i]['Momentum'][0].astype(float) for i in range(1,len(eff_dfs))])*(10**3)

# models = [eff_model(eff_dfs[0]), eff_model(eff_dfs[1]), eff_model(eff_dfs[2]), eff_model(eff_dfs[3]), eff_model(eff_dfs[4]) if rich_timing == 300 else None]

#endregion DETECTOR EFFICIENCY

#region EVENT LOOP

file_number[0] = 0 #  Initialises run number so += 1 can be used in event loop
current_file_name = "" #  Sets to empty string so first event loop changes it

for event in events: # loop through all events

  if events.GetFile().GetName() != current_file_name: #  If no longer in same file as before
    current_file_name = events.GetFile().GetName() #  Set file name to be the name of current file
    file_number[0] = get_file_number(current_file_name) #  Changes the file number to the new file number
    # print(f"Current file name: \n{current_file_name} \nCurrent file number: \n{file_number[0]}")
  
  displaced_tracks = ROOT.select( event.Particles, event.Vertices, 200, 1000,6) # select particles, verticies, min_pt, min_p,min_ipChi2_4d
  good_pions = [ track for track in displaced_tracks if abs(track.trueID) == p_dict['Pion'] and track.charge() > 0] # all pi+
  good_kaons = [ track for track in displaced_tracks if abs(track.trueID) == p_dict['Kaon'] and track.charge() < 0] # all k^-
  good_protons = [ track for track in displaced_tracks if abs(track.trueID) == p_dict['Proton'] and track.charge() > 0] # all p^+
  doca_cut = 0.5 # distance of closest approach cutoff, maximum allowed closest approach for consideration
  nPVs = npvs( event ) # the number of primary verticies in an event
  #print(f'the total number of primary verticies per event{nPVs}')
  found_signal = False # placeholder for when a signal is found, default of no signal found
  found_lambdac_signal = False
  #print( f"{entry} {nPVs} {len(good_pions)} {len(good_kaons)} {len(good_protons)}") # prints event information
  lambda_container = ROOT.combine( good_protons, good_kaons, doca_cut, 3, 0) # inputs: all kp, all km, doca_max, chi2ndf_max, charge
  # returns:  four momenta of particle1, particle2 , a combined particle, and the vertex where combination occurs
  #Num_lambda_container[0] = len(lambda_container)
  # print(f'total number of lambda containers per event {len(lambda_container)}')
  # create all phi candiates, two particles at a distance smaller than the maximum allowed distance, with acceptable chi2ndf and sum
  # to a charge of 0
  xiccpp_pions = [ track for track in ROOT.select( event.Particles, event.Vertices, 400, 2000, 3 ) if  track.trueID == p_dict['Pion'] and track.charge()>0]
  xiccpp_kaons = [ track for track in ROOT.select( event.Particles, event.Vertices, 400, 2000, 3 ) if  track.trueID == p_dict['Kaon'] and track.charge()<0] # needs changing from bs to Xi limits
  Num_protons_detected[0] = len(good_protons)
  Num_pions_detected[0] = len(good_pions)
  Num_kaons_detected[0] = len(good_kaons)
  Doca_cut[0] = doca_cut
  Num_pv[0] = nPVs

  for pion in good_pions :
    for p,k1,lambda0,lambda0_vtx in lambda_container: 

      # k1 is the four momenta of the positive kaons, k2 is the four momenta of the negative kaons, phi is the combined particle
      # created by the kaons, and phi_vtx is the vertex in which the combination occurs

      lambdac_vtx = ROOT.uVertex( [p,k1,pion] ) # create a new vertex, using momentum of the first kaon or second kaon and a pion as
      # these recombine to create a B0 (see diagram)
      # Should make reverse case as well

      lambdac = ROOT.uParticle( [p,k1,pion] ) # create a candiate particle for reconstruction. using either positive or negative kaon
 
      is_lambdac_signal = is_from(p, event, p_dict['Xicc++']) and is_from(k1, event, p_dict['Xicc++']) and is_from(pion, event, p_dict['Xicc++'])
      
      vtx_chi2.Fill( lambdac_vtx.chi2 / lambdac_vtx.ndof, is_lambdac_signal) # Fills the chi2 graph for the candiate signal

      Lambda_chi2[0] = lambdac_vtx.chi2 / lambdac_vtx.ndof
      p_pt[0] = p.pt()
      p_eta[0] = p.eta()
      k1_pt[0] = k1.pt()
      k1_eta[0] = k1.eta()
      pi1_pt[0] = pion.pt()
      pi1_eta[0] = pion.eta()
      pi1_ID[0] = abs(pion.trueID)
      Lambda_chi2_limit[0] = 5 # Formerly Chi2_ndf_limit

      if lambdac_vtx.chi2 / lambdac_vtx.ndof > 5 : # kills nothing
        if is_lambdac_signal:
          Lambdac_chi2_sig_kills[0] += 1
        else:
          Lambdac_chi2_bac_kills[0] += 1
        continue # if the chi2/ndf is not acceptable, disgard possible particle
      Lambdac_pdg = 2286.46
      Lambdac_Pcomposite_limit[0] = 1800
      if p.pt() + k1.pt() + pion.pt() < Lambdac_pdg - 150 :
        if is_lambdac_signal:
          Lambdac_Pcomposite_sig_kills[0] += 1
        else:
          Lambdac_Pcomposite_bac_kills[0] += 1
        continue # insufficient momentum to create a phi, discard
      Lambdac_mass_lower_limit[0] = 1800
      Lambdac_mass_upper_limit[0] = 2100
      if lambdac.mass < Lambdac_pdg - 150 or lambdac.mass  > Lambdac_pdg + 150 :
        if is_lambdac_signal:
          Lambdac_mass_sig_kills[0] += 1
        else:
          Lambdac_mass_bac_kills[0] += 1
        continue # insufficient mass to create D particle, discard
      
      pv  = lambdac.bpv_4d( event.Vertices ) # pv: possible vertex, finds best possible vertex for the considered
      Lambdac_chi2_distance[0] = lambdac_vtx.chi2_distance(pv)
      Lambdac_dira[0] = dira_bpv(lambdac,event.Vertices,max_timing)
#     vtx_chi2.Fill( ds_vtx.chi2_distance(pv), is_lambdac_signal )
      Lambdac_chi2_distance_limit[0] = 50
      if lambdac_vtx.chi2_distance(pv) < 16 : 
        if is_lambdac_signal:
          Lambdac_chi2_distance_sig_kills[0] += 1
        else:
          Lambdac_chi2_distance_bac_kills[0] += 1
        continue # if the product of the Chi squareds of the particle and the vertex
      # is greater than 50, discard
      Lambdac_dira_limit[0] = 0.9
      if dira_bpv(lambdac,event.Vertices,max_timing)  < 0.9 : 
        if is_lambdac_signal:
          Lambdac_dira_sig_kills[0] += 1
        else:
          Lambdac_dira_bac_kills[0] += 1
        continue # if the cos of the angle between momenta is less than 0.9 discard

      Lambdac_mass[0] = lambdac.mass
      lambdac_pt[0] = lambdac.pt()
      Lambdac_eta[0] = lambdac.eta()
      lambdac_plot.Fill(lambdac.mass*0.001)
      print(lambdac.mass)
      
      if (lambdac.mass<Lambdac_pdg-30) or (lambdac.mass>Lambdac_pdg+30):
        if is_lambdac_signal:
          Lambdac_mass2_sig_kills[0] += 1
        else:
          Lambdac_mass2_bac_kills[0] += 1
        continue
      for xiccpp_pion1,xiccpp_pion2 in xiccpp_pions:
            for xiccpp_kaon in xiccpp_kaons:
            
              is_xiccpp_signal = is_from(p, event, p_dict['Xicc++']) and is_from(k1, event, p_dict['Xicc++']) and is_from(pion, event,p_dict['Xicc++']) and is_from(xiccpp_pion1, event,p_dict['Xicc++']) and is_from(xiccpp_pion2, event,p_dict['Xicc++']) and is_from(xiccpp_kaon, event,p_dict['Xicc++'])
              if xiccpp_pion1.charge() + xiccpp_pion2.charge()+xiccpp_kaon.charge() + lambdac.charge() !=2: 
                if is_xiccpp_signal:
                  Xi_sign_sig_kills[0] += 1
                else:
                  Xi_sign_bac_kills[0] += 1
                continue
              xiccpp_vtx = ROOT.uVertex( [p, k1, pion, xiccpp_pion1,xiccpp_pion2,xiccpp_kaon] )
              xiccpp = ROOT.uParticle( [p, k1, pion, xiccpp_pion1,xiccpp_pion2,xiccpp_kaon] )

              Xi_chi2[0] = xiccpp_vtx.chi2 / xiccpp_vtx.ndof
              pi2_pt[0] = pion.pt()
              pi2_eta[0] = pion.eta()

              xi_vtx_chi2.Fill( xiccpp_vtx.chi2 / xiccpp_vtx.ndof, is_xiccpp_signal)
              Xi_chi2_limit[0] = 15
              if xiccpp_vtx.chi2 / xiccpp_vtx.ndof > 15 : 
                if is_xiccpp_signal:
                  Xi_chi2_sig_kills[0] += 1
                else:
                  Xi_chi2_bac_kills[0] += 1
                continue # if the chi2/ndf is not acceptable, disgard possible particle
              Xi_Pcomposite_limit[0] = 5000
              if lambdac.pt() + xiccpp_kaon.pt() + xiccpp_pion1 + xiccpp_pion2 < 5000 :
                if is_xiccpp_signal:
                  Xi_Pcomposite_sig_kills[0] += 1
                else:
                  Xi_Pcomposite_bac_kills[0] += 1
                continue # insufficient momentum to create a phi, discard
              Xi_mass_lower_limit[0] = 5100
              Xi_mass_upper_limit[0] = 5600
              xiccpp_pv  = xiccpp.bpv_4d( event.Vertices )

              Xi_chi2_distance[0] = xiccpp_vtx.chi2_distance(xiccpp_pv) 
              Xi_dira[0] = dira_bpv(xiccpp,event.Vertices,max_timing)

              Xi_chi2_distance_limit[0] = 50
              if xiccpp_vtx.chi2_distance(xiccpp_pv) < 50 : 
                if is_xiccpp_signal:
                  Xi_chi2_distance_sig_kills[0] += 1
                else:
                  Xi_chi2_disatance_bac_kills[0] += 1
                continue 
              Xi_dira_limit[0] = 0.9
              if dira_bpv(xiccpp,event.Vertices,max_timing)  < 0.90 :
                if is_xiccpp_signal:
                  Xi_dira_sig_kills[0] += 1
                else:
                  Xi_dira_bac_kills[0] += 1
                continue
              if (xiccpp.mass<XiccMass-100) or (xiccpp.mass>XiccMass+100):
                if is_xiccpp_signal:
                  Xi_mass_sig_kills[0] += 1
                else:
                  Xi_mass_bac_kills[0] += 1
                continue
              
              xi_sig[0] = 1 if is_xiccpp_signal is True else 0
              xi_plot.Fill(xiccpp.mass * 0.001)
              xiccpp_mass[0] = xiccpp.mass * 0.001
              entry += 1 # entry is the event being examined
              num_xiccpp[0] = entry
              found_signal |= is_xiccpp_signal

  RunParams.Fill()
  RunLimits.Fill()
  RunDiagnostics.Fill()
  Outputs.Fill()


  
#tree.Show(5)
#print(tree.GetEntries())

#endregion EVENT LOOP

file = TFile(f"{basedir}/Outputs/XisToLambdas/Tree{lower}:{upper}.root", "RECREATE")
# Creates temporary tree (deleted when trees are combined)
file.WriteObject(Outputs, "Outputs")
file.WriteObject(RunParams, "RunParams")
file.WriteObject(RunLimits, "RunLimits")
file.WriteObject(RunDiagnostics, "RunDiagnostics")
file.WriteObject(lambdac_plot, "Lambdac_Histogram")
file.WriteObject(xi_plot, "Xicc++_Histogram")
file.Close()
