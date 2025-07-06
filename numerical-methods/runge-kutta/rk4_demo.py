"""
Fourth‑order Runge–Kutta demonstration on dy/dt = -y
Compares numerical and exact solutions and shows error scaling.
"""

import numpy as np
import matplotlib.pyplot as plt

def rk4_step(f, t, y, h):
    k1 = f(t,          y)
    k2 = f(t + 0.5*h,  y + 0.5*h*k1)
    k3 = f(t + 0.5*h,  y + 0.5*h*k2)
    k4 = f(t + h,      y + h*k3)
    return y + (h/6)*(k1 + 2*k2 + 2*k3 + k4)

# ODE and exact solution
f_exact = lambda t: np.exp(-t)
f_rhs   = lambda t, y: -y

h_values = [0.4, 0.2, 0.1, 0.05]
errors   = []

for h in h_values:
    t_end = 5.0
    steps = int(t_end/h)
    t = 0.0
    y = 1.0
    for _ in range(steps):
        y = rk4_step(f_rhs, t, y, h)
        t += h
    exact = f_exact(t_end)
    errors.append(abs(y - exact))

# Plot convergence
plt.figure(figsize=(7,5))
plt.loglog(h_values, errors, 'o-', label='RK4 global error')
plt.loglog(h_values, [errors[-1]*(h/h_values[-1])**4 for h in h_values],
           '--', label=r'$h^{4}$ reference')
plt.gca().invert_xaxis()
plt.xlabel("Step size h (log scale)")
plt.ylabel("Error at t = 5 (log scale)")
plt.title("Convergence of RK4 on dy/dt = -y")
plt.legend()
plt.grid(True, which="both", ls=":")
plt.tight_layout()
plt.show()

# Plot numerical vs exact for one step size
h = 0.1
t_vals = np.arange(0, 5+h, h)
y_vals = [1.0]
for t in t_vals[:-1]:
    y_vals.append(rk4_step(f_rhs, t, y_vals[-1], h))
plt.figure(figsize=(7,5))
plt.plot(t_vals, y_vals, 'o-', label=f'RK4, h={h}')
plt.plot(t_vals, f_exact(t_vals), '--', label='Exact e^{-t}')
plt.xlabel("t")
plt.ylabel("y(t)")
plt.title("RK4 Solution vs Exact")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
