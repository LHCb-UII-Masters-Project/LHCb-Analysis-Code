import ROOT
# Assuming variables.py contains the initial guesses, mins, and maxes
variables = {
    'mu': {'value': 3.622, 
           'min': 3.6, 'max': 3.67},
    
    'sigma': {'value': 0.006044, 
              'min': 0.0036, 'max': 0.01},
    
    'alphaL': {'value': 2.321, 
               'min': 0.01, 'max': 6},
    
    'alphaR': {'value': 2.985, 
               'min': 0.45, 'max': 5},
    
    'nL': {'value': 1.995, 
           'min': 0.00001, 'max': 6},
    
    'nR': {'value': 0.03804, 
           'min': 0.01, 'max': 4},
    
    'bkg_coef1': {'value':0.1
                       , 'min': -3, 'max': 3},
    
    'bkg_coef2': {'value':0.1
                     , 'min': -3, 'max': 3},
    
    'nbkg': {'value': 8332, 
             'min': 1000, 'max': 10000},
    
    'nsig': {'value': 1170,
              'min': 400, 'max': 3000}
}


# Create the ROOT TTree
fit_initial_guess_tree = ROOT.TTree("fit_initial_guess", "fit_initial_guess_tree")

# Create the vectors for initial values, mins, and maxes
mean_guess = ROOT.std.vector('float')()
sigma_guess = ROOT.std.vector('float')()
alphaL_guess = ROOT.std.vector('float')()
alphaR_guess = ROOT.std.vector('float')()
nL_guess = ROOT.std.vector('float')()
nR_guess = ROOT.std.vector('float')()
bkg_coef1_guess = ROOT.std.vector('float')()
bkg_coef2_guess = ROOT.std.vector('float')()
nbkg_guess = ROOT.std.vector('float')()
nsig_guess = ROOT.std.vector('float')()

mean_min = ROOT.std.vector('float')()
sigma_min = ROOT.std.vector('float')()
alphaL_min = ROOT.std.vector('float')()
alphaR_min = ROOT.std.vector('float')()
nL_min = ROOT.std.vector('float')()
nR_min = ROOT.std.vector('float')()
bkg_coef1_min = ROOT.std.vector('float')()
bkg_coef2_min = ROOT.std.vector('float')()
nbkg_min = ROOT.std.vector('float')()
nsig_min = ROOT.std.vector('float')()

mean_max = ROOT.std.vector('float')()
sigma_max = ROOT.std.vector('float')()
alphaL_max = ROOT.std.vector('float')()
alphaR_max = ROOT.std.vector('float')()
nL_max = ROOT.std.vector('float')()
nR_max = ROOT.std.vector('float')()
bkg_coef1_max = ROOT.std.vector('float')()
bkg_coef2_max = ROOT.std.vector('float')()
nbkg_max = ROOT.std.vector('float')()
nsig_max = ROOT.std.vector('float')()

# Add the values to the vectors
mean_guess.push_back(variables['mu']['value'])
sigma_guess.push_back(variables['sigma']['value'])
alphaL_guess.push_back(variables['alphaL']['value'])
alphaR_guess.push_back(variables['alphaR']['value'])
nL_guess.push_back(variables['nL']['value'])
nR_guess.push_back(variables['nR']['value'])
bkg_coef1_guess.push_back(variables['bkg_coef1']['value'])
bkg_coef2_guess.push_back(variables['bkg_coef2']['value'])
nbkg_guess.push_back(variables['nbkg']['value'])
nsig_guess.push_back(variables['nsig']['value'])

mean_min.push_back(variables['mu']['min'])
sigma_min.push_back(variables['sigma']['min'])
alphaL_min.push_back(variables['alphaL']['min'])
alphaR_min.push_back(variables['alphaR']['min'])
nL_min.push_back(variables['nL']['min'])
nR_min.push_back(variables['nR']['min'])
bkg_coef1_min.push_back(variables['bkg_coef1']['min'])
bkg_coef2_min.push_back(variables['bkg_coef2']['min'])
nbkg_min.push_back(variables['nbkg']['min'])
nsig_min.push_back(variables['nsig']['min'])

mean_max.push_back(variables['mu']['max'])
sigma_max.push_back(variables['sigma']['max'])
alphaL_max.push_back(variables['alphaL']['max'])
alphaR_max.push_back(variables['alphaR']['max'])
nL_max.push_back(variables['nL']['max'])
nR_max.push_back(variables['nR']['max'])
bkg_coef1_max.push_back(variables['bkg_coef1']['max'])
bkg_coef2_max.push_back(variables['bkg_coef2']['max'])
nbkg_max.push_back(variables['nbkg']['max'])
nsig_max.push_back(variables['nsig']['max'])

# Create branches in the TTree for guesses, mins, and maxes
fit_initial_guess_tree.Branch("mean_guess", mean_guess)
fit_initial_guess_tree.Branch("sigma_guess", sigma_guess)
fit_initial_guess_tree.Branch("alphaL_guess", alphaL_guess)
fit_initial_guess_tree.Branch("alphaR_guess", alphaR_guess)
fit_initial_guess_tree.Branch("nL_guess", nL_guess)
fit_initial_guess_tree.Branch("nR_guess", nR_guess)
fit_initial_guess_tree.Branch("bkg_coef1_guess", bkg_coef1_guess)
fit_initial_guess_tree.Branch("bkg_coef2_guess", bkg_coef2_guess)
fit_initial_guess_tree.Branch("nbkg_guess", nbkg_guess)
fit_initial_guess_tree.Branch("nsig_guess", nsig_guess)

fit_initial_guess_tree.Branch("mean_min", mean_min)
fit_initial_guess_tree.Branch("sigma_min", sigma_min)
fit_initial_guess_tree.Branch("alphaL_min", alphaL_min)
fit_initial_guess_tree.Branch("alphaR_min", alphaR_min)
fit_initial_guess_tree.Branch("nL_min", nL_min)
fit_initial_guess_tree.Branch("nR_min", nR_min)
fit_initial_guess_tree.Branch("bkg_coef1_min", bkg_coef1_min)
fit_initial_guess_tree.Branch("bkg_coef2_min", bkg_coef2_min)
fit_initial_guess_tree.Branch("nbkg_min", nbkg_min)
fit_initial_guess_tree.Branch("nsig_min", nsig_min)

fit_initial_guess_tree.Branch("mean_max", mean_max)
fit_initial_guess_tree.Branch("sigma_max", sigma_max)
fit_initial_guess_tree.Branch("alphaL_max", alphaL_max)
fit_initial_guess_tree.Branch("alphaR_max", alphaR_max)
fit_initial_guess_tree.Branch("nL_max", nL_max)
fit_initial_guess_tree.Branch("nR_max", nR_max)
fit_initial_guess_tree.Branch("bkg_coef1_max", bkg_coef1_max)
fit_initial_guess_tree.Branch("bkg_coef2_max", bkg_coef2_max)
fit_initial_guess_tree.Branch("nbkg_max", nbkg_max)
fit_initial_guess_tree.Branch("nsig_max", nsig_max)

# Fill the tree (usually you would do this inside an event loop)
fit_initial_guess_tree.Fill()
