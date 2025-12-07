"""Tests for the utils module."""

import unittest

import utils


class TestUtils(unittest.TestCase):
    """Test all functions in the utils module."""

    def test_decimal2Base36_0to35(self):
        """Testing if it works for ids"""
        # Test from 0 to z
        decimals = range(36)
        base36 = [str(num) for num in range(10)]
        base36.extend(list('abcdefghijklmnopqrstuvwxyz'))
        for num_dec, num_36 in zip(decimals, base36, strict=True):
            self.assertEqual(utils.decimal2Base36(num_dec), num_36)

    def test_decimal2Base36_edges(self):
        """Tests if edge cases works."""
        base36s = ['1a', 'a1', 'abcd', '1234', '1ab2', 'a12b', '123a', 'abc1']
        for num_36 in base36s:
            num_dec = int(num_36, 36)
            self.assertEqual(num_36, utils.decimal2Base36(num_dec))
