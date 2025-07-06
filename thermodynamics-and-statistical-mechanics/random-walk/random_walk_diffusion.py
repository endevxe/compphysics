"""
2‑D lattice random walk (Brownian motion).
Computes mean‑square displacement ⟨r²⟩(t) and estimates the diffusion coefficient D
via a linear fit:  ⟨r²⟩ = 4 D t  in two dimensions.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------- simulation parameters ----------------
N_walkers = 5000          # number of independent walkers
N_steps   = 5000          # steps per walker
step_len  = 1.0           # lattice spacing
seed      = 42
# -------------------------------------------------------

rng = np.random.default_rng(seed)

# Each step: random choice among (±1,0) or (0,±1)
choices = np.array([[1,0], [-1,0], [0,1], [0,-1]])

# positions for all walkers
pos = np.zeros((N_walkers, 2))
msd = np.zeros(N_steps+1)   # mean‑square displacement vs time
msd[0] = 0.0

for t in range(1, N_steps+1):
    steps = choices[rng.integers(4, size=N_walkers)] * step_len
    pos += steps
    msd[t] = (pos[:,0]**2 + pos[:,1]**2).mean()

# Estimate diffusion coefficient: ⟨r²⟩ = 4 D t  →  D = slope/4
coeffs = np.polyfit(np.arange(N_steps+1), msd, 1)   # linear fit
slope  = coeffs[0]
D_est  = slope / 4.0

# ------------- plots -------------
plt.figure(figsize=(7,5))
plt.plot(msd, label=r'$\langle r^{2}(t)\rangle$ (simulation)')
plt.plot(np.arange(N_steps+1), slope*np.arange(N_steps+1)+coeffs[1],
         '--', label=f'Linear fit,  D ≈ {D_est:.3f}')
plt.xlabel('Step number  $t$')
plt.ylabel(r'Mean‑square displacement  $\langle r^{2}\rangle$')
plt.title('2‑D Random Walk  –  Diffusion Coefficient')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
