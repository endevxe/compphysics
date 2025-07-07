"""
Electric field lines from multiple point charges (2‑D)
Uses streamplot to visualise the field.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------- configure charges ----------
charges = [
    (+1.0, -1.0, 0.0),  # (q, x0, y0)
    (-1.0, +1.0, 0.0)
]
k = 1        # Coulomb constant (scaled)
# ---------------------------------------

# grid
nx, ny = 500, 500
x = np.linspace(-3, 3, nx)
y = np.linspace(-3, 3, ny)
X, Y = np.meshgrid(x, y)

Ex, Ey = np.zeros_like(X), np.zeros_like(Y)

for q, x0, y0 in charges:
    dx = X - x0
    dy = Y - y0
    r2 = dx**2 + dy**2
    Ex += k * q * dx / r2**1.5
    Ey += k * q * dy / r2**1.5

# field magnitude for colour
E = np.sqrt(Ex**2 + Ey**2)

plt.figure(figsize=(6,6))
plt.streamplot(X, Y, Ex, Ey, color=np.log(E), cmap='inferno', density=2)
plt.scatter([c[1] for c in charges], [c[2] for c in charges],
            c=['royalblue' if c[0]>0 else 'white' for c in charges],
            s=100, edgecolors='k')
plt.title('Electric Field Lines')
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.tight_layout()
plt.show()
