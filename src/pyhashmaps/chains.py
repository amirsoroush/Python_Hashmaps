from collections.abc import Generator, Iterator
from dataclasses import dataclass, field
from typing import Generic, Optional, cast

from .base import Comp_K, HashEntry, K, V, is_same
from .protocols import Chain


@dataclass(slots=True)
class LinkedListNode(Generic[K, V]):
    data: HashEntry[K, V]
    next: Optional["LinkedListNode[K, V]"] = field(
        default=None, repr=False, compare=False
    )


@dataclass(slots=True)
class BSTNode(Generic[Comp_K, V]):
    data: HashEntry[Comp_K, V]
    left: Optional["BSTNode[Comp_K, V]"] = field(
        default=None, repr=False, compare=False
    )
    right: Optional["BSTNode[Comp_K, V]"] = field(
        default=None, repr=False, compare=False
    )
    parent: Optional["BSTNode[Comp_K, V]"] = field(
        default=None, repr=False, compare=False
    )


class DynamicArray(Chain[K, V]):
    def __init__(self) -> None:
        self.lst: list[HashEntry[K, V]] = []

    def __len__(self) -> int:
        return len(self.lst)

    def __iter__(self) -> Iterator[HashEntry[K, V]]:
        yield from self.lst

    def find(self, key: K) -> HashEntry[K, V]:
        for e in self.lst:
            if is_same(e.key, key):
                return e
        raise KeyError(repr(key))

    def insert(self, item: HashEntry[K, V]) -> None:
        for idx, e in enumerate(self.lst):
            if is_same(item.key, e.key):
                self.lst[idx] = item
                break
        else:
            self.lst.append(item)

    def delete(self, key: K) -> None:
        for idx, e in enumerate(self.lst):
            if is_same(key, e.key):
                del self.lst[idx]
                return
        raise KeyError(repr(key))

    def append_at_end(self, item: HashEntry[K, V]) -> None:
        self.lst.append(item)


class LinkedList(Chain[K, V]):
    def __init__(self) -> None:
        self.head: LinkedListNode[K, V] | None = None
        self.tail: LinkedListNode[K, V] | None = None
        self.count: int = 0

    def __len__(self) -> int:
        return self.count

    def __iter__(self) -> Iterator[HashEntry[K, V]]:
        current = self.head
        while current:
            yield current.data
            current = current.next

    def find(self, key: K) -> HashEntry[K, V]:
        current_node = self.head
        while current_node:
            if is_same(current_node.data.key, key):
                return current_node.data
            current_node = current_node.next
        raise KeyError(repr(key))

    def insert(self, item: HashEntry[K, V]) -> None:
        current_node = self.head
        while current_node:
            if is_same(current_node.data.key, item.key):
                current_node.data = item
                break
            current_node = current_node.next
        else:
            self.insert_tail(item)

    def delete(self, key: K) -> None:
        current_node = self.head
        previous_node = self.head
        while current_node is not None:
            if is_same(current_node.data.key, key):
                if current_node is self.head:
                    self.head = current_node.next
                else:
                    previous_node = cast(LinkedListNode[K, V], previous_node)
                    previous_node.next = current_node.next
                self.count -= 1
                break
            previous_node = current_node
            current_node = current_node.next
        else:
            raise KeyError(repr(key))

    def insert_tail(self, data: HashEntry[K, V]) -> None:
        node = LinkedListNode(data)
        if self.tail:
            self.tail.next = node
            self.tail = node
        else:
            self.head = self.tail = node
        self.count += 1

    def append_at_end(self, item: HashEntry[K, V]) -> None:
        self.insert_tail(item)


class BinarySearchTree(Chain[Comp_K, V]):
    def __init__(self) -> None:
        self.root: BSTNode[Comp_K, V] | None = None
        self.count: int = 0

    def __len__(self) -> int:
        return self.count

    def __iter__(self) -> Iterator[HashEntry[Comp_K, V]]:
        yield from self.inorder_traversal(self.root)

    def find(self, key: Comp_K) -> HashEntry[Comp_K, V]:
        return self.find_node(key).data

    def insert(self, item: HashEntry[Comp_K, V]) -> None:
        new_node = BSTNode(item)

        if self.root is None:
            self.root = new_node
            self.count += 1
            return

        current_node = self.root
        while True:
            if is_same(item.key, current_node.data.key):
                current_node.data = item
                return
            if item.key < current_node.data.key:
                if current_node.left is None:
                    current_node.left = new_node
                    new_node.parent = current_node
                    self.count += 1
                    return
                current_node = current_node.left
            else:
                if current_node.right is None:
                    current_node.right = new_node
                    new_node.parent = current_node
                    self.count += 1
                    return
                current_node = current_node.right

    def delete(self, key: Comp_K) -> None:
        node = self.find_node(key)

        # Node has no children
        if node.left is None and node.right is None:
            self.reassign_nodes(node, None)

        # Node has one right child
        elif node.left is None:
            self.reassign_nodes(node, node.right)

        # Node has one left child
        elif node.right is None:
            self.reassign_nodes(node, node.left)

        # Node has both left and right children
        else:
            temp_node = self.find_biggest_node(node.left)
            self.delete(temp_node.data.key)
            node.data = temp_node.data

    def inorder_traversal(
        self, node: BSTNode[Comp_K, V] | None
    ) -> Generator[HashEntry[Comp_K, V], None, None]:
        if node is None:
            return
        yield from self.inorder_traversal(node.left)
        yield node.data
        yield from self.inorder_traversal(node.right)

    def find_node(self, key: Comp_K) -> BSTNode[Comp_K, V]:
        current_node = self.root
        while current_node is not None:
            if is_same(current_node.data.key, key):
                return current_node
            if key < current_node.data.key:
                current_node = current_node.left
            elif key > current_node.data.key:
                current_node = current_node.right

        raise KeyError(repr(key))

    def is_right_child(self, node: BSTNode[Comp_K, V]) -> bool:
        node.parent = cast(BSTNode[Comp_K, V], node.parent)
        if node.parent.right is not None:
            return is_same(node.parent.right.data.key, node.data.key)
        return False

    def reassign_nodes(
        self, node: BSTNode[Comp_K, V], child: BSTNode[Comp_K, V] | None
    ) -> None:
        if child is not None:
            child.parent = node.parent
        if node.parent is not None:
            if self.is_right_child(node):
                node.parent.right = child
            else:
                node.parent.left = child
        else:
            self.root = child
        self.count -= 1

    def find_biggest_node(self, node: BSTNode[Comp_K, V]) -> BSTNode[Comp_K, V]:
        while node.right is not None:
            node = node.right
        return node

    def append_at_end(self, item: HashEntry[Comp_K, V]) -> None:
        # Delegates to `insert` since there is no faster way of doing it except
        # removing the `is_same` from `.insert` which is a micro optimization.
        self.insert(item)
