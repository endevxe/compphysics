"""
1‑D Wave Equation (string) solved by finite–difference method;
generates an animated Plotly HTML file.

Equation:  ∂²u/∂t² = c² ∂²u/∂x²   with fixed ends.

Author: Episteme
"""
import numpy as np
import plotly.graph_objects as go

# ---------------- simulation parameters ----------------
L     = 1.0        # string length
c     = 1.0        # wave speed  (√(T/ρ) with ρ = 1, T = 1)
N     = 200        # spatial points
dx    = L / N
dt    = 0.5 * dx / c           # CFL‑stable time step
steps = 300                    # total time steps to animate

# ---------------- initial displacement -----------------
x  = np.linspace(0, L, N)
u0 = np.exp(-1000 * (x - 0.3) ** 2)   # Gaussian pulse
u1 = np.copy(u0)                      # assume zero initial velocity
u2 = np.zeros_like(u0)

frames = []

for n in range(steps):
    # finite‑difference update (fixed ends)
    for i in range(1, N - 1):
        u2[i] = (2 * u1[i] - u0[i] +
                 (c * dt / dx) ** 2 *
                 (u1[i + 1] - 2 * u1[i] + u1[i - 1]))
    frames.append(
        go.Frame(
            data=[go.Scatter(x=x, y=u2, mode="lines")],
            name=str(n)
        )
    )
    u0, u1 = u1, u2.copy()

# ---------------- Plotly figure ------------------------
fig = go.Figure(
    data=[go.Scatter(x=x, y=u0, mode="lines", line=dict(color="#6a0dad"))],
    layout=go.Layout(
        title="1D Wave Equation Simulation",
        xaxis=dict(title="x"),
        yaxis=dict(title="Displacement"),
        paper_bgcolor="#000",
        plot_bgcolor="#000",
        font=dict(color="#f5f5f5"),
        updatemenus=[dict(
            type="buttons",
            buttons=[
                dict(label="Play",  method="animate", args=[None]),
                dict(label="Pause", method="animate",
                     args=[[None],
                           {"frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0}}])
            ]
        )],
        margin=dict(t=40, b=40, l=40, r=40),
    ),
    frames=frames
)

fig.write_html("wave_equation.html", include_plotlyjs="cdn")
print("Saved → wave_equation.html")
