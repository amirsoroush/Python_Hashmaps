## Introduction

`pyhashmaps` is a fully annotated Python package which has several functional hashmap classes for educational purposes.

All classes support common operations on [ `MutableMapping` ](https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableMapping) type.

Here are the relationships between components of this package:

```mermaid
classDiagram
    class MutableMapping
    class BaseHM

    class OpenAddressingHM {list slots}
    class LinearProbingHM
    class QuadraticProbingHM
    class DoubleHashingHM

    class SeparateChainingHM {list[Chain] slots}
    class DynamicArrayHM {list[DynamicArray] slots}
    class LinkedListHM {list[LinkedList] slots}
    class BSTHM {list[BinarySearchTree] slots}

    MutableMapping <|-- BaseHM
    BaseHM <|-- OpenAddressingHM
    BaseHM <|-- SeparateChainingHM
    OpenAddressingHM <|-- LinearProbingHM
    OpenAddressingHM <|-- QuadraticProbingHM
    OpenAddressingHM <|-- DoubleHashingHM
    SeparateChainingHM <|-- DynamicArrayHM
    SeparateChainingHM <|-- LinkedListHM
    SeparateChainingHM <|-- BSTHM
```

```mermaid
classDiagram
    class Chain {
        <<interface>>
        find()
        insert()
        delete()
    }
    class DynamicArray
    class LinkedList
    class BinarySearchTree

    Chain <|-- DynamicArray
    Chain <|-- LinkedList
    Chain <|-- BinarySearchTree
```

# Requirements

It's tested on Python 3.10 & 3.11.

# Installation

If you have `git` installed:

```none
pip install git+https://github.com/amirsoroush/Python_Hashmaps.git
```

Otherwise:

```none
pip install https://github.com/amirsoroush/Python_Hashmaps/tarball/main
```

# Usage

It has the same interface as the built-in `dict` class.

```python
>>> from pyhashmaps import (
...                     LinearProbingHashMap,
...                     QuadraticProbingHashMap,
...                     DoubleHashingHashMap,
...                     DynamicArrayHashMap,
...                     LinkedListHashMap,
...                     BSTHashMap,
...                     )
>>>
>>> hashmap = LinearProbingHashMap()
>>> hashmap = LinearProbingHashMap[str, int]()
>>> hashmap["a"] = 10
>>> hashmap
LinearProbingHashMap({'a': 10})
>>> hashmap.update({"b": 20, "c": 30})
>>> len(hashmap)
3
>>> for k, v in hashmap.items():
...     print(k, v)
... 
c 30
a 10
b 20
>>> hashmap.clear()
>>> 
```
