# type: ignore
import unittest
from typing import TYPE_CHECKING

from src.pyhashmaps.base import BaseHashMap

base = unittest.TestCase if TYPE_CHECKING else object


class BaseTestCase(base):
    cls: BaseHashMap

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
