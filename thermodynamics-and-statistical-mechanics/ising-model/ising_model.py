"""
2‑D Ising model (square lattice) with the Metropolis Monte‑Carlo algorithm.
Plots magnetisation per spin as the system evolves at a chosen temperature.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------- simulation parameters ----------------
L         = 40          # lattice size  (L×L spins)
T         = 2.2         # temperature (k_B = 1 units)
J         = 1.0         # coupling constant (>0 ferromagnetic)
steps     = 60000       # total Monte‑Carlo steps
thermal   = 10000       # steps discarded as thermalisation
measure_every = 100     # record magnetisation every n steps
seed      = 1
# -------------------------------------------------------

rng = np.random.default_rng(seed)
spins = rng.choice([-1, 1], size=(L, L))           # initialise randomly

def energy_change(i, j):
    """ΔE if spin (i,j) is flipped, PBC assumed."""
    s  = spins[i, j]
    # 4 nearest neighbours with periodic BC
    nn = spins[(i+1)%L, j] + spins[(i-1)%L, j] + spins[i,(j+1)%L] + spins[i,(j-1)%L]
    return 2 * J * s * nn

beta = 1.0 / T
magnetisation = []

for step in range(steps):
    # pick random lattice site
    i = rng.integers(L)
    j = rng.integers(L)
    dE = energy_change(i, j)
    # Metropolis accept/reject
    if dE <= 0 or rng.random() < np.exp(-beta * dE):
        spins[i, j] *= -1

    # record after thermalisation
    if step >= thermal and step % measure_every == 0:
        m = np.abs(spins.sum()) / (L*L)           # |M| per spin
        magnetisation.append(m)

# plot magnetisation versus MC sample
plt.figure(figsize=(7,4))
plt.plot(np.arange(len(magnetisation)), magnetisation, '.', ms=2)
plt.xlabel("Recorded sample")
plt.ylabel("Magnetisation |M| per spin")
plt.title(f"2‑D Ising Model  –  L={L},  T={T}")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
