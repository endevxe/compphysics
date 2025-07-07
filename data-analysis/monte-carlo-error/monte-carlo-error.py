"""
Monte Carlo Error Propagation
Example: Compute area of a rectangle A = L * W
Given uncertainties in L and W, simulate error propagation by sampling.
"""
import numpy as np
import matplotlib.pyplot as plt

# Known values and their uncertainties (1 sigma)
L_mean, L_std = 10.0, 0.5  # length in cm
W_mean, W_std = 4.0, 0.2   # width in cm

# Number of Monte Carlo trials
N = 10000

# Sample from normal distributions
L_samples = np.random.normal(L_mean, L_std, N)
W_samples = np.random.normal(W_mean, W_std, N)

# Compute derived quantity: area = L * W
A_samples = L_samples * W_samples

# Statistics of area
A_mean = np.mean(A_samples)
A_std = np.std(A_samples)

# Print results
print(f"Estimated Area: {A_mean:.2f} ± {A_std:.2f} cm²")

# Plot histogram
plt.hist(A_samples, bins=50, color="#6a0dad", edgecolor="black", alpha=0.7)
plt.title("Monte Carlo Simulation of Area")
plt.xlabel("Area (cm²)")
plt.ylabel("Frequency")
plt.grid(alpha=0.3)
plt.show()
