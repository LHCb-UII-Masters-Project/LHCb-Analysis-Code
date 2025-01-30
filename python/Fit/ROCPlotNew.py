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
import matplotlib.ticker as ticker 

#import lhcbstyle

file = "/home/user293/Documents/selections/python/Outputs/TrackSelection/ROCPLOTDATA.csv"
df = pd.read_csv(file)
idata = df.assign(

    XiccppEfficiency = df['#1.TotalXiccppTracks']/df['#1.TotalTrueXiccppTracks'],
    XiccppPurity =  1 -( df['#1.TotalBackgroundTracks']/(df['#1.TotalXiccppTracks']+df['#1.TotalBackgroundTracks'])),

    PionEfficiency = df['#2.TotalXiccppPions']/df['#2.TotalTrueXiccppPions'],
    PionPurity =  1-(df['#2.TotalBackgroundPions']/(df['#2.TotalBackgroundPions'] + df['#2.TotalXiccppPions'])),

    KaonEfficiency = df["#3.TotalXiccppKaons"]/df["#3.TotalTrueXiccppKaons"],
    KaonPurity = 1 - (df["#3.TotalBackgroundKaons"]/(df["#3.TotalXiccppKaons"]+ df["#3.TotalBackgroundKaons"]))

)
DisplacedTracksDict = {
  "efficiency_minimum":0.6,
  "efficiency_maximum":0.8,
  "purity_minimum":0.0125,
  "purity_maximum":0.013
  }

XiccppPionsDict = {
 "efficiency_minimum":321,
  "efficiency_maximum":211,
  "purity_minimum":2212,
  "purity_maximum":4122
}

XiccppKaonsDict = {
 "efficiency_minimum":321,
  "efficiency_maximum":211,
  "purity_minimum":2212,
  "purity_maximum":4122
}

def df_zoom(idata, efficiency_column, purity_column, dictionary):
    eff_min = dictionary["efficiency_minimum"]
    eff_max = dictionary["efficiency_maximum"]
    purity_min = dictionary["purity_minimum"]
    purity_max = dictionary["purity_maximum"]

    zoomed_df = idata[(idata[efficiency_column] >= eff_min) & 
                 (idata[efficiency_column] <= eff_max) &
                 (idata[purity_column] >= purity_min) &
                 (idata[purity_column] <= purity_max)]
    return zoomed_df[~zoomed_df[['XiccppPurity', 'XiccppEfficiency']].duplicated(keep=False)]


# Example usage
xiccpp_zoomed = df_zoom(idata, "XiccppEfficiency", "XiccppPurity", DisplacedTracksDict)
pion_zoomed = df_zoom(idata,"PionEfficiency","PionPurity",XiccppPionsDict)
kaon_zoomed = df_zoom(idata,"KaonEfficiency","KaonPurity",XiccppKaonsDict)


idata_unique = idata.drop_duplicates(subset=["XiccppPurity", "XiccppEfficiency"])
unique_pion = idata.drop_duplicates(subset=["PionPurity", "PionEfficiency"])
unique_kaon = idata.drop_duplicates(subset=["KaonPurity", "KaonEfficiency"])

idata_unique_sorted = idata_unique.sort_values(by="XiccppEfficiency", ascending=True)
unique_pion_sorted = unique_pion.sort_values(by="PionEfficiency", ascending=True)
unique_kaon_sorted = unique_kaon.sort_values(by="KaonEfficiency", ascending=True)

fig, axs = plt.subplots(3, figsize=(10, 20))
DisplacedTracksScatter = axs[0]
XiccppPionScatter = axs[1]
XiccppKaonScatter = axs[2]
# Plot for Xiccpp (top-left and top-right)
DisplacedTracksScatter.scatter(idata_unique["XiccppEfficiency"],idata_unique["XiccppPurity"], s=30, color='black', label='DisplacedTracks')
DisplacedTracksScatter.plot(idata_unique_sorted["XiccppEfficiency"],idata_unique_sorted["XiccppPurity"], color = 'red')
DisplacedTracksScatter.set_xlabel("Efficiency")
DisplacedTracksScatter.set_ylabel("Background Rejection")
DisplacedTracksScatter.set_title("Efficiency vs background rejection for DisplacedTracks")
DisplacedTracksScatter.grid(alpha=0.3)
DisplacedTracksScatter.legend()
xspace = 0.025  # You can change this value to set the spacing of ticks
yspace = 0.001  # You can change this value to set the spacing of ticks
DisplacedTracksScatter.yaxis.set_major_locator(ticker.MultipleLocator(yspace))
DisplacedTracksScatter.xaxis.set_major_locator(ticker.MultipleLocator(xspace))


# Plot for Pion (middle-left and middle-right)
XiccppPionScatter.scatter(unique_pion["PionEfficiency"],unique_pion["PionPurity"], s = 30, color='black', label='xiccpp_pions')
XiccppPionScatter.plot(unique_pion_sorted["PionEfficiency"],unique_pion_sorted["PionPurity"], color = 'red')
XiccppPionScatter.set_xlabel("Efficiency")
XiccppPionScatter.set_ylabel("Background Rejection")
XiccppPionScatter.set_title("Efficiency vs background rejection for xiccpp_pions")
XiccppPionScatter.grid(alpha=0.3)
XiccppPionScatter.legend()
xspace = 0.025  # You can change this value to set the spacing of ticks
yspace = 0.0001  # You can change this value to set the spacing of ticks
XiccppPionScatter.yaxis.set_major_locator(ticker.MultipleLocator(yspace))
XiccppPionScatter.xaxis.set_major_locator(ticker.MultipleLocator(xspace))

# Plot for Kaon (bottom-left and bottom-right)
XiccppKaonScatter.scatter(unique_kaon["KaonEfficiency"],unique_kaon["KaonPurity"], s= 30, color='black', label='xiccpp_kaons')
XiccppKaonScatter.plot(unique_kaon_sorted["KaonEfficiency"],unique_kaon_sorted["KaonPurity"], color = 'red')
XiccppKaonScatter.set_xlabel("Efficiency")
XiccppKaonScatter.set_ylabel("Background Rejection")
XiccppKaonScatter.set_title("Efficiency vs background rejection for xiccpp_kaons")
XiccppKaonScatter.grid(alpha=0.3)
XiccppKaonScatter.legend()
xspace = 0.025  # You can change this value to set the spacing of ticks
yspace = 0.001  # You can change this value to set the spacing of ticks
XiccppKaonScatter.yaxis.set_major_locator(ticker.MultipleLocator(yspace))
XiccppKaonScatter.xaxis.set_major_locator(ticker.MultipleLocator(xspace))


# Adjust layout and save the figure
plt.tight_layout()
plt.savefig("/home/user293/Documents/selections/python/Fit/triple_plot.pdf", format='pdf', dpi=350)


# Chosen trade-off values:

dis_tracks_coords = [0.0015, 0.550]
xiccpp_pions_coords = [0.0069, 0.4]
xiccpp_kaons_coords = [0.036, 0.675]

jdata = df.assign(
    dis_track_min = ((idata["XiccppPurity"] - dis_tracks_coords[0])/dis_tracks_coords[0]) * ((idata["XiccppEfficiency"] - dis_tracks_coords[1])/dis_tracks_coords[1]),
    xipion_track_min = ((idata["PionPurity"] - xiccpp_pions_coords[0])/xiccpp_pions_coords[0]) * ((idata["PionEfficiency"] - xiccpp_pions_coords[1])/xiccpp_pions_coords[1]),
    xikaons_track_min = ((idata["KaonPurity"] - xiccpp_kaons_coords[0])/xiccpp_kaons_coords[0]) * ((idata["KaonEfficiency"] - xiccpp_kaons_coords[1])/xiccpp_kaons_coords[1])
)

dis_track_ID = df.loc[jdata["dis_track_min"].idxmin()]
xipion_track_ID = df.loc[jdata["xipion_track_min"].idxmin()]
xikaon_track_ID = df.loc[jdata["xikaons_track_min"].idxmin()]

track_ids = [dis_track_ID, xipion_track_ID, xikaon_track_ID]
track_id_names = ["Displaced", "XiPion", "XiKaons"]
for i, ID in enumerate(track_ids):
    print(f"{track_id_names[i]} Tracks Min_PT = " + str(ID["MinPT"]))
    print((f"{track_id_names[i]} Tracks Min_P = " + str(ID["MinP"])))
    print(f"{track_id_names[i]} MinIPChi2 = " + str(ID["MinIPChi2"]))
