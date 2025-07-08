"""Quantum Harmonic Oscillator Eigenstates
Plots the first few eigenfunctions and prints energies (ℏ=m=ω=1).
"""
import numpy as np
import matplotlib.pyplot as plt
from math import factorial, pi, sqrt

# Hermite polynomial via recursion
def H(n, x):
    if n == 0:
        return 1
    elif n == 1:
        return 2*x
    else:
        return 2*x*H(n-1, x) - 2*(n-1)*H(n-2, x)

x = np.linspace(-4, 4, 1000)
fig, ax = plt.subplots(figsize=(8,6))
for n in range(4):
    psi = (1/ sqrt(2**n * factorial(n) * sqrt(pi))) * np.exp(-x**2/2) * H(n, x)
    ax.plot(x, psi + n*0.5, label=f"n={n}, E={n+0.5}")

ax.set_title('Harmonic Oscillator Eigenfunctions')
ax.set_xlabel('x')
ax.set_ylabel('ψ_n(x)  (offset)')
ax.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
