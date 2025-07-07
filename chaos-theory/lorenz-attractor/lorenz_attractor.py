#!/usr/bin/env python3
"""
Lorenz Attractor – deterministic chaos in three dimensions.
Integrates the Lorenz system and plots the 3‑D trajectory.
"""
import numpy as np
import matplotlib.pyplot as plt

# Lorenz parameters
SIGMA = 10.0
RHO   = 28.0
BETA  = 8.0 / 3.0

# Integration settings
DT     = 0.01
STEPS  = 10000

# Initial condition
x, y, z = (0.0, 1.0, 1.05)
trajectory = np.empty((STEPS, 3))

def lorenz(x, y, z):
    """Return time derivatives dx/dt, dy/dt, dz/dt."""
    dx = SIGMA * (y - x)
    dy = x * (RHO - z) - y
    dz = x * y - BETA * z
    return dx, dy, dz

# Integrate using RK4
for i in range(STEPS):
    trajectory[i] = (x, y, z)
    dx1, dy1, dz1 = lorenz(x, y, z)
    dx2, dy2, dz2 = lorenz(x + 0.5*DT*dx1, y + 0.5*DT*dy1, z + 0.5*DT*dz1)
    dx3, dy3, dz3 = lorenz(x + 0.5*DT*dx2, y + 0.5*DT*dy2, z + 0.5*DT*dz2)
    dx4, dy4, dz4 = lorenz(x + DT*dx3, y + DT*dy3, z + DT*dz3)
    x += DT/6 * (dx1 + 2*dx2 + 2*dx3 + dx4)
    y += DT/6 * (dy1 + 2*dy2 + 2*dy3 + dy4)
    z += DT/6 * (dz1 + 2*dz2 + 2*dz3 + dz4)

# Plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], lw=0.5, color='#6a0dad')
ax.set_title('Lorenz Attractor')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.tight_layout()
plt.show()
