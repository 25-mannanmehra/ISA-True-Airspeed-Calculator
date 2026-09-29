"""
isa_engine.py
-------------
Implements the ICAO International Standard Atmosphere (ISA) model from sea
level up to 51 km (troposphere -> tropopause -> lower stratosphere ->
stratopause).

Physics reference (standard aerospace formulas):
  Gradient layer (lapse rate L != 0):
      T(h) = Tb + L * (h - hb)
      P(h) = Pb * (T(h) / Tb) ** (-g0 / (R * L))

  Isothermal layer (L == 0):
      T(h) = Tb
      P(h) = Pb * exp(-g0 * (h - hb) / (R * Tb))

  Ideal gas law:
      rho(h) = P(h) / (R * T(h))

  Speed of sound:
      a(h) = sqrt(gamma * R * T(h))

  Dynamic viscosity (Sutherland's law):
      mu(T) = mu0 * (T / T0)^1.5 * (T0 + S) / (T + S)

Imports `constants` and `validators` directly (flat, same-folder) -
no "src." prefix anywhere.
"""

import math
from dataclasses import dataclass

from constants import (
    EARTH_RADIUS, G0, GAMMA, ISA_LAYERS, P0_SL, R_SPECIFIC,
    SUTHERLAND_MU0, SUTHERLAND_S, SUTHERLAND_T0,
)
from validators import validate_altitude_m


@dataclass(frozen=True)
class AtmosphereState:
    """Immutable snapshot of atmospheric conditions at one altitude."""
    geometric_altitude_m: float
    geopotential_altitude_m: float
    temperature_k: float
    pressure_pa: float
    density_kg_m3: float
    speed_of_sound_mps: float
    dynamic_viscosity_pas: float

    def __str__(self) -> str:
        return (
            f"h={self.geometric_altitude_m:8.1f} m | "
            f"T={self.temperature_k:7.2f} K | "
            f"P={self.pressure_pa:10.2f} Pa | "
            f"rho={self.density_kg_m3:8.5f} kg/m^3 | "
            f"a={self.speed_of_sound_mps:6.2f} m/s"
        )


def geometric_to_geopotential(altitude_geometric_m: float) -> float:
    """Convert geometric altitude H to geopotential altitude h."""
    return (EARTH_RADIUS * altitude_geometric_m) / (EARTH_RADIUS + altitude_geometric_m)


def geopotential_to_geometric(altitude_geopotential_m: float) -> float:
    """Convert geopotential altitude h back to geometric altitude H."""
    return (EARTH_RADIUS * altitude_geopotential_m) / (EARTH_RADIUS - altitude_geopotential_m)


def _find_layer(h: float):
    """Return the (base_h, base_T, lapse_rate) tuple of the ISA layer containing h."""
    layer = ISA_LAYERS[0]
    for candidate in ISA_LAYERS:
        if h >= candidate[0]:
            layer = candidate
        else:
            break
    return layer


def _pressure_at_base(layer_index: int) -> float:
    """
    Recursively compute the pressure at the base of ISA_LAYERS[layer_index]
    by chaining the layer equations from sea level upward.
    """
    if layer_index == 0:
        return P0_SL

    hb, tb, lapse = ISA_LAYERS[layer_index - 1]
    h_top = ISA_LAYERS[layer_index][0]
    p_base = _pressure_at_base(layer_index - 1)

    if lapse == 0.0:
        return p_base * math.exp(-G0 * (h_top - hb) / (R_SPECIFIC * tb))
    t_top = tb + lapse * (h_top - hb)
    return p_base * (t_top / tb) ** (-G0 / (R_SPECIFIC * lapse))


def dynamic_viscosity(temperature_k: float) -> float:
    """Sutherland's law: dynamic viscosity of air (Pa*s) as a function of T (K)."""
    return (
        SUTHERLAND_MU0
        * (temperature_k / SUTHERLAND_T0) ** 1.5
        * (SUTHERLAND_T0 + SUTHERLAND_S)
        / (temperature_k + SUTHERLAND_S)
    )


def get_atmosphere(altitude_m: float, is_geopotential: bool = False) -> AtmosphereState:
    """
    Compute full ISA atmospheric state at a given altitude.

    Args:
        altitude_m: altitude value in metres.
        is_geopotential: if True, `altitude_m` is treated as geopotential
            height directly; otherwise it is treated as geometric altitude
            (e.g. what an altimeter / GPS reports) and converted internally.

    Returns:
        AtmosphereState with temperature, pressure, density, speed of sound
        and dynamic viscosity.
    """
    altitude_m = validate_altitude_m(altitude_m)

    if is_geopotential:
        h = altitude_m
        h_geometric = geopotential_to_geometric(h)
    else:
        h_geometric = altitude_m
        h = geometric_to_geopotential(altitude_m)

    hb, tb, lapse = _find_layer(h)
    layer_index = ISA_LAYERS.index((hb, tb, lapse))
    p_base = _pressure_at_base(layer_index)

    if lapse == 0.0:
        temperature = tb
        pressure = p_base * math.exp(-G0 * (h - hb) / (R_SPECIFIC * tb))
    else:
        temperature = tb + lapse * (h - hb)
        pressure = p_base * (temperature / tb) ** (-G0 / (R_SPECIFIC * lapse))

    density = pressure / (R_SPECIFIC * temperature)
    speed_of_sound = math.sqrt(GAMMA * R_SPECIFIC * temperature)
    viscosity = dynamic_viscosity(temperature)

    return AtmosphereState(
        geometric_altitude_m=h_geometric,
        geopotential_altitude_m=h,
        temperature_k=temperature,
        pressure_pa=pressure,
        density_kg_m3=density,
        speed_of_sound_mps=speed_of_sound,
        dynamic_viscosity_pas=viscosity,
    )


def get_atmosphere_profile(start_m: float, end_m: float, step_m: float = 1000.0):
    """Return a list of AtmosphereState objects sampled from start_m to end_m."""
    if step_m <= 0:
        raise ValueError("step_m must be positive")
    altitudes = []
    h = start_m
    while h <= end_m + 1e-9:
        altitudes.append(round(h, 3))
        h += step_m
    return [get_atmosphere(a) for a in altitudes]
