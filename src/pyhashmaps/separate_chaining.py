from collections.abc import Iterator

from .base import BaseHashMap, Chain, HashEntry, K, V
from .chains import BinarySearchTree, DynamicArray, LinkedList


class SeparateChainingHashMap(BaseHashMap[K, V]):
    chain: type[Chain[K, V]]

    def __init__(self, initial_size: int = 40, max_chain_size: int = 5) -> None:
        super().__init__(initial_size)
        self._max_chain_size = max_chain_size
        self.slots: list[Chain[K, V]] = [self.chain() for _ in range(self.size)]

    def __iter__(self) -> Iterator[K]:
        for chain in self.slots:
            for item in chain:
                yield item.key

    def __getitem__(self, key: K) -> V:
        h = self._hash_func(key)
        idx = h % self.size

        chain = self.slots[idx]
        return chain.find(key).value

    def __setitem__(self, key: K, value: V) -> None:
        h = self._hash_func(key)
        idx = h % self.size
        hash_entry = HashEntry(h, key, value)

        chain = self.slots[idx]

        chain_length_before = len(chain)
        chain.insert(hash_entry)
        chain_length_after = len(chain)

        if chain_length_before != chain_length_after:
            self._len += 1

            if self._need_increase(chain_length_after):
                self._increase_size()

    def __delitem__(self, key: K) -> None:
        h = self._hash_func(key)
        idx = h % self.size

        chain = self.slots[idx]

        chain_length_before = len(chain)
        chain.delete(key)
        chain_length_after = len(chain)

        if chain_length_before != chain_length_after:
            self._len -= 1

    def _need_increase(self, chain_size: int) -> bool:
        return chain_size >= self._max_chain_size

    def _increase_size(self) -> None:
        new_size = self.size * 2
        new_slots = [self.chain() for _ in range(new_size)]

        for chain in self.slots:
            for item in chain:
                idx = item.hash_value % new_size
                new_slots[idx].append_at_end(item)

        self.slots = new_slots
        self.size = new_size


class DynamicArrayHashMap(SeparateChainingHashMap[K, V]):
    chain: type[Chain[K, V]] = DynamicArray


class LinkedListHashMap(SeparateChainingHashMap[K, V]):
    chain: type[Chain[K, V]] = LinkedList


class BSTHashMap(SeparateChainingHashMap[K, V]):
    chain: type[Chain[K, V]] = BinarySearchTree
