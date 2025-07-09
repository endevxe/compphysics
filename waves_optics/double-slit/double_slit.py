"""
Young’s Double Slit Interference Pattern — 1D simulation

I(θ) ∝ cos²(π d sinθ / λ)
      ≈ cos²(π d x / (λ L))  using small-angle approx

Author: Episteme
"""

import numpy as np
import plotly.graph_objects as go

# ---------- Parameters ----------
wavelength = 500e-9     # 500 nm
d = 20e-6               # slit separation (20 µm)
L = 1.0                 # screen distance (1 m)
x = np.linspace(-5e-3, 5e-3, 1000)  # screen coordinate (–5 mm to +5 mm)

# intensity formula (no envelope)
k = np.pi * d / (wavelength * L)
I = np.cos(k * x)**2

# normalize
I /= I.max()

# ---------- Plot ----------
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=1e3 * x, y=I,
    mode="lines",
    line=dict(color="#6a0dad"),
    name="Intensity"
))

fig.update_layout(
    title="Double Slit Interference Pattern",
    xaxis_title="Screen Position x (mm)",
    yaxis_title="Normalized Intensity I(x)",
    paper_bgcolor="#000",
    plot_bgcolor="#000",
    font=dict(color="#f5f5f5"),
    margin=dict(t=40, b=40),
)

fig.write_html("double_slit.html", include_plotlyjs="cdn")
print("Saved → double_slit.html")
