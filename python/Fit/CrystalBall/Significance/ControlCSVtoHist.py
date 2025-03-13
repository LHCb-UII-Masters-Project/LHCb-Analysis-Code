import ROOT
import pandas as pd
import numpy as np
from ROOT import TCanvas, TH1D, TLine, TLegend

# Read CSV
csv_file = "/home/user293/Documents/selections/python/Outputs/ToyPlots/Models100Velo50.csv"
df = pd.read_csv(csv_file)

# Extract values
significances = df["Significance"].values
significance_errors = df["Significance_Error"].values

# Compute statistics
ninefive_percentile = np.percentile(significances, 5)
percent_above_3 = np.mean(significances > 3) * 100
percent_above_5 = np.mean(significances > 5) * 100

# Define histogram
num_bins = 30
hist = TH1D("Legend", "Control Mode Significance Distribution", num_bins,
            min(significances, default=0), max(significances, default=10))
energy_range = (max(significances, default=10) - min(significances, default=0)) / num_bins

# Fill histogram
for significance in significances:
    hist.Fill(significance)

# Draw histogram
canvas = TCanvas("canvas", "Significance Histogram", 800, 600)
hist.GetXaxis().SetTitle("Significance")
hist.GetYaxis().SetTitle(f"Entries / Bin (Bin Size = {energy_range:.2f})")
hist.SetStats(False)

# Vertical lines
line_secondpercentile = TLine(ninefive_percentile, 0, ninefive_percentile, hist.GetMaximum())
line_signif3 = TLine(3, 0, 3, hist.GetMaximum())
line_signif5 = TLine(5, 0, 5, hist.GetMaximum())

line_secondpercentile.SetLineColor(ROOT.kRed)
line_signif3.SetLineColor(ROOT.kGreen)
line_signif5.SetLineColor(ROOT.kMagenta)

line_secondpercentile.SetLineStyle(2)
line_signif3.SetLineStyle(2)
line_signif5.SetLineStyle(2)

line_secondpercentile.SetLineWidth(2)
line_signif3.SetLineWidth(2)
line_signif5.SetLineWidth(2)

# Legend
legend = TLegend(0.66, 0.7, 0.97, 0.9)
legend.SetLineColor(0)
legend.SetLineStyle(0)
legend.SetLineWidth(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetFillStyle(0)
legend.SetTextFont(62)
legend.SetTextSize(0.04)
legend.AddEntry(hist, "Toy Models", "l")
legend.AddEntry(line_secondpercentile, "95% CI", "l")
if np.min(significances) < 5:
    legend.AddEntry(line_signif5, "Observation", "l")
    if np.min(significances) < 3:
        legend.AddEntry(line_signif3, "Evidence", "l")

# Draw elements
hist.Draw("HIST")
line_secondpercentile.Draw()
line_signif3.Draw()
line_signif5.Draw()
legend.Draw()
canvas.SaveAs("/home/user293/Documents/selections/python/Outputs/ToyPlots/Models100Velo50.pdf")
