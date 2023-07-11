from abc import abstractmethod
from collections.abc import Hashable, MutableMapping
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar


class Comparable(Hashable, Protocol):
    """Protocol for annotating comparable and Hashable types."""

    def __lt__(self, other: "Comparable") -> bool:
        ...


K = TypeVar("K", bound=Hashable)
Comp_K = TypeVar("Comp_K", bound=Comparable)
V = TypeVar("V")


def is_same(k1: K, k2: K) -> bool:
    """Check whether two keys are the same"""
    return k1 is k2 or k1 == k2


@dataclass(slots=True)
class HashEntry(Generic[K, V]):
    hash_value: int
    key: K
    value: V


class BaseHashMap(MutableMapping[K, V]):
    def __init__(self, initial_size: int) -> None:
        if not (isinstance(initial_size, int) and initial_size > 0):
            raise ValueError("initial_size must be a positive integer.")
        self.size = initial_size
        self._len = 0

    def __len__(self) -> int:
        return self._len

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        items = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"{class_name}({{{items}}})"

    def _hash_func(self, key: K) -> int:
        return hash(key)

    @abstractmethod
    def _increase_size(self) -> None:
        pass
