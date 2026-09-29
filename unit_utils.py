"""
unit_utils.py
-------------
Small, dependency-free unit conversion helpers shared by the rest of the
project. No imports from other project files.
"""

FEET_PER_METER = 3.280839895
KELVIN_OFFSET = 273.15
KNOTS_PER_MPS = 1.9438444924


def m_to_ft(meters: float) -> float:
    """Convert metres to feet."""
    return meters * FEET_PER_METER


def ft_to_m(feet: float) -> float:
    """Convert feet to metres."""
    return feet / FEET_PER_METER


def celsius_to_kelvin(celsius: float) -> float:
    """Convert degrees Celsius to Kelvin."""
    return celsius + KELVIN_OFFSET


def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to degrees Celsius."""
    return kelvin - KELVIN_OFFSET


def mps_to_kt(mps: float) -> float:
    """Convert metres/second to knots."""
    return mps * KNOTS_PER_MPS


def kt_to_mps(knots: float) -> float:
    """Convert knots to metres/second."""
    return knots / KNOTS_PER_MPS


def pa_to_hpa(pascal: float) -> float:
    """Convert Pascals to hectopascals (millibars)."""
    return pascal / 100.0


def pa_to_inhg(pascal: float) -> float:
    """Convert Pascals to inches of mercury."""
    return pascal * 0.0002953
