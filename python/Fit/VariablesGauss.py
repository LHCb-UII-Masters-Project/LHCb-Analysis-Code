import ROOT
# Assuming variables.py contains the initial guesses, mins, and maxes
variables = {
    'mu': {'value': 5.366744099, 
           'min': 5.35, 'max': 5.38},
    
    'sigma': {'value': 0.01477, 
              'min': 0.01430, 'max': 0.0170},
    
    'nsig': {'value': 28700, 'min': 26000, 'max': 30000}
}

# Create the ROOT TTree
fit_initial_guess_tree = ROOT.TTree("fit_initial_guess", "fit_initial_guess_tree")

# Create the vectors for initial values, mins, and maxes
mean_guess = ROOT.std.vector('float')()
sigma_guess = ROOT.std.vector('float')()
nsig_guess = ROOT.std.vector('float')()
mean_min = ROOT.std.vector('float')()
sigma_min = ROOT.std.vector('float')()
nsig_min = ROOT.std.vector('float')()
mean_max = ROOT.std.vector('float')()
sigma_max = ROOT.std.vector('float')()
nsig_max = ROOT.std.vector('float')()
mean_guess.push_back(variables['mu']['value'])
sigma_guess.push_back(variables['sigma']['value'])
nsig_guess.push_back(variables['nsig']['value'])
mean_min.push_back(variables['mu']['min'])
sigma_min.push_back(variables['sigma']['min'])
nsig_min.push_back(variables['nsig']['min'])
mean_max.push_back(variables['mu']['max'])
sigma_max.push_back(variables['sigma']['max'])
nsig_max.push_back(variables['nsig']['max'])
# Create branches in the TTree for guesses, mins, and maxes
fit_initial_guess_tree.Branch("mean_guess", mean_guess)
fit_initial_guess_tree.Branch("sigma_guess", sigma_guess)
fit_initial_guess_tree.Branch("nsig_guess", nsig_guess)
fit_initial_guess_tree.Branch("mean_min", mean_min)
fit_initial_guess_tree.Branch("sigma_min", sigma_min)
fit_initial_guess_tree.Branch("nsig_min", nsig_min)
fit_initial_guess_tree.Branch("mean_max", mean_max)
fit_initial_guess_tree.Branch("sigma_max", sigma_max)
fit_initial_guess_tree.Branch("nsig_max", nsig_max)

# Fill the tree (usually you would do this inside an event loop)
fit_initial_guess_tree.Fill()
