import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import numpy as np

#particle = "Xi"
particle = "Lambdac"

# Load the CSV file
file = f"/home/user293/Documents/selections/python/Outputs/TrackSelection/OriginalROCPlots/{particle}IPALL.csv"
df = pd.read_csv(file)

# Extract columns
MinPT = df["MinPT"]
MinP = df["MinP"]
MinIPChi2 = df["MinIPChi2"]

if particle == "Lambdac":
    efficiency = df["efficiency"] = df["#XiLambdas"]/504
    purity = df["purity"] = (df["#XiLambdas"]) / (df["#LambdaCandidates"])
else:
    efficiency = df["efficiency"] = df["#XiPions"] * df["#XiKaons"]
    purity = df["purity"] = (df["#XiPions"] * 973 + df["#XiKaons"] * 493) / (df["#Pion"] + df["#Kaon"])

df["efficiency_purity"] = np.sqrt(df["efficiency"]**2 + df["purity"]**2)
max_row = df.loc[df["efficiency_purity"].idxmax()]

# Extract the corresponding values
max_eff_purity = max_row["efficiency_purity"]
optimal_MinPT = max_row["MinPT"]
optimal_MinP = max_row["MinP"]
optimal_MinIPChi2 = max_row["MinIPChi2"]

optimal_efficiency = max_row["efficiency"]
optimal_purity = max_row["purity"]

print(f"MinPT = {optimal_MinPT} \nMinP = {optimal_MinP} \nMinIpChi2 = {optimal_MinIPChi2}")
print(f"Efficiency = {optimal_efficiency} \nPurity = {optimal_purity}")


# Normalise MinPT, MinP, and MinIPChi2 for RGB mapping
norm_MinPT = (MinPT - MinPT.min()) / (MinPT.max() - MinPT.min())
norm_MinP = (MinP - MinP.min()) / (MinP.max() - MinP.min())
norm_MinIPChi2 = (MinIPChi2 - MinIPChi2.min()) / (MinIPChi2.max() - MinIPChi2.min())

# Create RGB colours
colours = list(zip(norm_MinPT, norm_MinP, norm_MinIPChi2))

# Plot efficiency vs purity
plt.figure(figsize=(10, 7))
scatter = plt.scatter(purity, efficiency)

# Add labels and title
plt.xlabel("Purity")
plt.ylabel("Efficiency")
plt.title("Efficiency vs Purity with RGB Colour Mapping")
plt.grid(alpha=0.3)


# Add colour bars
fig, ax = plt.gcf(), plt.gca()
ax.set_xscale('log')
sm_r = ScalarMappable(Normalize(MinPT.min(), MinPT.max()), cmap="Reds")
sm_g = ScalarMappable(Normalize(MinP.min(), MinP.max()), cmap="Greens")
sm_b = ScalarMappable(Normalize(MinIPChi2.min(), MinIPChi2.max()), cmap="Blues")

# Create a separate axis for each colour bar
cbar_r = fig.colorbar(sm_r, ax=ax, fraction=0.02, pad=0.04, location='right')
cbar_r.set_label("MinPT (Red)", color="red")
cbar_g = fig.colorbar(sm_g, ax=ax, fraction=0.02, pad=0.10, location='right')
cbar_g.set_label("MinP (Green)", color="green")
cbar_b = fig.colorbar(sm_b, ax=ax, fraction=0.02, pad=0.16, location='right')
cbar_b.set_label("MinIPChi2 (Blue)", color="blue")

# Save the plot as a PNG file
output_file = f"/home/user293/Documents/selections/python/Outputs/TrackSelection/{particle}EvsP.png"
plt.savefig(output_file, dpi=300)  # Save with 300 DPI for high quality
plt.close()  # Close the plot to free up memory

print(f"Plot saved to {output_file}")
