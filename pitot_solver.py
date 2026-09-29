"""
pitot_solver.py
----------------
Converts Indicated/Calibrated Airspeed (IAS/CAS) to True Airspeed (TAS)
using standard pitot-static and compressible-flow relations, and computes
Mach number.

Two models are provided:

1. Incompressible (low speed, e.g. < ~200 kt / low altitude):
       TAS = CAS * sqrt(rho0 / rho)

2. Compressible (isentropic flow, valid at any subsonic speed/altitude -
   this is the model real airspeed indicators are built around):
       qc = P0 * [ (1 + 0.2*(CAS/a0)^2)^3.5 - 1 ]        (impact pressure)
       M  = sqrt( 5 * [ (qc / P + 1)^(2/7) - 1 ] )         (local Mach number)
       TAS = M * a(altitude)

Imports `constants` and `isa_engine` directly (flat, same-folder) -
no "src." prefix anywhere.
"""

import math
from dataclasses import dataclass

from constants import A0_SL, P0_SL, RHO0_SL
from isa_engine import AtmosphereState, get_atmosphere
from validators import validate_airspeed


@dataclass(frozen=True)
class AirspeedResult:
    """Result of a CAS/IAS -> TAS conversion."""
    ias_kt: float
    altitude_m: float
    mach: float
    tas_kt: float
    tas_mps: float
    model: str
    atmosphere: AtmosphereState


def tas_incompressible(ias_kt: float, altitude_m: float) -> AirspeedResult:
    """
    Simple incompressible approximation. Good below ~10,000 ft and
    ~200 kt; increasingly inaccurate at high speed/altitude because it
    ignores air compressibility.
    """
    ias_kt = validate_airspeed(ias_kt, "IAS", max_value=700)
    atmosphere = get_atmosphere(altitude_m)

    ias_mps = ias_kt / 1.9438444924
    tas_mps = ias_mps * math.sqrt(RHO0_SL / atmosphere.density_kg_m3)
    mach = tas_mps / atmosphere.speed_of_sound_mps
    tas_kt = tas_mps * 1.9438444924

    return AirspeedResult(
        ias_kt=ias_kt,
        altitude_m=atmosphere.geometric_altitude_m,
        mach=mach,
        tas_kt=tas_kt,
        tas_mps=tas_mps,
        model="incompressible",
        atmosphere=atmosphere,
    )


def tas_compressible(cas_kt: float, altitude_m: float) -> AirspeedResult:
    """
    Full compressible (isentropic) CAS -> Mach -> TAS conversion, matching
    the physics behind a real mechanical airspeed indicator.
    """
    cas_kt = validate_airspeed(cas_kt, "CAS", max_value=700)
    atmosphere = get_atmosphere(altitude_m)

    cas_mps = cas_kt / 1.9438444924

    # Impact pressure implied by CAS, referenced to sea-level standard day.
    qc = P0_SL * ((1 + 0.2 * (cas_mps / A0_SL) ** 2) ** 3.5 - 1)

    # Local Mach number from impact pressure and actual static pressure.
    mach = math.sqrt(5 * ((qc / atmosphere.pressure_pa + 1) ** (2 / 7) - 1))

    tas_mps = mach * atmosphere.speed_of_sound_mps
    tas_kt = tas_mps * 1.9438444924

    return AirspeedResult(
        ias_kt=cas_kt,
        altitude_m=atmosphere.geometric_altitude_m,
        mach=mach,
        tas_kt=tas_kt,
        tas_mps=tas_mps,
        model="compressible",
        atmosphere=atmosphere,
    )


def mach_to_tas(mach: float, altitude_m: float) -> float:
    """Convert a known Mach number to TAS (m/s) at a given altitude."""
    if mach < 0:
        raise ValueError("Mach number cannot be negative")
    atmosphere = get_atmosphere(altitude_m)
    return mach * atmosphere.speed_of_sound_mps


def tas_to_mach(tas_mps: float, altitude_m: float) -> float:
    """Convert TAS (m/s) to Mach number at a given altitude."""
    atmosphere = get_atmosphere(altitude_m)
    return tas_mps / atmosphere.speed_of_sound_mps
