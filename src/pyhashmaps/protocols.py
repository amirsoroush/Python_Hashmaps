from collections.abc import Iterator
from typing import Protocol

from .base import HashEntry, K, V


class Chain(Protocol[K, V]):
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

    # `.append_at_end()` is a faster route than `.insert()` to insert items
    # since we no longer have to check the existing items.
    # All items are different.
    def append_at_end(self, item: HashEntry[K, V]) -> None:
        ...
