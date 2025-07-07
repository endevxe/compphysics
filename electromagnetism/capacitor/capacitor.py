#!/usr/bin/env python3
"""
Capacitor charging and discharging in an RC circuit.
Plots V(t) for both processes and marks the time constant tau = RC.
"""
import numpy as np
import matplotlib.pyplot as plt

# Parameters
R = 1e3           # resistance in ohms
C = 1e-6          # capacitance in farads
V0 = 5            # supply voltage in volts

tau = R * C       # time constant

# Time array (10 tau for full curve)
t = np.linspace(0, 10 * tau, 1000)

# Charging: V(t) = V0 (1 - exp(-t/RC))
V_charge = V0 * (1 - np.exp(-t / tau))

# Discharging: V(t) = V0 * exp(-t/RC)
V_discharge = V0 * np.exp(-t / tau)

plt.figure(figsize=(8,5))
plt.plot(t * 1e3, V_charge, label='Charging')
plt.plot(t * 1e3, V_discharge, label='Discharging')
plt.axvline(tau * 1e3, color='gray', ls='--', label=f'$t=\tau={tau*1e3:.1f}$ ms')
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.title('RC Circuit: Capacitor Charging & Discharging')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
