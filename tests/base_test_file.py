# type: ignore
# ruff: noqa
import unittest
from typing import TYPE_CHECKING

from src.pyhashmaps.base import BaseHashMap

base = unittest.TestCase if TYPE_CHECKING else object


class BaseTestCase(base):
    cls: BaseHashMap

    def test_constructor(self):
        hashmap1 = self.cls({"a": 10, "b": 20, "c": 30})
        hashmap2 = self.cls([("a", 10), ("b", 20), ("c", 30)])
        self.assertEqual(hashmap1.items(), {("a", 10), ("b", 20), ("c", 30)})
        self.assertEqual(hashmap2.items(), {("a", 10), ("b", 20), ("c", 30)})

    def test_add_item(self):
        hashmap = self.cls()
        hashmap["foo"] = 10
        hashmap["bar"] = 20
        self.assertEqual(hashmap["foo"], 10)
        self.assertEqual(hashmap["bar"], 20)
        with self.assertRaises(TypeError):
            hashmap[{}] = 10

    def test_not_existed_item(self):
        self.assertIsNone(self.cls().get("foo"))

    def test_delete_item(self):
        hashmap = self.cls()
        hashmap["foo"] = 10
        self.assertEqual(hashmap["foo"], 10)
        del hashmap["foo"]
        self.assertIsNone(hashmap.get("foo"))

    def test_len(self):
        hashmap = self.cls(initial_size=15)
        for i in range(10):
            hashmap[str(i)] = i
        self.assertEqual(len(hashmap), 10)
        del hashmap["4"]
        self.assertEqual(len(hashmap), 9)
        hashmap["5"] = None
        self.assertEqual(len(hashmap), 9)
        del hashmap["9"]
        self.assertEqual(len(hashmap), 8)
        del hashmap["0"]
        self.assertEqual(len(hashmap), 7)
        hashmap.clear()
        self.assertEqual(len(hashmap), 0)

    def test_same_key(self):
        hashmap = self.cls()
        hashmap["foo"] = 10
        self.assertEqual(hashmap["foo"], 10)
        hashmap["foo"] = 20
        self.assertEqual(hashmap["foo"], 20)
        self.assertEqual(len(hashmap), 1)

    def test_contain(self):
        hashmap = self.cls()
        hashmap["foo"] = 10
        self.assertTrue("foo" in hashmap)
        self.assertFalse("bar" in hashmap)

    def test_iteration(self):
        hashmap = self.cls()
        for i in range(10):
            hashmap[i] = i * 2
        self.assertEqual(set(hashmap), set(range(10)))
        self.assertEqual(set(hashmap.values()), set(i * 2 for i in range(10)))

    def test_large_number_of_items(self):
        hashmap = self.cls()
        n = 1000
        for i in range(n):
            hashmap[f"_{i}_"] = i
        self.assertEqual(len(hashmap), n)
        for i in range(0, n, 2):
            del hashmap[f"_{i}_"]
        self.assertEqual(len(hashmap), n // 2)

    def test_repr(self):
        hashmap = self.cls()
        class_name = hashmap.__class__.__name__
        self.assertEqual(repr(hashmap), f"{class_name}({{}})")
        hashmap["A"] = 30
        self.assertEqual(repr(hashmap), f"{class_name}({{'A': 30}})")

    def test_equality(self):
        hashmap = self.cls({"a": 10, "b": 20, "c": 30})
        dictionary = {"a": 10, "b": 20, "c": 30}
        self.assertEqual(hashmap, dictionary)

    def test_accidental_same_slot(self):
        """
        hash functions can accidentally collide in a same bucket. This test
        reveals this situation specifically in LinearProbingHashMap and
        QuadraticProbingHashMap.
        """

        class A:
            def __init__(self, var):
                self.var = var

            def __lt__(self, other):
                if isinstance(other, A):
                    return self.var < other.var
                return NotImplemented

            def __hash__(self) -> int:
                return hash(self.var)

            def __eq__(self, other: object) -> bool:
                if isinstance(other, A):
                    return self.var == other.var
                return NotImplemented

        hashmap = self.cls(initial_size=10)

        obj = A(11)
        # The A(11) object is placed into the second slot in the ten slots.
        hashmap[obj] = "something1"

        # A(21) also wants to go to the second slot in the ten slots.
        obj.var = 21
        hashmap[obj] = "something2"
        self.assertEqual(len(hashmap), 2)
