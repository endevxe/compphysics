"""Quantum tunnelling through a finite potential barrier (1‑D).
Computes transmission coefficient T(E) analytically for a rectangular
barrier of height V0 and width a, using natural units (ħ = m = 1)."""
import numpy as np
import matplotlib.pyplot as plt

V0 = 1.0   # barrier height (energy units)
a  = 1.0   # barrier width (length units)

E = np.linspace(0.01, 2.0, 800)  # energy range
T = np.zeros_like(E)

for i, energy in enumerate(E):
    if energy < V0:  # under‑barrier tunnelling
        kappa = np.sqrt(2*(V0 - energy))
        numerator = V0**2 * np.sinh(kappa * a)**2
        denom = 4 * energy * (V0 - energy)
        T[i] = 1 / (1 + numerator / denom)
    else:  # over‑barrier (partial reflection)
        k2 = np.sqrt(2*(energy - V0))
        numerator = V0**2 * np.sin(k2 * a)**2
        denom = 4 * energy * (energy - V0)
        T[i] = 1 / (1 + numerator / denom)

plt.figure(figsize=(8,5))
plt.plot(E, T, color='#6a0dad')
plt.axvline(V0, color='gray', ls='--', label=f'V0 = {V0}')
plt.title('Transmission Coefficient vs Energy')
plt.xlabel('Energy E')
plt.ylabel('Transmission T(E)')
plt.ylim(0,1.05)
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
