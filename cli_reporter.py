"""
cli_reporter.py
----------------
Formats ISA atmosphere and airspeed results as readable tables for the
command-line interface. Imports flat, same-folder - no "src." prefix.
"""

from isa_engine import AtmosphereState
from pitot_solver import AirspeedResult
from unit_utils import m_to_ft, pa_to_hpa


def print_atmosphere_table(states: list) -> None:
    """Print a formatted table of one or more AtmosphereState rows."""
    header = (
        f"{'Alt (m)':>10} {'Alt (ft)':>10} {'Temp (K)':>10} {'Temp (C)':>10} "
        f"{'Pressure (hPa)':>15} {'Density (kg/m3)':>17} {'Sound (m/s)':>12} {'Visc (Pa.s)':>14}"
    )
    print(header)
    print("-" * len(header))
    for s in states:
        print(
            f"{s.geometric_altitude_m:10.1f} "
            f"{m_to_ft(s.geometric_altitude_m):10.1f} "
            f"{s.temperature_k:10.2f} "
            f"{s.temperature_k - 273.15:10.2f} "
            f"{pa_to_hpa(s.pressure_pa):15.2f} "
            f"{s.density_kg_m3:17.5f} "
            f"{s.speed_of_sound_mps:12.2f} "
            f"{s.dynamic_viscosity_pas:14.3e}"
        )


def print_single_atmosphere(state: AtmosphereState) -> None:
    """Pretty-print a single atmosphere reading in a labelled block."""
    print("ISA Atmosphere Report")
    print("=" * 40)
    print(f"Geometric altitude : {state.geometric_altitude_m:.1f} m ({m_to_ft(state.geometric_altitude_m):.1f} ft)")
    print(f"Geopotential alt.  : {state.geopotential_altitude_m:.1f} m")
    print(f"Temperature        : {state.temperature_k:.2f} K ({state.temperature_k - 273.15:.2f} C)")
    print(f"Pressure           : {state.pressure_pa:.2f} Pa ({pa_to_hpa(state.pressure_pa):.2f} hPa)")
    print(f"Density            : {state.density_kg_m3:.5f} kg/m^3")
    print(f"Speed of sound     : {state.speed_of_sound_mps:.2f} m/s")
    print(f"Dynamic viscosity  : {state.dynamic_viscosity_pas:.4e} Pa.s")


def print_airspeed_result(result: AirspeedResult) -> None:
    """Pretty-print a CAS/IAS -> TAS conversion result."""
    print("Airspeed Conversion Report")
    print("=" * 40)
    print(f"Model used         : {result.model}")
    print(f"Input IAS/CAS      : {result.ias_kt:.2f} kt")
    print(f"Altitude           : {result.altitude_m:.1f} m")
    print(f"Mach number        : {result.mach:.4f}")
    print(f"True Airspeed (TAS): {result.tas_kt:.2f} kt  ({result.tas_mps:.2f} m/s)")
