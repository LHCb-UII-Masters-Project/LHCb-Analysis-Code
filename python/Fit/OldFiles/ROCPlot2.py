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


lambdas_true = 464
xilambdas_true = 504
xikaons_true = 493
xipions_true = 973
xi_true = 399
#file = "/home/user294/Documents/selections/python/Outputs/TrackSelection/LambdacCompIPALL.csv"
file = "/home/user294/Documents/selections/python/Outputs/TrackSelection/XiCompIPALL.csv"
df = pd.read_csv(file)
df['#Lambdas'] = df['#Lambdas']* lambdas_true
df['#XiLambdas'] = df['#XiLambdas'] * xilambdas_true
df['#XiKaons'] = df['#XiKaons'] *xikaons_true
df['#XiPions'] = df['#XiPions'] * xipions_true
df["#Xis"] = df['#Xis']*xi_true
def normalise(column):
    return (column - column.min()) / (column.max() - column.min())

df_calc = df.assign(
                LambdacSignalEfficiency= df['#Lambdas']/lambdas_true,
                LambdacSignalPurity=  (df['#XiLambdas']/(df["#Pion"] * df["#Proton"] * df["#Kaon"])),   
                normalised_MinPT = normalise(df['MinPT']),
                normalised_MinP = normalise(df["MinP"]),
                normalised_MinIPChi2 = normalise(df["MinIPChi2"])
                )

# Get the unique combinations of x and y
df_unique = df_calc.drop_duplicates(subset=["LambdacSignalPurity", "LambdacSignalEfficiency"])
df_filtered = df_unique[df_unique["LambdacSignalEfficiency"] >0.8]
# Now extract the unique x and y values
df_normalised = df_filtered.assign(
    NormalisedPurity = normalise(df_filtered["LambdacSignalPurity"]),
    NormalisedEfficiency = normalise(df_filtered["LambdacSignalEfficiency"])
)
x_norm = df_normalised["NormalisedPurity"]
y_norm = df_normalised["NormalisedEfficiency"]

x_filtered = df_filtered["LambdacSignalPurity"]
y_filtered = df_filtered["LambdacSignalEfficiency"]


distance = np.sqrt(x_norm**2 + y_norm**2)
max_distance_index = distance.idxmax()
max_distance_row = df_filtered.loc[max_distance_index]

root_purity_efficiency = np.sqrt(x_norm*y_norm)
max_root_purity_efficiency_index = root_purity_efficiency.idxmax()
max_root_purity_efficiency_row = df_filtered.loc[max_root_purity_efficiency_index]

print(f"distance maximum : {max_distance_row["LambdacSignalPurity"],max_distance_row["LambdacSignalEfficiency"]}")
print(f"max root purity: {max_root_purity_efficiency_row["LambdacSignalPurity"],max_root_purity_efficiency_row["LambdacSignalEfficiency"]}")
# Create a TGraph object to represent the data
graph = ROOT.TGraph(len(np.array(x_norm)), np.array(x_norm), np.array(y_norm))

# Define a power-law function: y = C * x^(-alpha)
# TF1 accepts a formula where [0] is C and [1] is alpha
power_law_function = ROOT.TF1("power_law", "[0] * x^(-[1])", 0,1)
power_law_function.SetParameters(1, -0.1)  # Guess: C=1, alpha=1

linear_function = ROOT.TF1("linear", "[0] + x*([1])", 0, 1)
linear_function.SetParameters(1,-0.5)

# Fit the graph data to the power-law function
graph.Fit("linear")

# Retrieve fitted parameters
C_fit= linear_function.GetParameter(0)
alpha_fit = linear_function.GetParameter(1)

with LHCbStyle() as lbs:
        # Create a ROOT canvas
    canvas = ROOT.TCanvas("canvas", "fit", 800, 600)
    # Set axis labels

    # Draw the graph and the fitted function
    graph.Draw("AP")
    linear_function.Draw("SAME")

    # Add labels and legend
    graph.SetTitle("Normalised Purity;Normalised Efficiency")
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(1)
    graph.SetMarkerColor(ROOT.kBlue)
    legend = ROOT.TLegend(0.67, 0.7, 0.97, 0.915) 
    legend.AddEntry(graph, "Data", "p")
    legend.AddEntry(linear_function, "Fit", "l")
    legend.SetLineColor(0)  # Remove the legend border
    legend.SetLineStyle(0)  # Ensure no border line style
    legend.SetLineWidth(0)  # Set line width to 0
    legend.SetFillColor(0)  # Remove any fill color
    legend.SetFillStyle(0)  # Ensure no fill style
    legend.SetTextFont(62)  # Helvetica, normal
    legend.SetTextSize(0.030)  # Adjust text size as needed
    legend.Draw()
    graph.GetXaxis().SetTitle("Normalised Purity")
    graph.GetYaxis().SetTitle("Normalised Efficiency")

    # Save the plot
    canvas.SaveAs("freq_fit.png")

    canvas2= ROOT.TCanvas("canvas", "fit", 1000, 600)
    graph2 = ROOT.TGraph(len(np.array(x_filtered)), np.array(x_filtered), np.array(y_filtered))

    # Set axis labels

    # Draw the graph and the fitted function
    graph2.Draw("AP")
    graph2.GetXaxis().SetTitle("Purity")
    graph2.GetYaxis().SetTitle("Efficiency")

    # Save the plot
    canvas2.SaveAs("test.png")