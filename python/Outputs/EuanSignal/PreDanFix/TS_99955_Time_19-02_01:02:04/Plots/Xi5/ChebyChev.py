import ROOT
# Assuming variables.py contains the initial guesses, mins, and maxes
variables = {
    'mu': {'value': 3.5189, 
           'min': 3.5, 'max': 3.6},
    
    'sigma': {'value': 0.003436, 
              'min': 0.003, 'max': 0.004},
    
    'alphaL': {'value': 1.478, 
               'min': 1.3, 'max': 1.6},
    
    'alphaR': {'value': 1.623, 
               'min': 1, 'max': 2.3},
    
    'nL': {'value': 20, 
           'min': 17, 'max': 23},
    
    'nR': {'value': 3.853, 
           'min': 2.7, 'max': 5},
    
    'bkg_coef1': {'value':-0.1
                       , 'min': -1, 'max': 1},
    
    'bkg_coef2': {'value':-0.01
                     , 'min': -1, 'max': 1},
    
    'nbkg': {'value': 6674, 
             'min': 5200, 'max': 7000},
    
    'nsig': {'value': 2681,
              'min': 1500, 'max': 3061}
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
