import ROOT
import numpy as np
import pandas as pd
import ROOT
latex = ROOT.TLatex()

# File path for the CSV containing significance values
csv_file = "/home/user293/Documents/selections/python/Outputs/ToyPlots/SigModels1000Velo50R0.5.csv"

# Load CSV data
df = pd.read_csv(csv_file)

# Extract significance values
significances = df["Significance"].to_numpy()

# Define histogram parameters
num_bins = 30
hist_min = min(significances, default=0)
hist_max = max(significances, default=10)
bin_width = (hist_max - hist_min) / num_bins

# Create ROOT histogram
hist = ROOT.TH1D("Legend", "", num_bins, hist_min, hist_max)
hist.SetStats(False)  # Disable stats box

# Fill histogram
for significance in significances:
    hist.Fill(significance)

# Compute confidence levels
ninefive_percentile = np.percentile(significances, 5) if len(significances) > 0 else 10
print(ninefive_percentile)

# Create canvas
canvas = ROOT.TCanvas("canvas", "Significance Histogram", 800, 600)

# Set histogram axis labels and formatting
hist.GetXaxis().SetTitle("Significance")
hist.GetYaxis().SetTitle(f"Entries / Bin (Bin Size = {bin_width:.2f})")
hist.GetXaxis().SetTitleSize(0.04)
hist.GetYaxis().SetTitleSize(0.04)
hist.GetXaxis().SetLabelSize(0.04)
hist.GetYaxis().SetLabelSize(0.04)
hist.GetXaxis().SetTitleOffset(1)
hist.GetYaxis().SetTitleOffset(1)
hist.GetXaxis().SetLabelFont(62)
hist.GetYaxis().SetLabelFont(62)
hist.GetXaxis().SetTitleFont(62)
hist.GetYaxis().SetTitleFont(62)

# Add vertical lines for confidence levels
line_ninefive = ROOT.TLine(ninefive_percentile, 0, ninefive_percentile, hist.GetMaximum())
line_ninefive.SetLineColor(ROOT.kRed)
line_ninefive.SetLineStyle(2)  # Dashed line
line_ninefive.SetLineWidth(2)

line_signif5 = ROOT.TLine(5, 0, 5, hist.GetMaximum())
line_signif3 = ROOT.TLine(3, 0, 3, hist.GetMaximum())
line_signif3.SetLineColor(ROOT.kGreen)
line_signif5.SetLineColor(ROOT.kMagenta)
line_signif5.SetLineStyle(2)
line_signif3.SetLineStyle(2)
line_signif5.SetLineWidth(2)
line_signif3.SetLineWidth(2)

# Create legend
legend = ROOT.TLegend(0.62, 0.78, 0.89, 0.87)
legend.SetLineColor(0)
legend.SetFillColor(0)
legend.SetTextFont(62)
legend.SetTextSize(0.04)
legend.AddEntry(hist, "Toy Models", "l")
legend.AddEntry(line_ninefive, "95% CI", "l")

latex.SetNDC()
latex.SetTextSize(0.050)
latex.SetTextFont(62)
latex.DrawText(0.8, 0.85, "LHCb Simulation")
latex.DrawLatex(0.8, 0.80, "#sqrt{s} = 14 TeV")
latex.DrawLatex(0.8, 0.745, f"R = 0.5")
latex.DrawLatex(0.8, 0.695, f"VELO Time = 50 ps")

if hist_min < 5:
    legend.AddEntry(line_signif5, "Observation", "l")
    if hist_min < 3:
        legend.AddEntry(line_signif3, "Evidence", "l")

# Draw histogram and lines
hist.Draw("HIST")
line_ninefive.Draw()
#line_signif5.Draw()
line_signif3.Draw()
legend.Draw()

# Save as PDF
output_path = "/home/user293/Documents/selections/python/Outputs/ToyPlots/Models1000Velo50R0.5.pdf"
canvas.cd()
canvas.Update()
canvas.SaveAs(output_path)
print(f"Histogram saved to: {output_path}")
