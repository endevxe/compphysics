"""
Infinite square well – plot many eigenstates quickly by analytic formula
"""

import numpy as np
import matplotlib.pyplot as plt

L = 1.0
Nstates = 8          # change for more
Nplot   = 800
x = np.linspace(0, L, Nplot)

plt.figure(figsize=(8, 5))
for n in range(1, Nstates+1):
    psi = np.sqrt(2/L) * np.sin(n*np.pi*x/L)
    En  = (n*np.pi)**2 / 2           # hbar = m = 1
    plt.plot(x, psi + 1.8*(n-1), label=fr"$n={n},\,E={En:.1f}$")  # vertical offset

plt.title("Infinite Well – First Many Eigenfunctions (offset for clarity)")
plt.xlabel("x")
plt.yticks([])
plt.legend(ncol=2, fontsize=8)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
