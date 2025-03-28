import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import pearsonr

# Data
velo = np.array([30, 50, 70, 100])
R_limit = np.array([0.5954, 0.6117, 0.6092, 0.6372])
errors = np.array([0.02983, 0.03071, 0.03063, 0.03216])

# Define a linear function
def linear(x, a, b):
    return a * x + b

# Perform linear fit
popt, pcov = curve_fit(linear, velo, R_limit, sigma=errors)

# Calculate R-squared value
residuals = R_limit - linear(velo, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((R_limit - np.mean(R_limit))**2)
r_squared = 1 - (ss_res / ss_tot)

# Compute Pearson correlation coefficient and p-value
pearson_coeff, p_value = pearsonr(velo, R_limit)

# Plot
plt.errorbar(velo, R_limit, yerr=errors, fmt='o', label='Data', capsize=5)
plt.plot(velo, linear(velo, *popt), 'r-', label=f'Fit: R² = {r_squared:.3f}')
plt.text(min(velo), max(R_limit), f'Pearson r = {pearson_coeff:.3f}\nP-value = {p_value:.3f}', fontsize=12, verticalalignment='top')
plt.xlabel('Velo')
plt.ylabel('Run 5 R Limit')
plt.title('Linear Fit of Run 5 R Limit vs. Velo')
plt.legend()
plt.grid()
plt.show()

# Print fit parameters
print(f"Fit parameters: a = {popt[0]:.5f}, b = {popt[1]:.5f}")
print(f"R-squared: {r_squared:.3f}")
print(f"Pearson correlation coefficient: {pearson_coeff:.3f}")
print(f"P-value: {p_value:.3f}")