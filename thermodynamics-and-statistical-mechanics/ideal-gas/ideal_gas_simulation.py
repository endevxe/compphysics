"""
2D Ideal Gas Simulation:
Particles move freely in a box and undergo elastic collisions with walls.
Plots the evolving velocity histogram vs. Maxwell–Boltzmann distribution.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Parameters ---
N = 100            # number of particles
L = 10.0           # box size
v_max = 3.0        # initial speed range
dt = 0.01
steps = 1000
mass = 1.0

# Random initial positions and velocities
np.random.seed(0)
pos = np.random.rand(N, 2) * L
vel = (np.random.rand(N, 2) - 0.5) * 2 * v_max

# Set up plotting
fig, (ax_box, ax_hist) = plt.subplots(1, 2, figsize=(10, 5))
scat = ax_box.scatter(pos[:, 0], pos[:, 1], s=10)
ax_box.set_xlim(0, L)
ax_box.set_ylim(0, L)
ax_box.set_title("Particles in a Box")
ax_box.set_aspect('equal')

hist_data, = ax_hist.plot([], [], lw=2, label='Velocity Histogram')
mb_line, = ax_hist.plot([], [], '--', lw=2, label='Maxwell–Boltzmann')

ax_hist.set_xlim(0, v_max)
ax_hist.set_ylim(0, N / 2)
ax_hist.set_xlabel("Speed")
ax_hist.set_ylabel("Counts")
ax_hist.set_title("Velocity Distribution")
ax_hist.legend()

def update(frame):
    global pos, vel

    pos += vel * dt

    # Elastic wall collisions
    for i in range(N):
        for dim in range(2):
            if pos[i, dim] < 0 or pos[i, dim] > L:
                vel[i, dim] *= -1

    scat.set_offsets(pos)

    speeds = np.linalg.norm(vel, axis=1)
    counts, bins = np.histogram(speeds, bins=30, range=(0, v_max))
    hist_data.set_data((bins[:-1] + bins[1:]) / 2, counts)

    # Maxwell–Boltzmann theoretical line
    T = np.mean(speeds**2) * mass / 2
    x = np.linspace(0, v_max, 200)
    mb = (mass / T) * x * np.exp(-mass * x**2 / (2 * T))
    mb *= N / np.sum(mb) * 2  # scale to match histogram
    mb_line.set_data(x, mb)

    return scat, hist_data, mb_line

ani = FuncAnimation(fig, update, frames=steps, interval=30, blit=True)
plt.tight_layout()
plt.show()
