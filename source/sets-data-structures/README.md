# Sets & Data Structures

Learn advanced Python data structures through Test-Driven Development.

## Overview

This chapter covers Python's built-in data structures beyond basic lists and dictionaries:

- **Sets**: Unordered collections of unique elements
- **Tuples & Named Tuples**: Immutable sequences and structured data
- **Counter**: Frequency counting and analysis
- **Deque**: Double-ended queues for efficient operations
- **DefaultDict**: Dictionaries with automatic default values

## Learning Objectives

By the end of this chapter, you will:

- Understand when and how to use different data structures
- Master set operations (union, intersection, difference)
- Create and use named tuples for structured data
- Implement efficient queues and stacks using deque
- Use Counter for frequency analysis
- Apply defaultdict for grouping and counting operations

## Getting Started

1. **Run the tests** to see what needs to be implemented:
   ```bash
   pytest -v
   ```

2. **Implement the methods** in `data_structures.py` to make the tests pass

3. **Follow TDD cycle**: Red → Green → Refactor

## Key Concepts

### Sets
```python
# Create sets
numbers = {1, 2, 3, 4}
unique_items = set([1, 2, 2, 3])  # {1, 2, 3}

# Set operations
set1 = {1, 2, 3}
set2 = {2, 3, 4}

intersection = set1 & set2      # {2, 3}
union = set1 | set2             # {1, 2, 3, 4}
difference = set1 - set2        # {1}
symmetric_diff = set1 ^ set2    # {1, 4}
```

### Named Tuples
```python
from collections import namedtuple

Person = namedtuple('Person', ['name', 'age', 'job'])
alice = Person('Alice', 30, 'Engineer')

print(alice.name)  # Alice
print(alice.age)   # 30
```

### Counter
```python
from collections import Counter

# Count frequencies
counter = Counter(['a', 'b', 'a', 'c', 'b', 'a'])
print(counter)  # Counter({'a': 3, 'b': 2, 'c': 1})

# Most common items
print(counter.most_common(2))  # [('a', 3), ('b', 2)]
```

### Deque (Double-ended Queue)
```python
from collections import deque

# Create queue
queue = deque()

# Queue operations (FIFO)
queue.append('first')     # Add to right
queue.append('second')
item = queue.popleft()    # Remove from left

# Stack operations (LIFO)
stack = deque()
stack.append('bottom')    # Push
stack.append('top')
item = stack.pop()        # Pop from right
```

### DefaultDict
```python
from collections import defaultdict

# Group items
groups = defaultdict(list)
for word in ['cat', 'dog', 'ant']:
    groups[len(word)].append(word)

print(dict(groups))  # {3: ['cat', 'dog', 'ant']}
```

## Test Structure

The tests are organized into classes:

- `TestSets`: Basic set operations and mathematical set theory
- `TestTuples`: Named tuple creation and immutability
- `TestCounter`: Frequency counting and analysis
- `TestDeque`: Queue and stack operations
- `TestDefaultDict`: Grouping and automatic defaults
- `TestAdvancedOperations`: Complex data structure patterns

## Implementation Tips

1. **Sets are unordered**: Don't rely on element order
2. **Use set operators**: `&`, `|`, `-`, `^` for cleaner code
3. **Named tuples are immutable**: Perfect for data that shouldn't change
4. **Deque is efficient**: O(1) operations at both ends
5. **Counter supports math**: Add, subtract, and compare counters
6. **DefaultDict prevents KeyError**: Automatically creates missing keys

## Common Patterns

### Removing Duplicates
```python
def remove_duplicates(items):
    return list(set(items))  # Note: loses order
```

### Finding Duplicates
```python
def find_duplicates(items):
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return duplicates
```

### Grouping Data
```python
def group_by_key(items, key_func):
    groups = defaultdict(list)
    for item in items:
        key = key_func(item)
        groups[key].append(item)
    return dict(groups)
```

## Performance Notes

- **Set membership**: O(1) average case
- **Set operations**: Generally O(min(len(s1), len(s2)))
- **Deque append/pop**: O(1) at both ends
- **Counter operations**: O(n) for counting, O(1) for access
- **DefaultDict**: Same as regular dict, but with automatic key creation

## Next Steps

After mastering these data structures:

1. Explore more collections: `OrderedDict`, `ChainMap`
2. Learn about `heapq` for priority queues
3. Study `bisect` for maintaining sorted lists
4. Investigate third-party libraries like `sortedcontainers`

## Resources

- [Python Collections Documentation](https://docs.python.org/3/library/collections.html)
- [Set Operations Guide](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)
- [Data Structures Tutorial](https://docs.python.org/3/tutorial/datastructures.html)
