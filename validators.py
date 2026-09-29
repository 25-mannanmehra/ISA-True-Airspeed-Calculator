"""
validators.py
-------------
Centralised input validation and the project's custom exception types.
Imports `constants` directly (flat, same-folder import) - no "src." prefix.
"""

from constants import MAX_SUPPORTED_ALTITUDE_M, MIN_SUPPORTED_ALTITUDE_M


class InputValidationError(ValueError):
    """Raised when a user-supplied value is outside an accepted range."""


def validate_altitude_m(altitude_m: float) -> float:
    """
    Ensure an altitude (in metres, geometric) is a real number within the
    range the ISA model in this project supports (0 - 51 km).
    """
    try:
        altitude_m = float(altitude_m)
    except (TypeError, ValueError) as exc:
        raise InputValidationError(f"Altitude must be numeric, got {altitude_m!r}") from exc

    if altitude_m != altitude_m:  # NaN check without importing math
        raise InputValidationError("Altitude cannot be NaN")

    if not (MIN_SUPPORTED_ALTITUDE_M <= altitude_m <= MAX_SUPPORTED_ALTITUDE_M):
        raise InputValidationError(
            f"Altitude {altitude_m} m is out of supported range "
            f"[{MIN_SUPPORTED_ALTITUDE_M}, {MAX_SUPPORTED_ALTITUDE_M}] m"
        )
    return altitude_m


def validate_airspeed(speed: float, name: str = "airspeed", max_value: float = 1000.0) -> float:
    """
    Ensure an airspeed value (knots or m/s, caller decides units) is a
    positive, finite, physically reasonable number.
    """
    try:
        speed = float(speed)
    except (TypeError, ValueError) as exc:
        raise InputValidationError(f"{name} must be numeric, got {speed!r}") from exc

    if speed != speed:
        raise InputValidationError(f"{name} cannot be NaN")

    if speed < 0:
        raise InputValidationError(f"{name} cannot be negative, got {speed}")

    if speed > max_value:
        raise InputValidationError(f"{name} of {speed} exceeds sanity limit of {max_value}")

    return speed


def validate_positive(value: float, name: str) -> float:
    """Ensure a value is strictly positive (used for pressures, densities)."""
    try:
        value = float(value)
    except (TypeError, ValueError) as exc:
        raise InputValidationError(f"{name} must be numeric, got {value!r}") from exc

    if value <= 0:
        raise InputValidationError(f"{name} must be > 0, got {value}")
    return value
