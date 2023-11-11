# type: ignore
# ruff: noqa
import unittest

from src.pyhashmaps.open_addressing import (
    DoubleHashingHashMap,
    LinearProbingHashMap,
    QuadraticProbingHashMap,
)

from .base_test_file import BaseTestCase


class TestOpenAddressingHashMap(BaseTestCase):
    cls = None

    def test_creation_valid(self):
        self.cls()
        self.cls(initial_size=100)
        self.cls(resize_factor=0.7)
        self.cls(initial_size=30, resize_factor=0.6)

    def test_creation_invalid(self):
        self.assertRaises(ValueError, self.cls, initial_size=-2)
        self.assertRaises(ValueError, self.cls, initial_size=0)
        self.assertRaises(ValueError, self.cls, resize_factor=1.1)

    def test_resize(self):
        hashmap = self.cls(initial_size=10, resize_factor=0.8)
        self.assertEqual(hashmap.size, 10)
        for i in range(8):
            hashmap[i] = None
        self.assertEqual(hashmap.size, 20)
        self.assertEqual(len(hashmap), 8)


class TestLinearProbingHashMap(TestOpenAddressingHashMap, unittest.TestCase):
    cls = LinearProbingHashMap


class TestQuadraticProbingHashMap(TestOpenAddressingHashMap, unittest.TestCase):
    cls = QuadraticProbingHashMap


class TestDoubleHashingHashMap(TestOpenAddressingHashMap, unittest.TestCase):
    cls = DoubleHashingHashMap
