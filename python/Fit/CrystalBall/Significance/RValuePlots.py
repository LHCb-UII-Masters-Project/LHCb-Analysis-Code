import matplotlib.pyplot as plt
import numpy as np

# Data
velo_settings = [30, 50, 70, 100, 200]
r_limits = [0.09672, 0.09937, 0.0987, 0.1035, 0.1031]
r_errors = [0.004302, 0.004428, 0.00426, 0.004639, 0.004686]

# Custom x-axis labels for Plot 1
x_labels = [f"{ps}ps" for ps in velo_settings]
x_positions = np.arange(len(velo_settings))  # Evenly spaced positions

# Plot 1: VELO settings vs R Limit with Theory Value line
plt.figure(figsize=(10, 6))
plt.errorbar(x_positions, r_limits, yerr=r_errors, fmt='o', label='Run 5 R Limit', color='blue', capsize=5, markersize=10)  # Increased marker size
plt.axhline(y=0.2, color='red', linestyle='--', label='Theory Predicted R Value')
plt.xticks(x_positions, x_labels, ha='right', fontsize=20, fontweight='bold')  # Larger and bold x-axis labels
plt.yticks(fontsize=20, fontweight='bold')  # Larger and bold y-axis labels
plt.xlabel('VELO Setting', fontsize=20, fontweight='bold')  # Larger and bold x-axis title
plt.ylabel('R Limit', fontsize=20, fontweight='bold')  # Larger and bold y-axis title
plt.title('Run 5 R Limit for Different VELO Settings', fontsize=22, fontweight='bold')  # Larger and bold title
plt.legend(fontsize=28, prop={'weight': 'bold'})  # Larger and bold legend text
plt.grid(True)
plt.tight_layout()  # Adjust layout to prevent label overlap
plt.savefig('/home/user293/Documents/selections/python/Fit/CrystalBall/Significance/plot1_run5_r_limit.png')  # Save as PNG
plt.close()

# Plot 2: R = 0.2 as a data point and R = 1 as a line
plt.figure(figsize=(10, 6))
plt.scatter(0, 0.2, color='green', label='Theory Value (R = 0.2)', zorder=5, s=150)  # Increased marker size
plt.axhline(y=1, color='orange', linestyle='-', label='Run 2 R Limit (R = 1)')
plt.xlim(-0.5, 0.5)  # Adjust x-axis limits to center the point
plt.ylim(0, 1.2)
plt.xticks([0], ['Run 2 R Limit'], ha='right', fontsize=20, fontweight='bold')  # Larger and bold x-axis label
plt.yticks(fontsize=20, fontweight='bold')  # Larger and bold y-axis labels
plt.xlabel('', fontsize=20, fontweight='bold')  # Larger and bold x-axis title (empty in this case)
plt.ylabel('R Limit', fontsize=20, fontweight='bold')  # Larger and bold y-axis title
plt.title('Comparison of Theory Value and Run 2 R Limit', fontsize=22, fontweight='bold')  # Larger and bold title
plt.legend(fontsize=28, prop={'weight': 'bold'})  # Larger and bold legend text
plt.grid(True)
plt.tight_layout()  # Adjust layout
plt.savefig('/home/user293/Documents/selections/python/Fit/CrystalBall/Significance/plot2_theory_vs_run2_limit.png')  # Save as PNG
plt.close()