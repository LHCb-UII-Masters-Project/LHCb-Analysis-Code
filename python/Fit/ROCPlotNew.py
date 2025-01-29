import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import ROOT
from Variables import *
import ROOT
from ROOT import TGraph
import ctypes
import lhcbstyle
from lhcbstyle import LHCbStyle
#import lhcbstyle

file = "/home/user294/Documents/selections/python/Outputs/TrackSelection/ROCPLOTDATA.csv"
df = pd.read_csv(file)
idata = df.assign(

    XiccppEfficiency = df['#1.TotalXiccppTracks']/df['#1.TotalTrueXiccppTracks'],
    XiccppPurity = df['#1.TotalXiccppTracks']/(df['#1.TotalXiccppTracks']+df['#1.TotalBackgroundTracks']),

    PionEfficiency = df['#2.TotalXiccppPions']/df['#2.TotalTrueXiccppPions'],
    PionPurity = df['#2.TotalXiccppPions']/(df['#2.TotalBackgroundPions'] + df['#2.TotalXiccppPions']),

    KaonEfficiency = df["#3.TotalXiccppKaons"]/df["#3.TotalTrueXiccppKaons"],
    KaonPurity = df["#3.TotalXiccppKaons"]/(df["#3.TotalXiccppKaons"]+ df["#3.TotalBackgroundKaons"])

)
x_xiccpp = idata["XiccppPurity"]
y_xiccpp = idata["XiccppEfficiency"]

x_pion = idata["PionPurity"]
y_pion = idata["PionEfficiency"]

x_kaon = idata["KaonPurity"]
y_kaon = idata["KaonEfficiency"]

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 12))

# Plot for Xiccpp
ax1.scatter(x_xiccpp, y_xiccpp, s=0.5, color='red', label='DisplacedTracks')
ax1.set_xlabel("Purity")
ax1.set_ylabel("Efficiency")
ax1.set_title("Efficiency vs Purity for DisplacedTracks")
ax1.grid(alpha=0.3)
ax1.legend()

# Plot for Pion
ax2.scatter(x_pion, y_pion, s=0.5, color='blue', label='xiccpp_pions')
ax2.set_xlabel("Purity")
ax2.set_ylabel("Efficiency")
ax2.set_title("Efficiency vs Purity for xiccpp_pions")
ax2.grid(alpha=0.3)
ax2.legend()

# Plot for Kaon
ax3.scatter(x_kaon, y_kaon, s=0.5, color='black', label='xiccpp_kaons')
ax3.set_xlabel("Purity")
ax3.set_ylabel("Efficiency")
ax3.set_title("Efficiency vs Purity for xiccpp_kaons")
ax3.grid(alpha=0.3)
ax3.legend()

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig("/home/user294/Documents/selections/python/Fit/triple_plot.png")
