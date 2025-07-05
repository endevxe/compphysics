#!/usr/bin/env python3
"""
Infinite‑square‑well eigenstates (1‑D)

Dependencies:
    numpy, matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt

# --------------------- parameters ---------------------
hbar = 1.0          # Planck constant / 2π  (set =1 for convenience)
m    = 1.0          # particle mass        (set =1)
L    = 1.0          # well width
N    = 500          # interior grid points (larger → better accuracy)
nev  = 4            # number of eigenstates to plot
# ------------------------------------------------------

dx = L / (N + 1)                            # grid spacing
x  = np.linspace(dx, L - dx, N)             # interior points (exclude walls)

# Finite‑difference 2nd derivative  (−ħ²/2m) d²/dx²
coeff = -(hbar**2) / (2 * m * dx**2)
diag  = np.full(N,   -2.0)                  # main diagonal
off   = np.full(N-1,  1.0)                  # off diagonals

H = coeff * (                                # kinetic term
        np.diag(diag) +
        np.diag(off,  k=1) +
        np.diag(off,  k=-1)
    )
# potential term is zero inside the well → no change to H

# diagonalise (eigenvalues sorted ascending)
E, psi = np.linalg.eigh(H)

# normalise eigenfunctions (columns of psi)
psi /= np.sqrt(dx)                # grid‑norm → ∑|ψ|² dx = 1

# ------------------------- plots -------------------------
plt.figure(figsize=(8, 5))

for n in range(nev):
    plt.plot(x, psi[:, n], label=fr"$n={n+1},\;E={E[n]:.3f}$")

plt.title("Infinite Square Well – First Few Eigenfunctions")
plt.xlabel("x")
plt.ylabel(r"$\psi_n(x)$")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
