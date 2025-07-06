"""
Central Force Motion
Simulates 2D motion under an inverse-square force (gravity-like) using RK4.
"""

import numpy as np
import matplotlib.pyplot as plt

# Gravitational constant (scaled)
G = 1.0
M = 1.0  # central mass
m = 0.001  # test mass

# Time settings
dt = 0.001
steps = 20000

# Initial conditions (adjust for elliptic vs hyperbolic)
r0 = np.array([1.0, 0.0])           # initial position
v0 = np.array([0.0, 1.2])           # initial velocity (try 1.0 for circular orbit)

# State: [x, y, vx, vy]
state = np.hstack((r0, v0))
trajectory = []

def acceleration(r):
    """Inverse-square law acceleration: -GM r / |r|^3"""
    norm = np.linalg.norm(r) + 1e-5
    return -G * M * r / norm**3

def rk4_step(state):
    x, y, vx, vy = state
    r = np.array([x, y])
    v = np.array([vx, vy])
    
    def deriv(s):
        r = s[:2]
        v = s[2:]
        a = acceleration(r)
        return np.hstack((v, a))

    k1 = deriv(state)
    k2 = deriv(state + 0.5*dt*k1)
    k3 = deriv(state + 0.5*dt*k2)
    k4 = deriv(state + dt*k3)
    
    return state + dt/6 * (k1 + 2*k2 + 2*k3 + k4)

# Simulate
for _ in range(steps):
    trajectory.append(state[:2])
    state = rk4_step(state)

trajectory = np.array(trajectory)

# Plot
plt.figure(figsize=(6,6))
plt.plot(trajectory[:,0], trajectory[:,1], label='Orbit path')
plt.plot(0, 0, 'yo', markersize=10, label='Central Mass')
plt.axis('equal')
plt.grid(True)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Central Force Motion')
plt.legend()
plt.tight_layout()
plt.show()
