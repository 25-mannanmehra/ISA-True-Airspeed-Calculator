"""
test_pitot_solver.py
----------------------
Sanity and regression tests for the CAS/IAS -> TAS conversion logic.
Run from the SAME folder as pitot_solver.py.
"""

import unittest

from pitot_solver import (
    mach_to_tas, tas_compressible, tas_incompressible, tas_to_mach,
)
from validators import InputValidationError


class TestSeaLevelBehaviour(unittest.TestCase):
    def test_tas_equals_ias_at_sea_level_incompressible(self):
        result = tas_incompressible(150, 0)
        self.assertAlmostEqual(result.tas_kt, 150, delta=0.5)

    def test_tas_equals_cas_at_sea_level_compressible(self):
        result = tas_compressible(150, 0)
        self.assertAlmostEqual(result.tas_kt, 150, delta=1.0)


class TestAltitudeEffect(unittest.TestCase):
    def test_tas_greater_than_ias_at_altitude(self):
        result = tas_compressible(150, 8000)
        self.assertGreater(result.tas_kt, 150)

    def test_tas_increases_monotonically_with_altitude(self):
        alts = [0, 2000, 5000, 8000, 11000]
        tas_values = [tas_compressible(200, a).tas_kt for a in alts]
        self.assertEqual(tas_values, sorted(tas_values))


class TestModelConsistency(unittest.TestCase):
    def test_compressible_and_incompressible_agree_at_low_speed_low_alt(self):
        incompressible = tas_incompressible(100, 1000)
        compressible = tas_compressible(100, 1000)
        self.assertAlmostEqual(incompressible.tas_kt, compressible.tas_kt, delta=2.0)


class TestMachConversions(unittest.TestCase):
    def test_mach_to_tas_and_back(self):
        altitude = 10000
        mach = 0.78
        tas = mach_to_tas(mach, altitude)
        recovered_mach = tas_to_mach(tas, altitude)
        self.assertAlmostEqual(mach, recovered_mach, places=6)

    def test_negative_mach_rejected(self):
        with self.assertRaises(ValueError):
            mach_to_tas(-0.5, 10000)


class TestValidation(unittest.TestCase):
    def test_negative_ias_rejected(self):
        with self.assertRaises(InputValidationError):
            tas_compressible(-50, 5000)

    def test_unreasonably_high_ias_rejected(self):
        with self.assertRaises(InputValidationError):
            tas_compressible(5000, 5000)


if __name__ == "__main__":
    unittest.main()
