"""test_unit_utils.py - round-trip and reference-value checks for unit_utils.py"""

import unittest

from unit_utils import (
    celsius_to_kelvin, ft_to_m, kelvin_to_celsius, kt_to_mps, m_to_ft, mps_to_kt,
)


class TestLengthConversions(unittest.TestCase):
    def test_m_to_ft_known_value(self):
        self.assertAlmostEqual(m_to_ft(1000), 3280.84, places=1)

    def test_round_trip(self):
        self.assertAlmostEqual(ft_to_m(m_to_ft(12345.6)), 12345.6, places=4)


class TestTemperatureConversions(unittest.TestCase):
    def test_celsius_to_kelvin(self):
        self.assertAlmostEqual(celsius_to_kelvin(15), 288.15, places=2)

    def test_round_trip(self):
        self.assertAlmostEqual(kelvin_to_celsius(celsius_to_kelvin(-40)), -40, places=6)


class TestSpeedConversions(unittest.TestCase):
    def test_kt_to_mps_known_value(self):
        self.assertAlmostEqual(kt_to_mps(1), 0.5144, places=3)

    def test_round_trip(self):
        self.assertAlmostEqual(mps_to_kt(kt_to_mps(250)), 250, places=4)


if __name__ == "__main__":
    unittest.main()
