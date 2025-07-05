import numpy as np
import matplotlib.pyplot as plt

# Parameters
g = 9.81      # gravity (m/s^2)
L = 1.0       # length (m)
theta0 = np.pi / 4  # initial angle (radians)
omega0 = 0.0        # initial angular velocity
dt = 0.01
T = 10
steps = int(T / dt)

# Define system of equations
def derivatives(theta, omega):
    dtheta_dt = omega
    domega_dt = - (g / L) * np.sin(theta)
    return dtheta_dt, domega_dt

# Runge-Kutta 4th order
theta = theta0
omega = omega0
time = [0]
theta_list = [theta]

for i in range(steps):
    k1_theta, k1_omega = derivatives(theta, omega)
    k2_theta, k2_omega = derivatives(theta + 0.5*dt*k1_theta, omega + 0.5*dt*k1_omega)
    k3_theta, k3_omega = derivatives(theta + 0.5*dt*k2_theta, omega + 0.5*dt*k2_omega)
    k4_theta, k4_omega = derivatives(theta + dt*k3_theta, omega + dt*k3_omega)

    theta += (dt / 6) * (k1_theta + 2*k2_theta + 2*k3_theta + k4_theta)
    omega += (dt / 6) * (k1_omega + 2*k2_omega + 2*k3_omega + k4_omega)

    time.append(time[-1] + dt)
    theta_list.append(theta)

# Plot
plt.plot(time, theta_list)
plt.title("Simple Pendulum Simulation (RK4)")
plt.xlabel("Time (s)")
plt.ylabel("Angle (rad)")
plt.grid(True)
plt.show()
