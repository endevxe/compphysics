"""
Finite square well: bound‑state energies and wavefunctions

Method: shoot from x=0 toward x=L, matching derivatives at the centre.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

# ---------------- parameters ----------------
hbar = 1.0
m    = 1.0
L    = 1.0          # width of well
V0   = 50.0         # barrier height outside well
n_states = 4
Nplot = 1000
# --------------------------------------------

def V(x):
    return 0.0 if 0 < x < L else V0

def schro_ode(x, y, E):
    psi, dpsi = y
    return [dpsi, 2*m/hbar**2 * (V(x) - E) * psi]

def shoot(E):
    # integrate from left wall into well (to centre)
    sol = solve_ivp(
        schro_ode, [0, L/2], [0, 1e-6], args=(E,),
        max_step=L/400, rtol=1e-8, atol=1e-8
    )
    psi_mid = sol.y[0, -1]
    return psi_mid  # node at centre needed for even/odd separation

# bracket roots using analytic infinite‑well energies as guesses
E_inf = [(np.pi*n/L)**2 * hbar**2 / (2*m) for n in range(1, n_states+3)]
E_low = [0.1] + [0.5*(E_inf[i-1]+E_inf[i]) for i in range(1, n_states+2)]
E_high = E_inf[1:n_states+3]

energies = []
for lo, hi in zip(E_low, E_high):
    try:
        Eroot = brentq(shoot, lo, hi, xtol=1e-10)
        energies.append(Eroot)
        if len(energies) >= n_states:
            break
    except ValueError:
        pass  # no root in interval

# plot eigenfunctions
x = np.linspace(0, L, Nplot)
plt.figure(figsize=(8, 5))
for k, E in enumerate(energies, 1):
    sol = solve_ivp(
        schro_ode, [0, L], [0, 1e-6], args=(E,),
        t_eval=x, max_step=L/400, rtol=1e-8, atol=1e-8
    )
    psi = sol.y[0]
    # normalise
    norm = np.trapz(psi**2, x)
    psi /= np.sqrt(norm)
    plt.plot(x, psi, label=fr"$n={k},\;E={E:.3f}$")

plt.title("Finite Square Well – Bound States")
plt.xlabel("x")
plt.ylabel(r"$\psi_n(x)$")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
