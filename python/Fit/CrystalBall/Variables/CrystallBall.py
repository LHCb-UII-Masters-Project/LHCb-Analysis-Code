import ROOT
# Assuming variables.py contains the initial guesses, mins, and maxes
variables = {
    'mu': {'value': 3.622, 
           'min': 3.6, 'max': 3.63},
    
    'sigma': {'value': 0.00429, 
              'min': 0.0030, 'max': 0.0060},
    
    'alphaL': {'value': 2.570, 
               'min': 1.5, 'max': 3.5},
    
    'alphaR': {'value': 2.501, 
               'min': 1.5, 'max': 3.5},
    
    'nL': {'value': 1.132, 
           'min': 0.5, 'max': 2},
    
    'nR': {'value': 0.5271, 
           'min': 0.3, 'max': 1}
    
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
mean_min = ROOT.std.vector('float')()
sigma_min = ROOT.std.vector('float')()
alphaL_min = ROOT.std.vector('float')()
alphaR_min = ROOT.std.vector('float')()
nL_min = ROOT.std.vector('float')()
nR_min = ROOT.std.vector('float')()
mean_max = ROOT.std.vector('float')()
sigma_max = ROOT.std.vector('float')()
alphaL_max = ROOT.std.vector('float')()
alphaR_max = ROOT.std.vector('float')()
nL_max = ROOT.std.vector('float')()
nR_max = ROOT.std.vector('float')()
# Add the values to the vectors
mean_guess.push_back(variables['mu']['value'])
sigma_guess.push_back(variables['sigma']['value'])
alphaL_guess.push_back(variables['alphaL']['value'])
alphaR_guess.push_back(variables['alphaR']['value'])
nL_guess.push_back(variables['nL']['value'])
nR_guess.push_back(variables['nR']['value'])

mean_min.push_back(variables['mu']['min'])
sigma_min.push_back(variables['sigma']['min'])
alphaL_min.push_back(variables['alphaL']['min'])
alphaR_min.push_back(variables['alphaR']['min'])
nL_min.push_back(variables['nL']['min'])
nR_min.push_back(variables['nR']['min'])

mean_max.push_back(variables['mu']['max'])
sigma_max.push_back(variables['sigma']['max'])
alphaL_max.push_back(variables['alphaL']['max'])
alphaR_max.push_back(variables['alphaR']['max'])
nL_max.push_back(variables['nL']['max'])
nR_max.push_back(variables['nR']['max'])

# Create branches in the TTree for guesses, mins, and maxes
fit_initial_guess_tree.Branch("mean_guess", mean_guess)
fit_initial_guess_tree.Branch("sigma_guess", sigma_guess)
fit_initial_guess_tree.Branch("alphaL_guess", alphaL_guess)
fit_initial_guess_tree.Branch("alphaR_guess", alphaR_guess)
fit_initial_guess_tree.Branch("nL_guess", nL_guess)
fit_initial_guess_tree.Branch("nR_guess", nR_guess)
fit_initial_guess_tree.Branch("mean_min", mean_min)
fit_initial_guess_tree.Branch("sigma_min", sigma_min)
fit_initial_guess_tree.Branch("alphaL_min", alphaL_min)
fit_initial_guess_tree.Branch("alphaR_min", alphaR_min)
fit_initial_guess_tree.Branch("nL_min", nL_min)
fit_initial_guess_tree.Branch("nR_min", nR_min)

fit_initial_guess_tree.Branch("mean_max", mean_max)
fit_initial_guess_tree.Branch("sigma_max", sigma_max)
fit_initial_guess_tree.Branch("alphaL_max", alphaL_max)
fit_initial_guess_tree.Branch("alphaR_max", alphaR_max)
fit_initial_guess_tree.Branch("nL_max", nL_max)
fit_initial_guess_tree.Branch("nR_max", nR_max)

# Fill the tree (usually you would do this inside an event loop)
fit_initial_guess_tree.Fill()
