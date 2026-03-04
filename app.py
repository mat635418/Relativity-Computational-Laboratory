import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

# =========================
# CONSTANTS
# =========================

c = 299_792_458  # speed of light (m/s)

# =========================
# PHYSICS CORE
# =========================

def gamma(v):
    if abs(v) >= c:
        raise ValueError("Velocity must satisfy |v| < c.")
    return 1.0 / np.sqrt(1 - (v**2 / c**2))

def time_dilation(delta_tau, v):
    return gamma(v) * delta_tau

def length_contraction(L0, v):
    return L0 / gamma(v)

def lorentz_transform(t, x, v):
    g = gamma(v)
    t_prime = g * (t - v * x / c**2)
    x_prime = g * (x - v * t)
    return t_prime, x_prime

def spacetime_interval(t, x):
    return -c**2 * t**2 + x**2

def proper_time_integral(t_array, v_array):
    integrand = np.sqrt(1 - (v_array**2 / c**2))
    return np.trapz(integrand, t_array)

# =========================
# STREAMLIT UI
# =========================

st.set_page_config(page_title="Relativity Computational Laboratory", layout="wide")

st.title("Relativity Computational Laboratory")
st.markdown("Inspired by Albert Einstein's Special Relativity")

# Sidebar
st.sidebar.header("Control Panel")

velocity_fraction = st.sidebar.slider("Velocity (fraction of c)", 0.0, 0.9999, 0.5)
v = velocity_fraction * c

proper_time_input = st.sidebar.number_input("Proper Time (seconds)", 1.0, 1e9, 10.0)

distance_input = st.sidebar.number_input("Proper Length (meters)", 1.0, 1e9, 100.0)

trajectory_type = st.sidebar.selectbox(
    "Trajectory Type",
    ["Constant Velocity", "Sinusoidal Velocity"]
)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Lorentz Factor",
    "Time Dilation",
    "Twin Paradox",
    "Minkowski Diagram",
    "Scientific Report"
])

# =========================
# TAB 1 — LORENTZ FACTOR
# =========================

with tab1:
    st.header("Lorentz Factor γ(v)")
    
    velocities = np.linspace(0, 0.9999*c, 1000)
    gammas = 1 / np.sqrt(1 - velocities**2 / c**2)
    
    fig, ax = plt.subplots()
    ax.plot(velocities/c, gammas)
    ax.set_xlabel("v / c")
    ax.set_ylabel("γ(v)")
    ax.set_title("Lorentz Factor Divergence")
    st.pyplot(fig)
    
    st.write("Current γ:", gamma(v))

# =========================
# TAB 2 — TIME DILATION
# =========================

with tab2:
    st.header("Time Dilation")
    
    dilated_time = time_dilation(proper_time_input, v)
    contraction = length_contraction(distance_input, v)
    
    st.write("Proper Time:", proper_time_input, "seconds")
    st.write("Dilated Time:", dilated_time, "seconds")
    st.write("Proper Length:", distance_input, "meters")
    st.write("Contracted Length:", contraction, "meters")

# =========================
# TAB 3 — TWIN PARADOX
# =========================

with tab3:
    st.header("Twin Paradox Simulator")
    
    earth_time = proper_time_input
    traveler_time = earth_time / gamma(v)
    
    st.write("Earth Twin Ages:", earth_time, "seconds")
    st.write("Traveling Twin Ages:", traveler_time, "seconds")
    st.write("Age Difference:", earth_time - traveler_time, "seconds")

# =========================
# TAB 4 — MINKOWSKI DIAGRAM
# =========================

with tab4:
    st.header("Minkowski Spacetime Diagram")
    
    t = np.linspace(0, 10, 100)
    x_stationary = np.zeros_like(t)
    x_moving = v * t
    
    fig, ax = plt.subplots()
    
    # Worldlines
    ax.plot(x_stationary, c*t, label="Stationary Observer")
    ax.plot(x_moving, c*t, label="Moving Observer")
    
    # Light cone
    ax.plot(c*t, c*t, linestyle="--")
    ax.plot(-c*t, c*t, linestyle="--")
    
    ax.set_xlabel("x")
    ax.set_ylabel("ct")
    ax.legend()
    
    st.pyplot(fig)

# =========================
# TAB 5 — SCIENTIFIC REPORT
# =========================

with tab5:
    st.header("Formal Mathematical Report")
    
    st.latex(r"\gamma(v) = \frac{1}{\sqrt{1 - \frac{v^2}{c^2}}}")
    
    st.latex(r"\Delta t = \gamma(v) \Delta \tau")
    
    st.latex(r"L = \frac{L_0}{\gamma(v)}")
    
    st.latex(r"-c^2 t^2 + x^2 = -c^2 t'^2 + x'^2")
    
    st.markdown("""
**Definition (Lorentz Factor).**

The Lorentz factor is defined as:

γ(v) = (1 - v²/c²)^(-1/2)

**Time Dilation Theorem.**

A clock moving at velocity v relative to an inertial observer
experiences proper time:

Δτ = Δt √(1 - v²/c²)

**Invariance of Spacetime Interval.**

The quantity:

−c²t² + x²

is invariant under Lorentz transformations.
""")
