# ------------------- Imports -------------------
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
# ------------------- RunParamsTree -------------------
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
com_energy[0] = 14
# ------------------- RunLimitsTree -------------------
RunLimits = ROOT.TTree("RunLimits", "RunLimits")
lambdac_vtx_chi2_ndof_limit = array('f', [0]) # Formerly Chi2_ndf_limit
RunLimits.Branch('lambdac_vtx_chi2_ndof_limit', lambdac_vtx_chi2_ndof_limit, 'lambdac_vtx_chi2_ndof_limit/F')
lambdac_combined_momentum_lower_limit = array('f', [0])
RunLimits.Branch('lambdac_combined_momentum_lower_limit', lambdac_combined_momentum_lower_limit, 'lambdac_combined_momentum_lower_limit/F')
lambdac_vtx_chi2_distance_limit = array('f', [0])
RunLimits.Branch('lambdac_vtx_chi2_distance_limit', lambdac_vtx_chi2_distance_limit, 'lambdac_vtx_chi2_distance_limit/F')
lambdac_vtx_dira_limit = array('f', [0])
RunLimits.Branch('lambdac_vtx_dira_limit', lambdac_vtx_dira_limit, 'lambdac_vtx_dira_limit/F')
xiccpp_vtx_chi2_ndof_limit = array('f', [0])
RunLimits.Branch('xiccpp_vtx_chi2_ndof_limit', xiccpp_vtx_chi2_ndof_limit, 'xiccpp_vtx_chi2_ndof_limit/F')
xiccpp_combined_momentum_lower_limit = array('f', [0])
RunLimits.Branch('xiccpp_combined_momentum_lower_limit', xiccpp_combined_momentum_lower_limit, 'xiccpp_combined_momentum_lower_limit/F')
xiccpp_vtx_chi2_distance_limit = array('f', [0])
RunLimits.Branch('xiccpp_vtx_chi2_distance_limit', xiccpp_vtx_chi2_distance_limit, 'xiccpp_vtx_chi2_distance_limit/F')
xiccpp_vtx_dira_limit = array('f', [0])
RunLimits.Branch('xiccpp_vtx_dira_limit', xiccpp_vtx_dira_limit, 'xiccpp_vtx_dira_limit/F')
# ------------------- RunDiagnosticsTree -------------------
RunDiagnostics = TTree("RunDiagnostics","RunDiagnostics")
lambdac_signal_combined_momentum_kills = array('f', [0]) # Formerly Chi2_ndf_limit
RunDiagnostics.Branch('lambdac_signal_combined_momentum_kills', lambdac_signal_combined_momentum_kills, 'lambdac_signal_combined_momentum_kills/F')
lambdac_bkg_combined_momentum_kills = array('f', [0]) # Formerly Chi2_ndf_limit
RunDiagnostics.Branch('lambdac_bkg_combined_momentum_kills', lambdac_bkg_combined_momentum_kills, 'lambdac_bkg_combined_momentum_kills/F')
lambdac_mass_limit_signal_kills = array('f', [0]) # Formerly Chi2_ndf_limit
RunDiagnostics.Branch('lambdac_mass_limit_signal_kills', lambdac_mass_limit_signal_kills, 'lambdac_mass_limit_signal_kills/F')
lambdac_mass_limit_bkg_kills = array('f', [0]) # Formerly Chi2_ndf_limit
RunDiagnostics.Branch('lambdac_mass_limit_bkg_kills', lambdac_mass_limit_bkg_kills, 'lambdac_mass_limit_bkg_kills/F')
lambdac_final_mass_cut_signal_kills = array('f', [0]) # Formerly Chi2_ndf_limit
RunDiagnostics.Branch('lambdac_final_mass_cut_signal_kills', lambdac_final_mass_cut_signal_kills, 'lambdac_final_mass_cut_signal_kills/F')
lambdac_final_mass_cut_bkg_kills = array('f', [0]) # Formerly Chi2_ndf_limit
RunDiagnostics.Branch('lambdac_final_mass_cut_bkg_kills', lambdac_final_mass_cut_bkg_kills, 'lambdac_final_mass_cut_bkg_kills/F')
lambdac_vtx_chi2_ndof_signal_kills = array('f', [0])
RunDiagnostics.Branch('lambdac_vtx_chi2_ndof_signal_kills', lambdac_vtx_chi2_ndof_signal_kills, 'lambdac_vtx_chi2_ndof_signal_kills/F')
lambdac_vtx_chi2_ndof_bkg_kills = array('f', [0])
RunDiagnostics.Branch('lambdac_vtx_chi2_ndof_bkg_kills',lambdac_vtx_chi2_ndof_bkg_kills , 'lambdac_vtx_chi2_ndof_bkg_kills/F')
lambdac_vtx_chi2_distance_sig_kills = array('f', [0])
RunDiagnostics.Branch('lambdac_vtx_chi2_distance_sig_kills', lambdac_vtx_chi2_distance_sig_kills, 'lambdac_vtx_chi2_distance_sig_kills/F')
lambdac_vtx_chi2_distance_bac_kills = array('f', [0])
RunDiagnostics.Branch('lambdac_vtx_chi2_distance_bac_kills', lambdac_vtx_chi2_distance_bac_kills, 'lambdac_vtx_chi2_distance_bac_kills/F')
lambdac_vtx_dira_sig_kills = array('f', [0])
RunDiagnostics.Branch('lambdac_vtx_dira_sig_kills', lambdac_vtx_dira_sig_kills, 'lambdac_vtx_dira_sig_kills/F')
lambdac_vtx_dira_bac_kills = array('f', [0])
RunDiagnostics.Branch('lambdac_vtx_dira_bac_kills', lambdac_vtx_dira_bac_kills, 'lambdac_vtx_dira_bac_kills/F')
xi_charge_conservation_signal_kills = array('f', [0])
RunDiagnostics.Branch('xi_charge_conservation_signal_kills', xi_charge_conservation_signal_kills, 'xi_charge_conservation_signal_kills/F')
xi_charge_conservation_bkg_kills = array('f', [0])
RunDiagnostics.Branch('xi_charge_conservation_bkg_kills', xi_charge_conservation_bkg_kills, 'xi_charge_conservation_bkg_kills/F')
xi_vtx_chi2_ndof_sig_kills = array('f', [0])
RunDiagnostics.Branch('xi_vtx_chi2_ndof_sig_kills', xi_vtx_chi2_ndof_sig_kills, 'xi_vtx_chi2_ndof_sig_kills/F')
xi_vtx_chi2_ndof_bkg_kills = array('f', [0])
RunDiagnostics.Branch('xi_vtx_chi2_ndof_bkg_kills', xi_vtx_chi2_ndof_bkg_kills, 'xi_vtx_chi2_ndof_bkg_kills/F')
xi_signal_minimum_momentum_kills = array('f', [0])
RunDiagnostics.Branch('xi_signal_minimum_momentum_kills', xi_signal_minimum_momentum_kills, 'xi_signal_minimum_momentum_kills/F')
xi_bkg_minimum_momentum_kills = array('f', [0])
RunDiagnostics.Branch('xi_bkg_minimum_momentum_kills', xi_bkg_minimum_momentum_kills, 'xi_bkg_minimum_momentum_kills/F')
xi_vtx_chi2_distance_sig_kills = array('f', [0])
RunDiagnostics.Branch('xi_vtx_chi2_distance_sig_kills', xi_vtx_chi2_distance_sig_kills, 'xi_vtx_chi2_distance_sig_kills/F')
xi_chi2_disatance_bac_kills = array('f', [0])
RunDiagnostics.Branch('xi_chi2_disatance_bac_kills', xi_chi2_disatance_bac_kills, 'xi_chi2_disatance_bac_kills/F')
xi_vtx_dira_sig_kills = array('f', [0])
RunDiagnostics.Branch('xi_vtx_dira_sig_kills', xi_vtx_dira_sig_kills, 'xi_vtx_dira_sig_kills/F')
xi_vtx_dira_bkg_kills = array('f', [0])
RunDiagnostics.Branch('xi_vtx_dira_bkg_kills', xi_vtx_dira_bkg_kills, 'xi_vtx_dira_bkg_kills/F')
xi_mass_sig_kills = array('f', [0])
RunDiagnostics.Branch('xi_mass_sig_kills', xi_mass_sig_kills, 'xi_mass_sig_kills/F')
xi_mass_bkg_kills = array('f', [0])
RunDiagnostics.Branch('xi_mass_bkg_kills', xi_mass_bkg_kills, 'xi_mass_bkg_kills/F')
# ------------------- OutputsTree -------------------
Outputs = TTree("Run Diagnostics","Run Diagnostics")
xiccpp_signal_binary_flag = array('f', [0])
Outputs.Branch('xiccpp_signal_binary_flag', xiccpp_signal_binary_flag, 'xiccpp_signal_binary_flag/F')
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
lambdac_vtx_chi2_ndof_v = array('f', [0])
Outputs.Branch('lambdac_vtx_chi2_ndof_v', lambdac_vtx_chi2_ndof_v, 'lambdac_vtx_chi2_ndof_v/F')
proton_pt = array('f', [0])
Outputs.Branch('proton_pt', proton_pt, 'proton_pt/F')
xiccpp_pion2_pt = array('f', [0])
Outputs.Branch('xiccpp_pion2_pt', xiccpp_pion2_pt, 'xiccpp_pion2_pt/F')
xiccpp_pion2_eta = array('f', [0])
Outputs.Branch('xiccpp_pion2_eta', xiccpp_pion2_eta, 'xiccpp_pion2_eta/F')
xiccpp_kaon_eta = array('f', [0])
Outputs.Branch('xiccpp_kaon_eta', xiccpp_kaon_eta, 'xiccpp_kaon_eta/F')
xiccpp_kaon_pt = array('f', [0])
Outputs.Branch('xiccpp_kaon_pt', xiccpp_kaon_pt, 'xiccpp_kaon_pt/F')
lambdac_kaon_pt = array('f', [0])
Outputs.Branch('lambdac_kaon_pt', lambdac_kaon_pt, 'lambdac_kaon_pt/F')
lambdac_kaon_eta = array('f', [0])
Outputs.Branch('lambdac_kaon_eta', lambdac_kaon_eta, 'lambdac_kaon_eta/F')
lambdac_pion_pt = array('f', [0])
Outputs.Branch('lambdac_pion_pt', lambdac_pion_pt, 'lambdac_pion_pt/F')
lambdac_pion_eta = array('f', [0])
Outputs.Branch('lambdac_pion_eta', lambdac_pion_eta, 'lambdac_pion_eta/F')
lambdac_pion_ID = array('f', [0])
Outputs.Branch('lambdac_pion_ID', lambdac_pion_ID, 'lambdac_pion_ID/F')
lambdac_mass = array('f', [0])
Outputs.Branch('lambdac_mass', lambdac_mass, 'lambdac_mass/F')
lambdac_vtx_chi2_distance = array('f', [0])
Outputs.Branch('lambdac_vtx_chi2_distance', lambdac_vtx_chi2_distance, 'lambdac_vtx_chi2_distance/F')
lambdac_vtx_dira= array('f', [0])
Outputs.Branch('lambdac_vtx_dira', lambdac_vtx_dira, 'lambdac_vtx_dira/F')
xiccpp_vtx_chi2_ndof = array('f', [0])
Outputs.Branch('xiccpp_vtx_chi2_ndof', xiccpp_vtx_chi2_ndof, 'xiccpp_vtx_chi2_ndof/F')
lambdac_pt= array('f', [0])
Outputs.Branch('lambdac_pt', lambdac_pt, 'lmabdas_pt/F')
lambdac_eta = array('f', [0])
Outputs.Branch('lambdac_eta', lambdac_eta, 'lambdac_eta/F')
xiccpp_pion1_pt= array('f', [0])
Outputs.Branch('xiccpp_pion1_pt', xiccpp_pion1_pt, 'xiccpp_pion1_pt/F')
xiccpp_pion1_eta = array('f', [0])
Outputs.Branch('xiccpp_pion1_eta', xiccpp_pion1_eta, 'xiccpp_pion1_eta/F')
xi_vtx_chi2_distance= array('f', [0])
Outputs.Branch('xi_vtx_chi2_distance', xi_vtx_chi2_distance, 'xi_vtx_chi2_distance/F')
xi_vtx_dira= array('f', [0])
Outputs.Branch('xi_vtx_dira', xi_vtx_dira, 'xi_vtx_dira/F')
number_of_xiccpp= array('f', [0])
xiccpp_mass= array('f', [0])
Outputs.Branch('number_of_xiccpp', number_of_xiccpp, 'number_of_xiccpp/F')
Outputs.Branch('xiccpp_mass', xiccpp_mass, 'xiccpp_mass/F')
# ------------------- UserInputs -------------------
def get_arg(index, default, args):  # Arg function that returns relevant arguments and deals with missing args
    try:
        return int(args[index])
    except (IndexError, ValueError, TypeError):
        return default
args = sys.argv
lower = get_arg(1, 0, args)  # Default timing argument if not provided
upper = get_arg(2, 2, args)  # Default timing argument if not provided
rand_seed_arg = get_arg(3, int(time.time() * os.getpid()), args)  # Default random seed if not provided
rand_seed[0] = rand_seed_arg
max_timing = 0.050 # needs adjusting (temporary line)
if path.dirname(path.realpath(__file__))[-6:] == "python": # Checks if path ends in "python"
  basedir=path.dirname(path.realpath(__file__))
  sys.path.append(f"{path.dirname(path.realpath(__file__))}/..")
  batching = False
else:
  basedir = f"{path.dirname(path.realpath(__file__))}/../../../.."
  sys.path.append(f"{path.dirname(path.realpath(__file__))}/../../../..")
  batching = True
# ------------------- RandomNumberGenerator -------------------
rand = ROOT.TRandom() # creates a random number engine, used for when we want to have PID (temporarily not used here)
rand.SetSeed(rand_seed_arg)
# ------------------- Class and Function Definitions -------------------
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

def kill_counter(condition,tree_branch1,tree_branch2):
  if condition:
    tree_branch1[0] += 1
  else:
    tree_branch2[0] += 1 
# ------------------- Dictionaries -------------------
particle_dict = {
  "Kaon":321,
  "Pion":211,
  "Proton":2212,
  "lambdac":4122,
  "xicc++":4222,
  "xicc+":4212,
  "xic+": 4232}

mass_dict = {
  "xiccpp":2286.46,
  "lambdac":3621.6}

limits_dict = {
  "lambdac_vtx_chi2_ndof":5,
  "lambdac_vtx_chi2_distance":16,
  "lambdac_vtx_dira":0.9,
  "xiccpp_vtx_chi2_ndof":15,
  "xiccpp_vtx_chi2_distance":50,
  "xiccpp_dira":0.9,
  "lambdac_combined_momentum":mass_dict["lambdac"] - 150,
  "xiccpp_combined_momentum":mass_dict["xiccpp"] - 150}
# ------------------- LimitTreeFill(can be closed with region) -------------------
#region LimitsTree
lambdac_vtx_chi2_ndof_limit = limits_dict["lambdac_vtx_chi2_ndof"]
lambdac_combined_momentum_lower_limit = limits_dict["lambdac_combined_momentum"]
lambdac_vtx_chi2_distance_limit = limits_dict["lambdac_vtx_chi2_distance"]
lambdac_vtx_dira_limit = limits_dict["lambdac_vtx_dira"]
xiccpp_vtx_chi2_ndof_limit = limits_dict["xiccpp_vtx_chi2_ndof"]
xiccpp_combined_momentum_lower_limit = limits_dict["xiccpp_combined_momentum"]
xiccpp_vtx_chi2_distance_limit = limits_dict["xiccpp_vtx_chi2_distance"]
xiccpp_vtx_dira_limit = limits_dict["xiccpp_dira"]
#endregion LimitsTree
# ------------------- FileReading/EventGrabbing -------------------
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
entry=0
# -------------------PID SImulation (Not Activate ATM) -------------------
# Switched off as per Dan'd instructions
# eff_directory = os.path.join(basedir, f'Inputs/PEff Kaons_{rich_timing}')
# List all file paths
# eff_dfs = [pd.read_csv(os.path.join(eff_directory, file)) for file in sorted(os.listdir(eff_directory))]
# boundaries = np.array([eff_dfs[i]['Momentum'][0].astype(float) for i in range(1,len(eff_dfs))])*(10**3)
# models = [eff_model(eff_dfs[0]), eff_model(eff_dfs[1]), eff_model(eff_dfs[2]), eff_model(eff_dfs[3]), eff_model(eff_dfs[4]) if rich_timing == 300 else None]
file_number[0] = 0 #  Initialises run number so += 1 can be used in event loop
current_file_name = "" #  Sets to empty string so first event loop changes it
for event in events: # loop through all events

  if events.GetFile().GetName() != current_file_name: #  If no longer in same file as before
    current_file_name = events.GetFile().GetName() #  Set file name to be the name of current file
    file_number[0] = get_file_number(current_file_name) #  Changes the file number to the new file number
# ------------------- ParticleLists -------------------
  displaced_tracks = ROOT.select( event.Particles, event.Vertices, 200, 1000,6) # select particles, verticies, min_pt, min_p,min_ipChi2_4d
  good_pions = [ track for track in displaced_tracks if abs(track.trueID) == particle_dict['Pion'] and track.charge() > 0] # all pi+
  good_kaons = [ track for track in displaced_tracks if abs(track.trueID) == particle_dict['Kaon'] and track.charge() < 0] # all k^-
  good_protons = [ track for track in displaced_tracks if abs(track.trueID) == particle_dict['Proton'] and track.charge() > 0] # all proton^+
  doca_cut = Doca_cut[0] = 0.5 # distance of closest approach cutoff, maximum allowed closest approach for consideration
  nPVs = Num_pv[0] = npvs( event ) # the number of primary verticies in an event
  #print(f'the total number of primary verticies per event{nPVs}')
  found_xiccpp_signal = False # placeholder for when a signal is found, default of no signal found
  found_lambdac_signal = False
  #print( f"{entry} {nPVs} {len(good_pions)} {len(good_kaons)} {len(good_protons)}") # prints event information
  lambda_container = ROOT.combine( good_protons, good_kaons, doca_cut, 3, 0) # inputs: all kp, all km, doca_max, chi2ndf_max, charge
  # returns:  four momenta of particle1, particle2 , a combined particle, and the vertex where combination occurs
  #Num_lambda_container[0] = len(lambda_container)
  # print(f'total number of lambda containers per event {len(lambda_container)}')
  # create all phi candiates, two particles at a distance smaller than the maximum allowed distance, with acceptable chi2ndf and sum
  # to a charge of 0
  xiccpp_pions = [ track for track in ROOT.select( event.Particles, event.Vertices, 400, 2000, 3 ) if  track.trueID == particle_dict['Pion'] and track.charge()>0]
  xiccpp_kaons = [ track for track in ROOT.select( event.Particles, event.Vertices, 400, 2000, 3 ) if  track.trueID == particle_dict['Kaon'] and track.charge()<0] # needs changing from bs to xi limits
  Num_protons_detected[0] = len(good_protons)
  Num_pions_detected[0] = len(good_pions)
  Num_kaons_detected[0] = len(good_kaons)
# ------------------- LambdacReconstruction -------------------
  for pion in good_pions :
    for proton,lambdac_kaon,lambda0,lambda0_vtx in lambda_container: 
      #region LambdacOutputTreeFill
      proton_pt[0] = proton.pt()
      proton_pt[0] = proton.eta()
      lambdac_kaon_pt[0] = lambdac_kaon.pt()
      lambdac_kaon_eta[0] = lambdac_kaon.eta()
      lambdac_pion_pt[0] = pion.pt()
      lambdac_pion_eta[0] = pion.eta()
      lambdac_pion_ID[0] = abs(pion.trueID)
      #endregion LambdacOutputTreeFill
      lambdac_vtx = ROOT.uVertex( [proton,lambdac_kaon,pion] ) # create a new vertex, using momentum of the first kaon or second kaon and a pion as
      # Should make reverse case as well
      lambdac = ROOT.uParticle( [proton,lambdac_kaon,pion] ) # create a candiate particle for reconstruction. using either positive or negative kaon
      is_lambdac_signal = is_from(proton, event, particle_dict['xicc++']) and is_from(lambdac_kaon, event, particle_dict['xicc++']) and is_from(pion, event, particle_dict['xicc++'])
      lambdac_vtx_chi2_ndof_v[0] = lambdac_vtx.chi2 / lambdac_vtx.ndof
      if lambdac_vtx.chi2 / lambdac_vtx.ndof > limits_dict["lambdac_vtx_chi2_ndof"] :
        kill_counter(is_lambdac_signal,lambdac_vtx_chi2_ndof_signal_kills,lambdac_vtx_chi2_ndof_bkg_kills)
        continue # if the chi2/ndf is not acceptable, disgard possible particle
      if proton.pt() + lambdac_kaon.pt() + pion.pt() < limits_dict["lambdac_combined_momentum"]:
        kill_counter(is_lambdac_signal,lambdac_signal_combined_momentum_kills,lambdac_signal_combined_momentum_kills)
        continue # insufficient momentum to create a phi, discard
      if lambdac.mass < mass_dict['lambdac'] - 150 or lambdac.mass  > mass_dict['lambdac'] + 150 :
        kill_counter(is_lambdac_signal,lambdac_mass_limit_signal_kills,lambdac_mass_limit_bkg_kills)
        continue # insufficient mass to create D particle, discard
      pv  = lambdac.bpv_4d( event.Vertices ) # pv: possible vertex, finds best possible vertex for the considered
      lambdac_vtx_chi2_distance[0] = lambdac_vtx.chi2_distance(pv)
      lambdac_vtx_dira[0] = dira_bpv(lambdac,event.Vertices,max_timing)
      if lambdac_vtx.chi2_distance(pv) < limits_dict['lambdac_vtx_chi2_distance'] : 
        kill_counter(is_lambdac_signal,lambdac_vtx_chi2_distance_sig_kills,lambdac_vtx_chi2_distance_bac_kills)
        continue # if the product of the Chi squareds of the particle and the vertex
      # is greater than 50, discard
      if dira_bpv(lambdac,event.Vertices,max_timing)  < limits_dict['lambdac_vtx_dira'] : 
        kill_counter(is_lambdac_signal,lambdac_vtx_dira_sig_kills,lambdac_vtx_dira_bac_kills)
        continue # if the cos of the angle between momenta is less than 0.9 discard
      # ------------------- LambdacOutputs -------------------
      lambdac_mass[0] = lambdac.mass
      found_lambdac_signal |= is_lambdac_signal
      lambdac_pt[0] = lambdac.pt()
      lambdac_eta[0] = lambdac.eta()      
      if (lambdac.mass<mass_dict["lambdac"]-30) or (lambdac.mass>mass_dict["lambdac"]+30):
        kill_counter(is_lambdac_signal,lambdac_final_mass_cut_signal_kills,lambdac_final_mass_cut_bkg_kills)
        continue
      # ------------------- xiccppReconstruction -------------------
      for xiccpp_pion1,xiccpp_pion2 in xiccpp_pions:
            for xiccpp_kaon in xiccpp_kaons:
              #region xiccppTreeFill
              xiccpp_pion1_pt[0] = xiccpp_pion1.pt()
              xiccpp_pion1_eta[0] = xiccpp_pion1.eta()
              xiccpp_pion2_pt[0] = xiccpp_pion2.pt()
              xiccpp_pion2_eta[0] = xiccpp_pion2.eta()
              xiccpp_kaon_pt[0] = xiccpp_kaon.pt()
              xiccpp_kaon_eta[0] = xiccpp_kaon.eta()
              #endregion xiccppTreeFill
              is_xiccpp_signal = is_from(proton, event, particle_dict['xicc++']) and is_from(lambdac_kaon, event, particle_dict['xicc++']) and is_from(pion, event,particle_dict['xicc++']) and is_from(xiccpp_pion1, event,particle_dict['xicc++']) and is_from(xiccpp_pion2, event,particle_dict['xicc++']) and is_from(xiccpp_kaon, event,particle_dict['xicc++'])
              if xiccpp_pion1.charge() + xiccpp_pion2.charge()+xiccpp_kaon.charge() + lambdac.charge() !=2: 
                kill_counter(lambdac_final_mass_cut_signal_kills,xi_charge_conservation_signal_kills,xi_charge_conservation_bkg_kills)
                continue
              xiccpp_vtx = ROOT.uVertex( [proton, lambdac_kaon, pion, xiccpp_pion1,xiccpp_pion2,xiccpp_kaon] )
              xiccpp = ROOT.uParticle( [proton, lambdac_kaon, pion, xiccpp_pion1,xiccpp_pion2,xiccpp_kaon] )
              xiccpp_vtx_chi2_ndof[0] = xiccpp_vtx.chi2 / xiccpp_vtx.ndof
              if xiccpp_vtx.chi2 / xiccpp_vtx.ndof > limits_dict['xiccpp_vtx_chi2_ndof'] : 
                kill_counter(is_xiccpp_signal,xi_vtx_chi2_ndof_sig_kills,xi_vtx_chi2_ndof_bkg_kills)
                continue # if the chi2/ndf is not acceptable, disgard possible particle
              if lambdac.pt() + xiccpp_kaon.pt() + xiccpp_pion1 + xiccpp_pion2 < limits_dict['xiccpp_combined_momentum'] :
                kill_counter(is_xiccpp_signal,xi_signal_minimum_momentum_kills,xi_bkg_minimum_momentum_kills)
                continue # insufficient momentum to create a phi, discard
              xiccpp_pv  = xiccpp.bpv_4d( event.Vertices )
              xi_vtx_chi2_distance[0] = xiccpp_vtx.chi2_distance(xiccpp_pv) 
              xi_vtx_dira[0] = dira_bpv(xiccpp,event.Vertices,max_timing)
              if xiccpp_vtx.chi2_distance(xiccpp_pv) < limits_dict['xiccpp_vtx_chi2_distance'] :
                kill_counter(is_xiccpp_signal,xi_vtx_chi2_distance_sig_kills,xi_chi2_disatance_bac_kills)
                continue 
              if dira_bpv(xiccpp,event.Vertices,max_timing)  < limits_dict['xiccpp_dira'] :
                kill_counter(is_xiccpp_signal,xi_vtx_dira_sig_kills,xi_vtx_dira_bkg_kills)
                continue
              if (xiccpp.mass<mass_dict['xiccpp']-100) or (xiccpp.mass>mass_dict['xiccpp']+100):
                kill_counter(is_xiccpp_signal,xi_mass_sig_kills,xi_mass_bkg_kills)
                continue
              # ------------------- xiccppOutputs -------------------
              xiccpp_signal_binary_flag[0] = 1 if is_xiccpp_signal is True else 0
              xiccpp_mass[0] = xiccpp.mass * 0.001
              entry += 1 # entry is the event being examined
              number_of_xiccpp[0] = entry
              found_xiccpp_signal |= is_xiccpp_signal
              # ---------------------------------------------------
# ------------------- TreeFilling -------------------
  RunParams.Fill()
  RunLimits.Fill()
  RunDiagnostics.Fill()
  Outputs.Fill()
# ------------------- FileWriting -------------------
file = TFile(f"{basedir}/Outputs/XisTolambdas/Tree{lower}:{upper}.root", "RECREATE")
# Creates temporary tree (deleted when trees are combined)
file.WriteObject(Outputs, "Outputs")
file.WriteObject(RunParams, "RunParams")
file.WriteObject(RunLimits, "RunLimits")
file.WriteObject(RunDiagnostics, "RunDiagnostics")
file.Close()
# ---------------------------------------------------
