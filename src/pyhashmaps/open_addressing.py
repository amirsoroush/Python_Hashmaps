from abc import abstractmethod
from collections.abc import Generator, Iterator
from enum import Enum

from .base import BaseHashMap, HashEntry, HashMapArgument, K, V, is_same


class NotExist(Enum):
    empty = 0
    deleted = 1

    def __str__(self) -> str:
        return self.name.upper()

    __repr__ = __str__


EMPTY = NotExist.empty
DELETED = NotExist.deleted


class OpenAddressingHashMap(BaseHashMap[K, V]):
    def __init__(
        self,
        mapping_or_iterable: HashMapArgument[K, V] | None = None,
        /,
        *,
        initial_size: int = 64,
        resize_factor: float = 0.7,
    ) -> None:
        super().__init__(initial_size)

        if not 0.0 < resize_factor < 1.0:
            raise ValueError("resize_factor must be between 0 and 1.")
        self.resize_factor = resize_factor
        self.slots: list[HashEntry[K, V] | NotExist] = [EMPTY] * self.size
        if mapping_or_iterable is not None:
            self.update(mapping_or_iterable)

    def __iter__(self) -> Iterator[K]:
        for item in self.slots:
            if isinstance(item, HashEntry):
                yield item.key

    def __getitem__(self, key: K) -> V:
        prob_sequence_gen = self._probing_sequence(key, self.size)
        while True:
            idx = next(prob_sequence_gen)
            slot = self.slots[idx]
            if slot is EMPTY:
                raise KeyError(repr(key))
            if isinstance(slot, HashEntry) and is_same(slot.key, key):
                return slot.value

    def __setitem__(self, key: K, value: V) -> None:
        h = self._hash_func(key)
        hash_entry = HashEntry(h, key, value)

        prob_sequence_gen = self._probing_sequence(key, self.size)
        while True:
            idx = next(prob_sequence_gen)
            slot = self.slots[idx]

            if isinstance(slot, HashEntry):
                if is_same(slot.key, key):
                    slot.value = value
                    break
            elif slot is EMPTY:
                self.slots[idx] = hash_entry
                self._len += 1

                if self._need_increase():
                    self._increase_size()
                break

    def __delitem__(self, key: K) -> None:
        prob_sequence_gen = self._probing_sequence(key, self.size)
        while True:
            idx = next(prob_sequence_gen)
            slot = self.slots[idx]
            if slot is EMPTY:
                raise KeyError(repr(key))
            if isinstance(slot, HashEntry) and is_same(slot.key, key):
                self.slots[idx] = DELETED
                break

        self._len -= 1

    def _need_increase(self) -> bool:
        return len(self) / self.size >= self.resize_factor

    def _increase_size(self) -> None:
        new_size = self.size * 2
        new_slots: list[HashEntry[K, V] | NotExist] = [EMPTY] * new_size

        for item in self.slots:
            if isinstance(item, HashEntry):
                for idx in self._probing_sequence(item.key, new_size):
                    slot = new_slots[idx]
                    if slot is EMPTY:
                        new_slots[idx] = item
                        break

        self.slots = new_slots
        self.size = new_size

    @abstractmethod
    def _probing_sequence(self, key: K, size: int) -> Generator[int, None, None]:
        yield 0


class LinearProbingHashMap(OpenAddressingHashMap[K, V]):
    def _probing_sequence(self, key: K, size: int) -> Generator[int, None, None]:
        h = self._hash_func(key)
        idx = h % size
        while True:
            yield idx % size
            idx += 1


class QuadraticProbingHashMap(OpenAddressingHashMap[K, V]):
    def _probing_sequence(self, key: K, size: int) -> Generator[int, None, None]:
        h = self._hash_func(key)
        idx = h % size
        i = 0
        while True:
            yield idx % size
            idx += i**2
            i += 1


class DoubleHashingHashMap(OpenAddressingHashMap[K, V]):
    def __init__(
        self,
        mapping_or_iterable: HashMapArgument[K, V] | None = None,
        /,
        *,
        initial_size: int = 64,
        resize_factor: float = 0.7,
        prime_number: int = 7,
    ) -> None:
        self._prime = prime_number
        super().__init__(
            mapping_or_iterable, initial_size=initial_size, resize_factor=resize_factor
        )

    def _hash_func2(self, key: K) -> int:
        return self._prime - (self._hash_func(key) % self._prime)

    def _probing_sequence(self, key: K, size: int) -> Generator[int, None, None]:
        h1 = self._hash_func(key)
        h2 = self._hash_func2(key)
        i = 0
        while True:
            yield ((h1 % size) + (h2 % size) + i) % size
            i += 1
