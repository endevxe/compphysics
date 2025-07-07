"""
Logistic Map Simulation
Explores bifurcations and chaotic behavior for different values of r.
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
r_values = np.linspace(2.4, 4.0, 800)  # Range of r values
iterations = 1000                      # Total iterations
last = 100                             # Plot only the last N values per r

x0 = 0.5  # Initial value of x

fig, ax = plt.subplots(figsize=(10, 6))

for r in r_values:
    x = x0
    results = []
    for i in range(iterations):
        x = r * x * (1 - x)
        if i >= (iterations - last):
            results.append((r, x))

    rs, xs = zip(*results)
    ax.plot(rs, xs, ',k', alpha=0.25)  # small black dots

ax.set_title("Logistic Map Bifurcation Diagram")
ax.set_xlabel("r")
ax.set_ylabel("x")
plt.grid(alpha=0.2)
plt.tight_layout()
plt.show()
