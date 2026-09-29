# ISA & True Airspeed Calculator

A Python project that computes the **ICAO International Standard Atmosphere (ISA)** from sea level to 51 km and converts **indicated/calibrated airspeed (IAS/CAS)** into **true airspeed (TAS)** and **Mach number**. It ships with a command-line interface, matplotlib plots, a unit-test suite, and a standalone browser calculator.

---

## Features

- **ISA model (0 – 51 km):** temperature, pressure, density, speed of sound and dynamic viscosity (Sutherland's law), covering the troposphere, tropopause, both stratosphere layers and the stratopause.
- **Geometric ↔ geopotential altitude conversion**, so you can enter the altitude an altimeter/GPS reports or a geopotential height directly.
- **Two airspeed models:**
  - *Incompressible:* `TAS = CAS · √(ρ₀ / ρ)` (good at low speed / low altitude).
  - *Compressible (isentropic):* CAS → impact pressure → Mach → TAS, the physics behind a real airspeed indicator.
- **Mach ↔ TAS helpers.**
- **CLI** with subcommands, plus an interactive menu when run with no arguments.
- **Plots** (PNG): T/P/ρ vs altitude, and TAS vs altitude for a constant IAS.
- **Input validation** with a custom `InputValidationError`.
- **Web calculator** (`isa_tas_website.html`): a single-file, offline-capable page that mirrors the same physics in JavaScript.
- **Unit tests** against published ISA reference values.

---

## Project structure

All Python modules live in the **same folder** (flat imports, no package prefix).

| File | Purpose |
|---|---|
| `main.py` | CLI entry point (argparse subcommands + interactive menu) |
| `constants.py` | Physical constants and the ISA layer table |
| `isa_engine.py` | ISA calculations, `AtmosphereState` dataclass, altitude conversions |
| `pitot_solver.py` | CAS/IAS → TAS, Mach conversions, `AirspeedResult` dataclass |
| `validators.py` | Input validation and `InputValidationError` |
| `unit_utils.py` | Unit conversions (m/ft, °C/K, kt/m·s⁻¹, Pa/hPa/inHg) |
| `cli_reporter.py` | Formatted console tables and reports |
| `visualizer.py` | Matplotlib plotting (headless `Agg` backend) |
| `isa_tas_website.html` | Standalone browser version of the calculator |
| `test_isa_engine.py` | Tests for the atmosphere model |
| `test_pitot_solver.py` | Tests for airspeed conversions |
| `test_unit_utils.py` | Tests for unit conversions |

---

## Requirements

- Python 3.8+
- `matplotlib` (only needed for the `plot` and `plot-tas` commands)

```bash
pip install matplotlib
```

The core calculator and tests use only the standard library.

---

## Usage

Run from inside the project folder:

```bash
cd isa_tas_calculator
```

### Atmosphere at one altitude

```bash
python main.py atmosphere --altitude 5000
```

### Atmosphere table over a range

```bash
python main.py profile --start 0 --end 20000 --step 1000
```

### IAS/CAS → True Airspeed

```bash
python main.py tas --ias 250 --altitude 10000 --model compressible
python main.py tas --ias 150 --altitude 2000 --model incompressible
```

### Plots (saved to `output/`)

```bash
python main.py plot --start 0 --end 30000 --step 500
python main.py plot-tas --ias 250 --end 15000
```

### Interactive menu

Running `python main.py` with no arguments (for example via an editor's Run button) opens a simple numbered menu.

### Web version

Open `isa_tas_website.html` in any modern browser. Use the altitude and IAS controls to see live atmosphere values, TAS/Mach, and a density-vs-altitude chart.

### Use as a library

```python
from isa_engine import get_atmosphere
from pitot_solver import tas_compressible

state = get_atmosphere(8000)                 # geometric altitude, metres
print(state.temperature_k, state.pressure_pa, state.density_kg_m3)

result = tas_compressible(250, 8000)         # 250 kt CAS at 8000 m
print(result.mach, result.tas_kt)
```

---

## Running the tests

```bash
python -m unittest discover -v
```

Or run a single file:

```bash
python test_isa_engine.py
```

The tests check sea-level values, the 11 km and 20 km reference points, monotonic behaviour of pressure/density/TAS, model agreement at low speed, round-trip conversions, and rejection of invalid input.

---

## How it works

**ISA layers** (base geopotential height, base temperature, lapse rate):

| Layer | Base (m) | Base T (K) | Lapse (K/m) |
|---|---|---|---|
| Troposphere | 0 | 288.15 | −0.0065 |
| Tropopause | 11,000 | 216.65 | 0 |
| Stratosphere I | 20,000 | 216.65 | +0.0010 |
| Stratosphere II | 32,000 | 228.65 | +0.0028 |
| Stratopause | 47,000 | 270.65 | 0 |

- Gradient layer: `T = Tb + L(h − hb)`, `P = Pb (T/Tb)^(−g₀/(R·L))`
- Isothermal layer: `P = Pb · exp(−g₀(h − hb)/(R·Tb))`
- Density: `ρ = P / (R·T)`; speed of sound: `a = √(γ R T)`
- Viscosity: Sutherland's law
- Compressible airspeed: `qc = P₀[(1 + 0.2(CAS/a₀)²)^3.5 − 1]`, `M = √(5[(qc/P + 1)^(2/7) − 1])`, `TAS = M · a`

---

## Input limits

- Altitude: 0 – 51,000 m
- IAS/CAS: 0 – 700 kt
- Invalid, negative, NaN or out-of-range values raise `InputValidationError`; the CLI prints a clean error message instead of a traceback.

---

## Limitations

- Standard-day atmosphere only (no temperature deviation such as ISA+15).
- IAS is treated as CAS: no instrument or position error correction.
- The compressible model assumes subsonic flow (no shock-wave/Rayleigh pitot correction).
- No wind, humidity or non-standard pressure (QNH) handling.
- Model ends at 51 km.

---

## Possible future work

- ISA deviation (ΔT) and non-standard sea-level pressure inputs
- Equivalent airspeed (EAS) and pressure/density altitude
- Supersonic pitot relations
- CSV export and a packaged `pip`-installable module

---

## License

Provided for educational use. Add your preferred license here.
