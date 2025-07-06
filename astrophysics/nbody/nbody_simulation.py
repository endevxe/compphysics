"""
N-body gravitational simulation using RK4.
Simulates simplified solar system dynamics.
"""

import numpy as np
import matplotlib.pyplot as plt

# ------------------- Parameters -------------------
G = 1.0  # Gravitational constant in AU^3 / (yr^2 * solar_mass)
dt = 0.001
steps = 20000

# [mass, x, y, vx, vy]
bodies = [
    [1.0,   0.0, 0.0,    0.0,  0.0],      # Sun
    [0.001, 1.0, 0.0,    0.0, 6.28],      # Earth-like orbit
    [0.0001,1.5, 0.0,    0.0, 5.1]        # Small asteroid
]
# ---------------------------------------------------

def acceleration(bodies):
    """Compute acceleration on each body due to gravity from others."""
    n = len(bodies)
    acc = np.zeros((n, 2))
    for i in range(n):
        mi, xi, yi = bodies[i][0], bodies[i][1], bodies[i][2]
        for j in range(n):
            if i == j: continue
            mj, xj, yj = bodies[j][0], bodies[j][1], bodies[j][2]
            dx, dy = xj - xi, yj - yi
            r = np.hypot(dx, dy) + 1e-5
            a = G * mj / r**3
            acc[i][0] += a * dx
            acc[i][1] += a * dy
    return acc

def rk4_step(bodies):
    """Advance positions and velocities using RK4."""
    n = len(bodies)
    pos = np.array([[b[1], b[2]] for b in bodies])
    vel = np.array([[b[3], b[4]] for b in bodies])
    mass = [b[0] for b in bodies]

    def get_acc(pos_):
        temp = [[mass[i], pos_[i][0], pos_[i][1], 0, 0] for i in range(n)]
        return acceleration(temp)

    k1v = get_acc(pos)
    k1x = vel

    k2v = get_acc(pos + 0.5 * dt * k1x)
    k2x = vel + 0.5 * dt * k1v

    k3v = get_acc(pos + 0.5 * dt * k2x)
    k3x = vel + 0.5 * dt * k2v

    k4v = get_acc(pos + dt * k3x)
    k4x = vel + dt * k3v

    new_pos = pos + dt/6 * (k1x + 2*k2x + 2*k3x + k4x)
    new_vel = vel + dt/6 * (k1v + 2*k2v + 2*k3v + k4v)

    for i in range(n):
        bodies[i][1], bodies[i][2] = new_pos[i]
        bodies[i][3], bodies[i][4] = new_vel[i]

    return bodies

# Run simulation and collect trajectories
n = len(bodies)
trajectories = [[] for _ in range(n)]

for _ in range(steps):
    for i in range(n):
        trajectories[i].append((bodies[i][1], bodies[i][2]))
    rk4_step(bodies)

# Plot
plt.figure(figsize=(8, 6))
for i, traj in enumerate(trajectories):
    x, y = zip(*traj)
    plt.plot(x, y, label=f'Body {i+1}')
plt.gca().set_aspect('equal')
plt.title('N-Body Gravitational Simulation')
plt.xlabel('x (AU)')
plt.ylabel('y (AU)')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
