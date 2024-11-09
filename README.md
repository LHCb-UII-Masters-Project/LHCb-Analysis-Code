# LHCb UII Project Notes

PLOT ZONE!!!
## Debug Lines/ Meeting Questions

> How can we introduce Basean analysis into the code, is ROO fit already Basean?
>![signalrelativetobkg1](https://github.com/user-attachments/assets/c6bb8a84-cc96-4af3-ab72-19cd08d4d4f0)
![sigrelativetobkg2](https://github.com/user-attachments/assets/3fcdbdc0-58eb-4253-aecb-6feb452eda79)

>
>



# Code Instructions
## Login for Visualisation Using TigerVNC

Port into the PC with vpn turned on
```
ssh -XY -L 59<##>:localhost59<##> user<####>@<computer>.bham.ac.uk
```

Once logged in create a server
```
vncserver :<##> -localhost
```

To kill the sever
```
vncserver -kill :<##>
```

Open tiger vnc
```
 localhost:59<##>
```

Once logged in, change operating system

```
alma9
```

run the code on the tigervnc terminal for fast visualisation



## Python Code
Problems were encountered in sourcing the required libaries for the python code
In order to correctly source the libaries use
```
alma9
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-clang16-dbg
```

Code to source the cern files

```
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_105 x86_64-el9-gcc12-opt
```
    

# Work log

### Week 1
> Met with project supervisors (Fri) and began reading the
introductory and VELO sections of the [Framework TDR for the LHCb Upgrade II](https://cds.cern.ch/record/2776420?ln=en) (pages 0-47) to gain a background understanding of the project.

### Week 2
> Finished reading relevant sections of the FTDR and confirmed project choices with supervisors. Started the tech set up process, gaining
direct and remote access to the linux desktops. Worked through initialisation tech-gremlins to visualise LHCb Experiment on personal
computers through tiger viewer system.
    
    
### Week 3
>Completed the set up of the git organisation for use throughout the project. Began work on the python analysis code. Problems encountered while attempting to run the analysis code due to incompatible linux versions (incompatiable with alma9). Used
[LHCb Analysis Starter Kit](https://lhcb.github.io/starterkit-lessons/first-analysis-steps/introduction-to-course.html) to better understand the analysis code, >?>commented the <b>BsToDspi.py</b> functions and code for clairty. Proceeded to familiarise with the root fitting programme and syntax.

### Week 4

> Used the resource [CERN Thesis](https://cds.cern.ch/record/2779131/files/CERN-THESIS-2020-360.pdf) to understand the function dira_bpv understanding it to be the constraint that means "the momentum vector of the B0 meson [is] constrained to be parallel to a vector connecting the PV to its decay vertex". I.e. dira_bpv is the angle between the line conecting the decay vertex to the primary vertex and the momentum vector. See diagram below:

![](https://codimd.web.cern.ch/uploads/upload_71564ed2bbc0353f7c1ce44c2f652653.png)

Trying to reconstruct $B^{s}_{0}$ from the D candidates identified in the BsToDsPi.py code provided and then introduce detector effects through Monte-Carlo like randoms.
$$
B^{s}_{0} \rightarrow D^{\mp}_{s} + \pi^{\pm}\\
D^{\mp}_{s} \rightarrow \phi + \pi^{\mp}\\
\text{Quark Content(}\phi\text{) = } k^{-} + k^{+}\\
\text{Overall:}\\
B^{s}_{0} \rightarrow D^{\mp}_{s}(\rightarrow k^{+} + k^{-} + \pi^{\mp}) + \pi^{\pm}$$


>Investigated using Ds tracking to reconstruct a Bs by combining with pions but found Ds are not included in event.Particles (see ParticleLister.py).
Abs(Track ID's of Displaced Tracks):
![](https://codimd.web.cern.ch/uploads/upload_4b59fa424407f5ce51659462219d7aca.png)

>Instead we took the D identified by the given BsToDsPi code cycled through all identified pions, using checking criteria adapted from the D identifier to select appropriate B candidates to create a mass peak for the decaying particle, $B_0^{s}$. 

![](https://codimd.web.cern.ch/uploads/upload_ee630a253103aa36d98ff3b749ff4ad3.png)

>Implemented detection efficiency into the simulation as a function of particle momentum.

> The pion efficiency is roughly constant accross the energy range with 99% of true pions being detected and an extra 1% of pions
being reconstructed falsely from background decays. This requirement was implemented using a random number generator at the track level.

```
  good_pions = [ track for track in displaced_tracks if abs( track.trueID ) == 211 and int(rand.Integer(100))!=12 ] # 99/100 detection         chance
  
  bad_pions = [ track for track in displaced_tracks if abs( track.trueID ) != 211 and int(rand.Integer(100))==23 ] # 1/100 chance of a         misconstructed "pion"
  
  pions = good_pions + bad_pions

```

> Similarly the process was repeated for the k+-, where the detection efficiency depends on the momenta of the kaon.
Using the figure illustrated below, 5 regions represented by liner models were created to estimate the efficiency for a 
given momentum.

![](https://codimd.web.cern.ch/uploads/upload_b1ff9195db571ef4e006c74676e882b5.png)


```
def eff_model(df):
  x, y = np.array(df.iloc[:, 0].astype(float)), np.array(df.iloc[:, 1].astype(float))
  scatter_plot = ROOT.TGraph(len(x), x, y)
  linear_function = ROOT.TF1("linear_function", "[0] + [1]*x", np.min(x), np.max(x))
  scatter_plot.Fit(linear_function)
  return(linear_function.GetParameter(0), linear_function.GetParameter(1))

r1_model = eff_model(pd.read_csv('PEff Kaons/Region 1.csv', skiprows=1))
r2_model = eff_model(pd.read_csv('PEff Kaons/Region 2.csv', skiprows=1))
r3_model = eff_model(pd.read_csv('PEff Kaons/Region 3.csv', skiprows=1))
r4_model = eff_model(pd.read_csv('PEff Kaons/Region 4.csv', skiprows=1))
r5_model = eff_model(pd.read_csv('PEff Kaons/Region 5.csv', skiprows=1))
```

> Once the linear models were created, they were implemented alongside random number generators to simulate efficiency in the simulation

```
 unadjusted_good_kaons = [ track for track in displaced_tracks if abs( track.trueID ) == 321] # all kaons
  
  good_kaons = [] # initialised list to be filled with good kaons
  
  for kaon in unadjusted_good_kaons:
    k_p = np.sqrt((kaon.p4().Px())**2 + (kaon.p4().Py())**2 + (kaon.p4().Pz())**2) # calculate the kaon momentum
    # Adjust conditions and use nested conditionals for efficiency
    if k_p <= 1260*(10**3) and int(rand.Rndm()) <= (r1_model[1] * k_p + r1_model[0]):
        good_kaons.append(kaon)
    elif 1260*(10**3) < k_p <= 8*10**11 and int(rand.Rndm()) <= (r2_model[1] * k_p + r2_model[0]):
        good_kaons.append(kaon)
    elif k_p > 8 * 10**11 and int(rand.Rndm()) <= (r3_model[1] * k_p + r3_model[0]):
        good_kaons.append(kaon)
```
> It is now the case that running our BsReconstructor.py multiple times generates different mass plots due to pseudo-detector effects.

![](https://codimd.web.cern.ch/uploads/upload_144f3306179a5e525080428bbe956dab.png)

>Also made some quality of reading and efficiency improvements by replacing the if statements for model creation with a for loop. This made the code more versitle to different kaon efficiency plots.
```
for i in range(len(boundaries)):
      if (boundaries[i-1] if i > 0 else 0) <= k_p < (boundaries[i] if i != len(boundaries) else np.inf) and int(rand.Rndm()) <= (models[i][1] * k_p + models[i][0]):
        good_kaons.append(kaon)
        continue
```

### Week 5

>Fixed mistake in the reading of Kaon efficiency graphs and added the ability to toggle between different time resolutions.


>![](https://codimd.web.cern.ch/uploads/upload_0ce6c624cacddd1c34d16573e1ef8702.png)

>Figure shows two runs with alternate time resolution, note the differences between the two runs due to the operational randomising code and also the differences between 50 & 200ps timing resolution.

>Prepared for batch running by adding variables that can be defined when the program is called, with the addition of default values.
```
args = sys.argv
try:
  timing_arg = int(args[1]) # user inputted arguments
  pid_switch_arg = int(args[2]) # user inputted arguments
except IndexError:
  timing_arg = 300  # default arguments in the event of no user input
  pid_switch_arg = 1
```

>Saved run info to a ROOT TTree, allowing for faster running and better post processing. Creating the opportunity to compare plots after runs and create seperate analysis code. Thinking to the future, we added a saving procedure so files can be identified later.

```
file = TFile("t=" + str(timing) + "/PID" + str(pid_switch_arg) + "/" + version + "_TreeSize" + str(tree.GetEntries()) + "_Seed_" + str(time.time() * rand_seed[0]) + "_" + time.strftime("%d-%m-%y_%H:%M:%S", time.localtime()) + ".root", "RECREATE")
file.WriteObject(tree, "Tree")
file.WriteObject(b_plot, "B_Histogram")
file.Close()
```

> Produced a binned fitting programme (UnbinnedFitting.py) which fits the binned mass histograms stored in the TTree() using pyROOT. Fits a gaussian to the histogram ( switiching to double crystal ball with chebychev polynomial to better account for the signal and background).

```
gaussFit = ROOT.TF1("gaussfit","gaus",5.20,5.60) # to fit a gaussian
data_hist.Fit(gaussFit ,"E")
```

>Proceeds to create a ratio plot between the model and this histogram data points - gives the model points 0 error on the values.

```
fit_hist = data_hist.Clone("fit_hist")
fit_hist.Reset()

# Fill the new histogram with fit values
for i in range(1, fit_hist.GetNbinsX() + 1):
    x = fit_hist.GetBinCenter(i)
    fit_value = gaussFit.Eval(x)
    fit_hist.SetBinContent(i, fit_value)
    fit_hist.SetBinError(i, 0)  # No error bars for fit histogram

fit_hist.Divide(data_hist)
```

> Calculates the best fit parameters and overlays these onto the plot
```
chi2 = gaussFit.GetChisquare()
ndof = gaussFit.GetNDF()
mean = gaussFit.GetParameter(1)
width = gaussFit.GetParameter(2)


latex.DrawText(0.2,0.85,"Mean = %.3f GeV"%(mean)) 
latex.DrawText(0.2,0.80,"Width = %.3f GeV"%(width)) 
latex.DrawText(0.2,0.75,"chi2/ndof = %.1f/%d = %.1f"%(chi2,ndof,chi2/ndof))
latex.DrawText(0.2, 0.70, "Timing = %d" % timing_value)
latex.DrawText(0.2, 0.65, "Pid Pion = %.1f" % PID_pion_value)
latex.DrawText(0.2, 0.60, "Pid Kaon = %.1f" % PID_kaon_value)
```


> Finally, plots the histogram with the overlayed fit line alongside the ratio plot. Adds the timing and PID toggles onto the canvas for clarity.


![](https://codimd.web.cern.ch/uploads/upload_58447c4292e16a35acdecf3e3a6e0ed6.png)

### Week 6

>In a meeting to discus the future of the project with our superviosrs, it was determined that we would look to model a different decay mode of interest (as stated in the LHCb FTDR). We could then investigate how improved timing resolution improves our ability to reconstruct this decay. We also set some short term goals for the project to be completed before the relevant decay Monte Carlo data could be made available to us. 

>These included; Completing a double crystal ball fit to the MBs data (unbinned), making the random number generation more efficient and reproducable, make quality of life improvements (creating tree using a function), use is-signal test to reveal true signal shape (if possible), read papers on the $\Xi_c^{+} \rightarrow {\Lambda}_{c}^{+} + k^+ + \pi^-$, $\Xi_c^{++} \rightarrow {\Lambda}_{c}^{+} + k^- + \pi^+ + \pi^+$, and $\Xi_c^{++} \rightarrow \Xi_c^{+} + \pi^+$ decays (found ond PDG Live), consider how constructing such decays would be fifferent to the BsToDsPi we have been reconstructing so far (i.e. no displaced vertices), and setup Condor to begin batch running. 

Euan: Making the random number generator more efficient and reproducable.
Jack: Switch to unbinned fitting.
Euan: Batching then change how the tree is created (quality of life improvement).
