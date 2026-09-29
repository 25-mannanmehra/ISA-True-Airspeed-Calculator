# Project Statement

## Project Title
**ISA & True Airspeed Calculator**

## Problem Statement
An aircraft's airspeed indicator does not show how fast the aircraft is actually moving through the air. It measures impact pressure, which depends on air density. As altitude increases, air becomes thinner, so the same indicated airspeed corresponds to a higher true airspeed. Students, pilots and engineers therefore need a reliable way to (1) determine atmospheric conditions at a given altitude and (2) convert indicated/calibrated airspeed into true airspeed and Mach number.

Doing this by hand is slow and error-prone. It requires layered atmosphere equations, geopotential altitude conversion, and compressible-flow formulas. Existing tools are often closed, lack explanations, or do not let learners see how the results are produced.

## Objective
Build an open, well-tested, easy-to-read software tool that:

1. Computes the ICAO International Standard Atmosphere from 0 to 51 km.
2. Converts IAS/CAS to TAS and Mach number using both a simple and a full compressible model.
3. Presents results through a command-line interface, graphical plots and an interactive web page.
4. Validates input and verifies its own accuracy against published reference values.

## Scope
**In scope**
- Temperature, pressure, density, speed of sound and dynamic viscosity for the standard atmosphere up to 51 km
- Geometric and geopotential altitude handling
- Incompressible and isentropic compressible IAS/CAS → TAS conversion, plus Mach ↔ TAS
- Unit conversions (metres/feet, °C/K, knots/m·s⁻¹, Pa/hPa/inHg)
- CLI, PNG plots, standalone HTML calculator, unit tests

**Out of scope**
- Non-standard days (ISA deviation) and non-standard pressure settings
- Instrument/position error correction, wind, humidity
- Supersonic flow and altitudes above 51 km

## Target Users
- Aerospace and aviation students learning atmosphere and airspeed concepts
- Pilots and flight-planning enthusiasts needing quick TAS/Mach estimates
- Developers or educators wanting a clear reference implementation

## High-Level Features
| # | Feature | Delivered by |
|---|---|---|
| 1 | Standard atmosphere model (5 layers) | `isa_engine.py`, `constants.py` |
| 2 | Altitude conversion (geometric ↔ geopotential) | `isa_engine.py` |
| 3 | IAS/CAS → TAS (two models) and Mach conversions | `pitot_solver.py` |
| 4 | Input validation and custom errors | `validators.py` |
| 5 | Unit conversion helpers | `unit_utils.py` |
| 6 | Formatted console output | `cli_reporter.py` |
| 7 | CLI with subcommands and interactive menu | `main.py` |
| 8 | Profile and TAS plots | `visualizer.py` |
| 9 | Browser-based calculator with live chart | `isa_tas_website.html` |
| 10 | Automated tests | `test_*.py` |

## Approach and Methodology
- **Modular design:** each concern (constants, physics, validation, units, reporting, plotting, CLI) lives in its own module with flat, same-folder imports.
- **Standard physics:** layer equations from ICAO/ISO 2533; ideal gas law for density; Sutherland's law for viscosity; isentropic pitot-static relations for compressible airspeed.
- **Immutable results:** `AtmosphereState` and `AirspeedResult` are frozen dataclasses, so results cannot be changed accidentally.
- **Verification:** unit tests compare outputs to known ISA values (sea level, 11 km, 20 km, 5 km), check monotonic trends, model agreement at low speed, round-trip conversions and error handling.
- **Two front ends, one model:** the web calculator reimplements the same equations in JavaScript so it works offline with no server.

## Expected Outcome
A working, documented calculator that returns accurate ISA properties and true airspeed for any valid altitude and airspeed, with clear output, visual plots and a passing test suite.

## Technologies Used
- Python 3 (standard library: `math`, `dataclasses`, `argparse`, `unittest`)
- Matplotlib (plotting)
- HTML, CSS and JavaScript (web calculator, SVG chart)

## Limitations
- Standard-day conditions only
- IAS is assumed equal to CAS
- Subsonic compressible model
- Upper altitude limit of 51 km

## Future Enhancements
- ISA deviation and QNH inputs
- Equivalent airspeed (EAS), pressure altitude and density altitude
- Supersonic pitot relations
- Data export (CSV) and pip packaging
