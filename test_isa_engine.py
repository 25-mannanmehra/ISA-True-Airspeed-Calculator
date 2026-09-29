"""
test_isa_engine.py
-------------------
Validates isa_engine.py against published ICAO Standard Atmosphere
reference values. Run from the SAME folder as isa_engine.py:

    python test_isa_engine.py
or
    python -m unittest test_isa_engine.py -v
"""

import unittest

from isa_engine import get_atmosphere, get_atmosphere_profile
from validators import InputValidationError


class TestSeaLevel(unittest.TestCase):
    def test_sea_level_conditions(self):
        state = get_atmosphere(0)
        self.assertAlmostEqual(state.temperature_k, 288.15, places=2)
        self.assertAlmostEqual(state.pressure_pa, 101325.0, delta=1.0)
        self.assertAlmostEqual(state.density_kg_m3, 1.225, places=3)
        self.assertAlmostEqual(state.speed_of_sound_mps, 340.29, delta=0.1)


class TestKnownAltitudes(unittest.TestCase):
    def test_11000m_tropopause(self):
        state = get_atmosphere(11000, is_geopotential=True)
        self.assertAlmostEqual(state.temperature_k, 216.65, delta=0.05)
        self.assertAlmostEqual(state.pressure_pa, 22632, delta=50)
        self.assertAlmostEqual(state.density_kg_m3, 0.3639, delta=0.002)

    def test_20000m_stratosphere(self):
        state = get_atmosphere(20000, is_geopotential=True)
        self.assertAlmostEqual(state.temperature_k, 216.65, delta=0.05)
        self.assertAlmostEqual(state.pressure_pa, 5474.9, delta=20)

    def test_5000m_general_aviation_cruise(self):
        state = get_atmosphere(5000)
        self.assertAlmostEqual(state.temperature_k, 255.65, delta=0.1)
        self.assertTrue(0.6 < state.density_kg_m3 < 0.8)


class TestMonotonicity(unittest.TestCase):
    def test_temperature_decreases_in_troposphere(self):
        low = get_atmosphere(0)
        high = get_atmosphere(10000)
        self.assertLess(high.temperature_k, low.temperature_k)

    def test_pressure_always_decreases_with_altitude(self):
        profile = get_atmosphere_profile(0, 40000, 2000)
        pressures = [s.pressure_pa for s in profile]
        self.assertEqual(pressures, sorted(pressures, reverse=True))

    def test_density_always_decreases_with_altitude(self):
        profile = get_atmosphere_profile(0, 40000, 2000)
        densities = [s.density_kg_m3 for s in profile]
        self.assertEqual(densities, sorted(densities, reverse=True))


class TestValidation(unittest.TestCase):
    def test_negative_altitude_rejected(self):
        with self.assertRaises(InputValidationError):
            get_atmosphere(-500)

    def test_altitude_above_supported_range_rejected(self):
        with self.assertRaises(InputValidationError):
            get_atmosphere(60000)

    def test_non_numeric_altitude_rejected(self):
        with self.assertRaises(InputValidationError):
            get_atmosphere("not-a-number")


class TestGeopotentialConversion(unittest.TestCase):
    def test_round_trip_conversion(self):
        from isa_engine import geometric_to_geopotential, geopotential_to_geometric
        geometric = 10000.0
        geopotential = geometric_to_geopotential(geometric)
        back = geopotential_to_geometric(geopotential)
        self.assertAlmostEqual(geometric, back, places=6)


if __name__ == "__main__":
    unittest.main()
