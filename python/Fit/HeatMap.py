import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from os import path, listdir 
from matplotlib.backends.backend_pdf import PdfPages

# mode = "Efficacy"
mode = "SNR"

args = sys.argv
file = args[1]

basedir=f"{file}/.."
sys.path.insert(0,basedir)

# Load the CSV file
csv_file = file  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)

# Extract relevant columns (adjust index for zero-based indexing)
x = df.iloc[:, 1]  # Column 2 (index 1)
y = df.iloc[:, 2]  # Column 3 (index 2)
if mode == "SNR":
    heat = (df.iloc[:, 5] * 504) / df.iloc[:, [9, 10, 11]].min(axis=1)
elif mode == "Efficacy":
    heat = (df.iloc[:,5])

# Combine columns into a new DataFrame
heatmap_data = pd.DataFrame({'x': x, 'y': y, 'heat': heat})

# Pivot the data for heatmap
heatmap_pivot = heatmap_data.pivot_table(index='y', columns='x', values='heat', aggfunc=np.mean)

# Plot the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(heatmap_pivot, cmap='viridis', annot=False, cbar=True)
plt.title(f"{file[-7:-4]}{mode} Heat Map")
plt.xlabel("Transverse Momentum (MeV/c)")
plt.ylabel("Total Momentum (MeV/c)")

output_pdf = f"{file[:-18]}{mode}HeatMap{file[-7:-4]}.pdf"  # Replace with your desired output filename
with PdfPages(output_pdf) as pdf:
    pdf.savefig()  # Save the current figure
    plt.close()  # Close the figure to avoid displaying it
