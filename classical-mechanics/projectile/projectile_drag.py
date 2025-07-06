"""
Projectile motion with and without quadratic air resistance.
Compares trajectories on a single plot.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------- Parameters ----------------
g   = 9.81        # m s⁻²
v0  = 50.0        # initial speed (m/s)
ang = 40.0        # launch angle (degrees)
k   = 0.02        # drag coefficient (kg⁻¹ m⁻¹)
m   = 1.0         # projectile mass (kg)

dt  = 1e-3        # time step (s)
t_max = 10        # max integration time (s)
# --------------------------------------------

theta = np.radians(ang)
vx0, vy0 = v0*np.cos(theta), v0*np.sin(theta)

def accel(vx, vy):
    """Accelerations with quadratic drag."""
    v = np.hypot(vx, vy)
    ax = -k/m * v * vx
    ay = -g - (k/m) * v * vy
    return ax, ay

def integrate(vx0, vy0, drag=True):
    """Returns arrays x, y for the chosen model."""
    x, y = [0.0], [0.0]
    vx, vy = vx0, vy0
    t = 0.0
    while y[-1] >= 0 and t < t_max:
        if drag:
            ax, ay = accel(vx, vy)
        else:
            ax, ay = 0.0, -g
        # RK4
        def f(vx, vy):
            return accel(vx, vy) if drag else (0.0, -g)

        k1_vx, k1_vy = f(vx, vy)
        k1_x,  k1_y  = vx, vy

        k2_vx, k2_vy = f(vx+0.5*dt*k1_vx, vy+0.5*dt*k1_vy)
        k2_x,  k2_y  = vx+0.5*dt*k1_vx, vy+0.5*dt*k1_vy

        k3_vx, k3_vy = f(vx+0.5*dt*k2_vx, vy+0.5*dt*k2_vy)
        k3_x,  k3_y  = vx+0.5*dt*k2_vx, vy+0.5*dt*k2_vy

        k4_vx, k4_vy = f(vx+dt*k3_vx, vy+dt*k3_vy)
        k4_x,  k4_y  = vx+dt*k3_vx, vy+dt*k3_vy

        vx += dt/6*(k1_vx + 2*k2_vx + 2*k3_vx + k4_vx)
        vy += dt/6*(k1_vy + 2*k2_vy + 2*k3_vy + k4_vy)
        x_new = x[-1] + dt/6*(k1_x + 2*k2_x + 2*k3_x + k4_x)
        y_new = y[-1] + dt/6*(k1_y + 2*k2_y + 2*k3_y + k4_y)

        x.append(x_new)
        y.append(y_new)
        t += dt
    return np.array(x), np.array(y)

# Integrate
x_drag, y_drag = integrate(vx0, vy0, drag=True)
x_ideal, y_ideal = integrate(vx0, vy0, drag=False)

# Plot
plt.figure(figsize=(8,5))
plt.plot(x_ideal, y_ideal, label='Ideal (no drag)')
plt.plot(x_drag,  y_drag,  label='With quadratic drag')
plt.title("Projectile Motion: Ideal vs Air Resistance")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
