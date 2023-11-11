from abc import abstractmethod
from collections.abc import Hashable, Iterable, Iterator, Mapping, MutableMapping
from dataclasses import dataclass
from typing import Any, Generic, Protocol, TypeVar


class Comparable(Hashable, Protocol):
    """Protocol for annotating comparable and Hashable types."""

    def __lt__(self, other: Any) -> bool:
        ...


K = TypeVar("K", bound=Hashable)
Comp_K = TypeVar("Comp_K", bound=Comparable)
V = TypeVar("V")
HashMapArgument = Mapping[K, V] | Iterable[tuple[K, V]]


def is_same(k1: K, k2: K) -> bool:
    """
    Check whether two keys are the same or not.

    It's consistent with how Python itself compares keys in hashtables.
    """
    return k1 is k2 or k1 == k2


@dataclass(slots=True)
class HashEntry(Generic[K, V]):
    hash_value: int
    key: K
    value: V


class Chain(Protocol[K, V]):
    """
    A protocol for classes which are intended to be used as the underlying
    data structure for storing objects in 'separate chaining' method.
    """

    def __iter__(self) -> Iterator[HashEntry[K, V]]:
        ...

    def __len__(self) -> int:
        ...

    def find(self, key: K) -> HashEntry[K, V]:
        ...

    def insert(self, item: HashEntry[K, V]) -> None:
        ...

    def delete(self, key: K) -> None:
        ...

    def append_at_end(self, item: HashEntry[K, V]) -> None:
        """
        Append the `item` at the end.

        `.append_at_end()` is a faster route than `.insert()` to insert items when
        we no longer have to check the existing items - when all items are different.
        This is the case when we resize the hashtable.
        """
        ...


class BaseHashMap(MutableMapping[K, V]):
    """
    An abstract base class which is the parent of all classes implementing hashtables
    using either methods(open addressing, separete chaining)
    """

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
        """
        Hash function used for hashing keys.

        For simplicity, the built-in `hash()` function is used.
        """
        return hash(key)

    @abstractmethod
    def _increase_size(self) -> None:
        """
        increases the size of the hash table based on the criteria
        specified by subclasses.
        """
        pass
