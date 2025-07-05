#!/usr/bin/env python3
"""
Gaussian wave‑packet in an infinite square well
Split‑operator (FFT) method
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
hbar = 1.0
m    = 1.0
L    = 1.0
Nx   = 1024
dt   = 0.002
Nt   = 800          # number of time steps
save_every = 40

x = np.linspace(0, L, Nx, endpoint=False)
dx = x[1] - x[0]
k = 2*np.pi*np.fft.fftfreq(Nx, d=dx)

# Initial Gaussian
x0   = 0.3*L
sigma= 0.05*L
p0   = 40.0
psi = np.exp(-(x-x0)**2/(2*sigma**2)) * np.exp(1j*p0*(x-x0)/hbar)
psi /= np.sqrt(np.trapz(np.abs(psi)**2, x))

# Pre‑compute evolution operators
V = np.zeros_like(x)             # V=0 inside well
T_factor = np.exp(-1j * (hbar*k**2)/(2*m) * dt /2)
V_factor = np.exp(-1j * V / hbar * dt)

frames = []
for t in range(Nt):
    # half‑kick in momentum space
    psi_k = np.fft.fft(psi)
    psi_k *= T_factor
    psi = np.fft.ifft(psi_k)
    # potential kick
    psi *= V_factor
    # another half‑kick
    psi_k = np.fft.fft(psi)
    psi_k *= T_factor
    psi = np.fft.ifft(psi_k)

    if t % save_every == 0:
        frames.append(np.abs(psi)**2)

# animate / plot snapshots
plt.figure(figsize=(8,5))
for i,prob in enumerate(frames):
    plt.plot(x, prob + 1.1*i, lw=1)   # vertical offset
plt.title("Gaussian Wave Packet – Evolution (offset snapshots)")
plt.xlabel("x")
plt.ylabel(r"$|\psi(x,t)|^{2}$  (offset)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
