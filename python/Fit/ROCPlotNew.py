import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import ROOT
from ROOT import TGraph
import ctypes
import lhcbstyle
from lhcbstyle import LHCbStyle
import matplotlib.ticker as ticker 

#import lhcbstyle
new_numerator = True

file = "/home/user293/Documents/selections/python/Outputs/TrackSelection/Batch4D.csv"
df = pd.read_csv(file)

if new_numerator is True:
    idata = df.assign(

        XiccppEfficiency = df['#1.TotalXiLcDaughterTracks']/df['#1.TotalTrueXiLcDaughterTracks'],
        XiccppPurity =  1 -( df['#1.TotalXiLcBackgroundTracks']/(df['#1.TotalXiLcDaughterTracks']+df['#1.TotalXiLcBackgroundTracks'])),

        PionEfficiency = df['#2.TotalBachelorPionTracks']/df['#2.TotalTrueBachelorPionTracks'],
        PionPurity =  1-(df['#2.TotalBachelorPionBackgroundTracks']/(df['#2.TotalBachelorPionBackgroundTracks'] + df['#2.TotalBachelorPionTracks'])),

        KaonEfficiency = df["#3.TotalBachelorKaonTracks"]/df["#3.TotalTrueBachelorKaonTracks"],
        KaonPurity = 1 - (df["#3.TotalBackgroundBachelorKaons"]/(df["#3.TotalBachelorKaonTracks"]+ df["#3.TotalBackgroundBachelorKaons"]))
    )
else:
    idata = df.assign(

        XiccppEfficiency = df['#1.TotalXiccppTracks']/df['#1.TotalTrueXiccppTracks'],
        XiccppPurity =  1 -( df['#1.TotalBackgroundTracks']/(df['#1.TotalXiccppTracks']+df['#1.TotalBackgroundTracks'])),

        PionEfficiency = df['#2.TotalXiccppPions']/df['#2.TotalTrueXiccppPions'],
        PionPurity =  1-(df['#2.TotalBackgroundPions']/(df['#2.TotalBackgroundPions'] + df['#2.TotalXiccppPions'])),

        KaonEfficiency = df["#3.TotalXiccppKaons"]/df["#3.TotalTrueXiccppKaons"],
        KaonPurity = 1 - (df["#3.TotalBackgroundKaons"]/(df["#3.TotalXiccppKaons"]+ df["#3.TotalBackgroundKaons"]))
    )

paper_lc_values = idata.query('MinP == 2000 and MinPT == 200 and MinIPChi2 == 6')
paper_xi_values = idata.query('MinP == 1000 and MinPT == 500')

DisplacedTracksDict = {
  "efficiency_minimum":0.63,
  "efficiency_maximum":0.65,
  "purity_minimum":0.014,
  "purity_maximum":0.017
  }

XiccppPionsDict = {
 "efficiency_minimum":0.32,
  "efficiency_maximum":0.43,
  "purity_minimum":0.0052,
  "purity_maximum":0.006
}

XiccppKaonsDict = {
 "efficiency_minimum":0.6,
  "efficiency_maximum":0.63,
  "purity_minimum":0.018,
  "purity_maximum":0.024
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

fig, axs = plt.subplots(3, figsize=(15, 30))
DisplacedTracksScatter = axs[0]
XiccppPionScatter = axs[1]
XiccppKaonScatter = axs[2]
# Plot for Xiccpp (top-left and top-right)
DisplacedTracksScatter.scatter(data = idata, x = "XiccppEfficiency", y = "XiccppPurity", s=30, color='black', label='DisplacedTracks')
DisplacedTracksScatter.scatter(data = paper_lc_values, x = "XiccppEfficiency", y = "XiccppPurity", s=30, color='red', label='LcPaperValues')
DisplacedTracksScatter.scatter(data = paper_xi_values, x = "XiccppEfficiency", y = "XiccppPurity", s=30, color='blue', label='XiPaperValues')
# Annotate each point
# Annotate each point
"""
for i, row in idata_unique.iterrows():
    DisplacedTracksScatter.annotate(
        f'[{row["MinP"],row["MinPT"],row["MinIPChi2"]}]', 
        (row["XiccppEfficiency"], row["XiccppPurity"]),  # Use the correct coordinates
        textcoords="offset points",
        xytext=(0, 0),  # Offset the text slightly
        ha='center', fontsize=8  # Corrected capitalization and fontsize
    )
"""

DisplacedTracksScatter.set_xlabel("Efficiency")
DisplacedTracksScatter.set_ylabel("Purity")
DisplacedTracksScatter.set_title("Efficiency vs Purity for DisplacedTracks")
DisplacedTracksScatter.grid(alpha=0.3)
DisplacedTracksScatter.legend()
#xspace = 0.0025  # You can change this value to set the spacing of ticks
#yspace = 0.00005  # You can change this value to set the spacing of ticks
#DisplacedTracksScatter.yaxis.set_major_locator(ticker.MultipleLocator(yspace))
#DisplacedTracksScatter.xaxis.set_major_locator(ticker.MultipleLocator(xspace))

# Plot for Pion (middle-left and middle-right)
XiccppPionScatter.scatter(data = idata , x = "PionEfficiency",y = "PionPurity", s = 30, color='black', label='xiccpp_pions')
XiccppPionScatter.scatter(data = paper_lc_values, x = "PionEfficiency", y = "PionPurity", s=30, color='red', label='LcPaperValuesPions')
XiccppPionScatter.scatter(data = paper_xi_values, x = "PionEfficiency", y = "PionPurity", s=30, color='blue', label='XiPaperValuesPions')

"""
for i, row in pion_zoomed.iterrows():
    XiccppPionScatter.annotate(
        f'[{row["MinP"],row["MinPT"],row["MinIPChi2"]}]', 
        (row["PionEfficiency"], row["PionPurity"]),  # Use the correct coordinates
        textcoords="offset points",
        xytext=(0, 0),  # Offset the text slightly
        ha='center', fontsize=8  # Corrected capitalization and fontsize
    )
"""

XiccppPionScatter.set_xlabel("Efficiency")
XiccppPionScatter.set_ylabel("Purity")
XiccppPionScatter.set_title("Efficiency vs Purity for xiccpp_pions")
XiccppPionScatter.grid(alpha=0.3)
XiccppPionScatter.legend()

#xspace = 0.0025  # You can change this value to set the spacing of ticks
#yspace = 0.00005  # You can change this value to set the spacing of ticks
#XiccppPionScatter.yaxis.set_major_locator(ticker.MultipleLocator(yspace))
#XiccppPionScatter.xaxis.set_major_locator(ticker.MultipleLocator(xspace))

# Plot for Kaon (bottom-left and bottom-right)
XiccppKaonScatter.scatter(data = idata , x = "KaonEfficiency",y = "KaonPurity", s = 30, color='black', label='xiccpp_kaons')
XiccppKaonScatter.scatter(data = paper_lc_values, x = "KaonEfficiency", y = "KaonPurity", s=30, color='red', label='LcPaperValuesKaons')
XiccppKaonScatter.scatter(data = paper_xi_values, x = "KaonEfficiency", y = "KaonPurity", s=30, color='blue', label='XiPaperValuesKaons')

"""
for i, row in kaon_zoomed.iterrows():
    XiccppKaonScatter.annotate(
        f'[{row["MinP"],row["MinPT"],row["MinIPChi2"]}]', 
        (row["KaonEfficiency"], row["KaonPurity"]),  # Use the correct coordinates
        textcoords="offset points",
        xytext=(0, 0),  # Offset the text slightly
        ha='center', fontsize=8  # Corrected capitalization and fontsize
    )
"""

XiccppKaonScatter.set_xlabel("Efficiency")
XiccppKaonScatter.set_ylabel("Purity")
XiccppKaonScatter.set_title("Efficiency vs Purity for xiccpp_kaons")
XiccppKaonScatter.grid(alpha=0.3)
XiccppKaonScatter.legend()
#xspace = 0.025  # You can change this value to set the spacing of ticks
#yspace = 0.005  # You can change this value to set the spacing of ticks
#XiccppKaonScatter.yaxis.set_major_locator(ticker.MultipleLocator(yspace))
#XiccppKaonScatter.xaxis.set_major_locator(ticker.MultipleLocator(xspace))


# Adjust layout and save the figure
plt.tight_layout()
if new_numerator is True:
    plt.savefig("/home/user293/Documents/selections/python/Fit/batch_newnewtrip_plot_4D.pdf", format='pdf', dpi=350)
else:
    plt.savefig("/home/user293/Documents/selections/python/Fit/batch_newoldtrip_plot_4D.pdf", format='pdf', dpi=350)


# Chosen trade-off values:

# [purity, efficiency]
dis_tracks_coords = [0.018, 0.56]
xiccpp_pions_coords = [0.01575, 0.325]
xiccpp_kaons_coords = [0.094, 0.45]

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
