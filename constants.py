"""
constants.py
------------
Physical and standard-atmosphere constants used across the project.
Values follow the ICAO / ISO 2533 International Standard Atmosphere (ISA).

No imports from other project files - safe to import from anywhere.
"""

# --- Universal / air constants -------------------------------------------------
GAMMA = 1.4                # Ratio of specific heats for air (Cp/Cv)
R_SPECIFIC = 287.05287     # Specific gas constant for dry air, J/(kg*K)
G0 = 9.80665               # Standard gravitational acceleration, m/s^2
EARTH_RADIUS = 6_356_766   # Effective earth radius for geopotential conversion, m

# Sutherland's law constants (dynamic viscosity of air)
SUTHERLAND_MU0 = 1.716e-5  # Reference viscosity at T0, Pa*s
SUTHERLAND_T0 = 273.15     # Reference temperature, K
SUTHERLAND_S = 110.4       # Sutherland constant for air, K

# --- Sea level standard conditions (h = 0 m) ------------------------------------
T0_SL = 288.15             # Temperature, K (15 deg C)
P0_SL = 101325.0           # Pressure, Pa
RHO0_SL = 1.225            # Density, kg/m^3
A0_SL = 340.294            # Speed of sound, m/s

# --- ISA layer table -------------------------------------------------------------
# Each row: (base_geopotential_height_m, base_temperature_K, lapse_rate_K_per_m)
# A lapse rate of 0.0 marks an isothermal layer.
ISA_LAYERS = [
    (0.0,     288.15, -0.0065),   # Troposphere
    (11000.0, 216.65,  0.0),      # Tropopause (isothermal)
    (20000.0, 216.65,  0.0010),   # Stratosphere I
    (32000.0, 228.65,  0.0028),   # Stratosphere II
    (47000.0, 270.65,  0.0),      # Stratopause (isothermal)
]

MAX_SUPPORTED_ALTITUDE_M = 51000.0
MIN_SUPPORTED_ALTITUDE_M = 0.0
