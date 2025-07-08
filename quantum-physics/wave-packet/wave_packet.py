"""Gaussian wave‑packet reflection & tunnelling
Split‑operator (FFT) method, ħ=m=1, finite rectangular barrier V0,a.
Plots |ψ(x,t)|^2 at several times. """
import numpy as np, matplotlib.pyplot as plt
L=200; N=2048; dx=L/N; x=np.linspace(-L/2,L/2,N)
V0=1.0; a=5.0; V=np.where(abs(x)<a/2,V0,0)
# initial packet
x0=-40; k0=2.0; sigma=4
psi=np.exp(-(x-x0)**2/(2*sigma**2))*np.exp(1j*k0*x)
psi/=np.sqrt(np.sum(abs(psi)**2)*dx)
# split‑operator params
dt=0.05; steps=800
k=np.fft.fftfreq(N,dx)*2*np.pi
Kfactor=np.exp(-0.5j*k**2*dt)
Vhalf=np.exp(-0.5j*V*dt)
frames=[]
for s in range(steps):
    psi=Vhalf*psi
    psi=np.fft.ifft(Kfactor*np.fft.fft(psi))
    psi=Vhalf*psi
    if s%100==0:
        frames.append(abs(psi)**2)
# plot snapshots
for i,f in enumerate(frames):
    plt.plot(x,f+i*0.02,label=f't={(i*100*dt):.1f}')
plt.xlabel('x');plt.ylabel('|ψ|² offset');plt.title('Wave‑packet reflection & tunnelling')
plt.legend();plt.tight_layout();plt.show()
