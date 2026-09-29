"""
visualizer.py
-------------
Generates matplotlib plots of ISA properties versus altitude. Imports flat,
same-folder - no "src." prefix. Requires: pip install matplotlib
"""

import matplotlib
matplotlib.use("Agg")  # headless-safe backend
import matplotlib.pyplot as plt

from isa_engine import get_atmosphere_profile
from unit_utils import m_to_ft


def plot_profile(start_m: float = 0, end_m: float = 47000, step_m: float = 500,
                  save_path: str = "output/isa_profile.png") -> str:
    """
    Plot temperature, pressure and density versus altitude on one figure
    with three stacked subplots, and save it as a PNG.

    Returns the path the figure was saved to.
    """
    states = get_atmosphere_profile(start_m, end_m, step_m)
    alt_ft = [m_to_ft(s.geometric_altitude_m) for s in states]
    temps = [s.temperature_k for s in states]
    pressures = [s.pressure_pa / 1000 for s in states]
    densities = [s.density_kg_m3 for s in states]

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    axes[0].plot(temps, alt_ft, color="#c0392b")
    axes[0].set_xlabel("Temperature (K)")
    axes[0].set_ylabel("Altitude (ft)")
    axes[0].set_title("Temperature vs Altitude")
    axes[0].grid(alpha=0.3)

    axes[1].plot(pressures, alt_ft, color="#2980b9")
    axes[1].set_xlabel("Pressure (kPa)")
    axes[1].set_title("Pressure vs Altitude")
    axes[1].grid(alpha=0.3)

    axes[2].plot(densities, alt_ft, color="#27ae60")
    axes[2].set_xlabel("Density (kg/m^3)")
    axes[2].set_title("Density vs Altitude")
    axes[2].grid(alpha=0.3)

    fig.suptitle("ISA Standard Atmosphere Profile")
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    return save_path


def plot_tas_vs_altitude(ias_kt: float, start_m: float = 0, end_m: float = 15000,
                          step_m: float = 500, save_path: str = "output/tas_profile.png") -> str:
    """
    For a fixed indicated airspeed, plot how True Airspeed grows with
    altitude and save it as a PNG.
    """
    from pitot_solver import tas_compressible

    altitudes = []
    h = start_m
    while h <= end_m + 1e-9:
        altitudes.append(h)
        h += step_m

    results = [tas_compressible(ias_kt, a) for a in altitudes]
    alt_ft = [m_to_ft(a) for a in altitudes]
    tas_values = [r.tas_kt for r in results]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(tas_values, alt_ft, marker="o", markersize=3, color="#8e44ad")
    ax.axvline(ias_kt, color="gray", linestyle="--", label=f"IAS = {ias_kt} kt")
    ax.set_xlabel("True Airspeed (kt)")
    ax.set_ylabel("Altitude (ft)")
    ax.set_title(f"TAS vs Altitude for constant IAS = {ias_kt} kt")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    return save_path
