# type: ignore
import unittest

from src.pyhashmaps.separate_chaining import (
    BSTHashMap,
    DynamicArrayHashMap,
    LinkedListHashMap,
)

from .base_test_file import BaseTestCase


class TestSeparateChainingHashmap(BaseTestCase):
    cls = None

    def test_creation_valid(self):
        self.cls()
        self.cls(initial_size=100)
        self.cls(initial_size=100, max_chain_size=5)
        self.cls(max_chain_size=5)

    def test_creation_invalid(self):
        self.assertRaises(ValueError, self.cls, initial_size=-2)

    def test_resize(self):
        class A:
            __hash__ = lambda self: 0

        hashmap = self.cls(initial_size=5, max_chain_size=3)
        self.assertEqual(hashmap.size, 5)
        for i in range(3):
            hashmap[A()] = i
        self.assertEqual(hashmap.size, 5 * 2)


class TestDynamicArrayHashMap(TestSeparateChainingHashmap, unittest.TestCase):
    cls = DynamicArrayHashMap


class TestLinkedListHashMap(TestSeparateChainingHashmap, unittest.TestCase):
    cls = LinkedListHashMap


class TestBSTHashMap(TestSeparateChainingHashmap, unittest.TestCase):
    cls = BSTHashMap

    # This is an override since `BSTHashMap` needs `HashEntr`s to be comparable.
    def test_resize(self):
        class A:
            def __hash__(self) -> int:
                return 0

            def __lt__(self, item) -> bool:
                return True

        hashmap = self.cls(initial_size=5, max_chain_size=3)
        self.assertEqual(hashmap.size, 5)
        for i in range(3):
            hashmap[A()] = i
        self.assertEqual(hashmap.size, 5 * 2)
