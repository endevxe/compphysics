"""Least‑Squares Fitting demo
Generates noisy linear data, fits a line using numpy.polyfit, and plots
(1) data + best‑fit line  (2) residuals.  Computes R^2 and RMSE.
"""
import numpy as np
import matplotlib.pyplot as plt

# --- synthetic data ---
np.random.seed(0)
true_m, true_b = 2.0, 1.0
x = np.linspace(0, 10, 30)
y_true = true_m * x + true_b
noise = np.random.normal(scale=2.0, size=x.size)
y_noisy = y_true + noise

# --- least‑squares fit ---
coef = np.polyfit(x, y_noisy, 1)  # [m,b]
fit_m, fit_b = coef
y_fit = fit_m * x + fit_b

# --- residuals & error metrics ---
residuals = y_noisy - y_fit
rmse = np.sqrt(np.mean(residuals**2))
ss_res = np.sum(residuals**2)
ss_tot = np.sum((y_noisy - np.mean(y_noisy))**2)
R2 = 1 - ss_res/ss_tot

# --- plots ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7,8), gridspec_kw={'height_ratios':[3,1]})
ax1.scatter(x, y_noisy, label='Noisy data', color='white', edgecolors='k')
ax1.plot(x, y_fit, color='#6a0dad', label=f'Best fit: y={fit_m:.2f}x+{fit_b:.2f}')
ax1.set_title('Least‑Squares Linear Fit')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.legend()
ax1.grid(alpha=0.3)

ax2.axhline(0, color='gray', lw=1)
ax2.scatter(x, residuals, color='#ffcc00', edgecolors='k', s=40)
ax2.set_xlabel('x')
ax2.set_ylabel('Residual')
ax2.set_title(f'Residuals  |  RMSE={rmse:.2f},  R²={R2:.3f}')
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.show()
