import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
g = 9.81     # gravity
L1 = L2 = 1  # lengths
m1 = m2 = 1  # masses

# Initial conditions: [theta1, omega1, theta2, omega2]
state = np.radians([120, 0, -10, 0])
dt = 0.04
t_max = 20
frames = int(t_max / dt)

def derivatives(y):
    θ1, ω1, θ2, ω2 = y
    Δ = θ2 - θ1

    den1 = (m1 + m2) - m2 * np.cos(Δ)**2
    den2 = den1  # same denominator

    a1 = (m2 * g * np.sin(θ2) * np.cos(Δ) -
          m2 * np.sin(Δ) * (L1 * ω1**2 * np.cos(Δ) + L2 * ω2**2) -
          (m1 + m2) * g * np.sin(θ1)) / (L1 * den1)

    a2 = ((m1 + m2) * (L1 * ω1**2 * np.sin(Δ) -
          g * np.sin(θ2) + g * np.sin(θ1) * np.cos(Δ)) +
          m2 * L2 * ω2**2 * np.sin(Δ) * np.cos(Δ)) / (L2 * den2)

    return np.array([ω1, a1, ω2, a2])

# Runge–Kutta 4 integrator
def rk4_step(f, y, dt):
    k1 = f(y)
    k2 = f(y + dt/2 * k1)
    k3 = f(y + dt/2 * k2)
    k4 = f(y + dt * k3)
    return y + dt/6 * (k1 + 2*k2 + 2*k3 + k4)

# Integrate
trajectory = []
y = state.copy()
for _ in range(frames):
    trajectory.append(y.copy())
    y = rk4_step(derivatives, y, dt)
trajectory = np.array(trajectory)

# Convert to (x, y) positions
x1 = L1 * np.sin(trajectory[:,0])
y1 = -L1 * np.cos(trajectory[:,0])
x2 = x1 + L2 * np.sin(trajectory[:,2])
y2 = y1 - L2 * np.cos(trajectory[:,2])

# Animate
fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
line, = ax.plot([], [], 'o-', lw=2)
trace, = ax.plot([], [], 'r-', lw=0.5, alpha=0.6)
trail_x, trail_y = [], []

def update(i):
    line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])
    trail_x.append(x2[i])
    trail_y.append(y2[i])
    trace.set_data(trail_x, trail_y)
    return line, trace

ani = FuncAnimation(fig, update, frames=frames, interval=40, blit=True)
plt.title("Double Pendulum Simulation")
plt.tight_layout()
plt.show()
