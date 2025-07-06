"""
Mass–spring–damper system.
Compares analytic solution (underdamped) with RK4 numerical integration.
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
m   = 1.0      # kg
k   = 20.0     # N/m  (spring constant)
c   = 2.0      # N·s/m (damping coefficient)
x0  = 1.0      # initial displacement (m)
v0  = 0.0      # initial velocity (m/s)
t_end = 10.0
dt    = 0.001

# Derived quantities
omega_n = np.sqrt(k / m)
zeta    = c / (2 * np.sqrt(k * m))      # damping ratio

# Analytic solution (underdamped only: zeta < 1)
def analytic(t):
    omega_d = omega_n * np.sqrt(1 - zeta**2)
    A = x0
    B = (v0 + zeta*omega_n*x0) / omega_d
    return np.exp(-zeta*omega_n*t) * (A*np.cos(omega_d*t) + B*np.sin(omega_d*t))

# RK4 system
def derivatives(state):
    x, v = state
    a = -(c/m)*v - (k/m)*x
    return np.array([v, a])

def rk4_step(f, y, dt):
    k1 = f(y)
    k2 = f(y + 0.5*dt*k1)
    k3 = f(y + 0.5*dt*k2)
    k4 = f(y + dt*k3)
    return y + dt/6 * (k1 + 2*k2 + 2*k3 + k4)

# Integrate
times = np.arange(0, t_end+dt, dt)
x_num = []
state = np.array([x0, v0])
for _ in times:
    x_num.append(state[0])
    state = rk4_step(derivatives, state, dt)
x_num = np.array(x_num)

# Analytic
x_an  = analytic(times)

# Plot
plt.figure(figsize=(8,5))
plt.plot(times, x_an,  '--', label='Analytic (underdamped)')
plt.plot(times, x_num, '-',  label='RK4 numerical')
plt.xlabel("Time (s)")
plt.ylabel("Displacement x (m)")
plt.title("Mass–Spring–Damper Response  (ζ = {:.2f})".format(zeta))
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
