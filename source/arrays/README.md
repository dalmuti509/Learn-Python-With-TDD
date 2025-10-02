# Arrays and Lists

Let's explore working with arrays and lists in Python using TDD. We'll build various functions that demonstrate list manipulation and operations.

## The Problem

We want to create functions that work with lists, including basic operations like adding, removing, and searching elements.

## Red: Write Failing Tests

Let's start with some basic list operations:

```python
# list_operations_test.py
import pytest
from list_operations import ListOperations

def test_append():
    ops = ListOperations()
    result = ops.append([1, 2, 3], 4)
    assert result == [1, 2, 3, 4]

def test_prepend():
    ops = ListOperations()
    result = ops.prepend([2, 3, 4], 1)
    assert result == [1, 2, 3, 4]

def test_remove_first():
    ops = ListOperations()
    result = ops.remove_first([1, 2, 3, 4])
    assert result == [2, 3, 4]

def test_remove_last():
    ops = ListOperations()
    result = ops.remove_last([1, 2, 3, 4])
    assert result == [1, 2, 3]

def test_find_index():
    ops = ListOperations()
    result = ops.find_index([1, 2, 3, 4], 3)
    assert result == 2

def test_find_index_not_found():
    ops = ListOperations()
    result = ops.find_index([1, 2, 3, 4], 5)
    assert result == -1

def test_slice_list():
    ops = ListOperations()
    result = ops.slice_list([1, 2, 3, 4, 5], 1, 4)
    assert result == [2, 3, 4]

def test_concatenate():
    ops = ListOperations()
    result = ops.concatenate([1, 2], [3, 4])
    assert result == [1, 2, 3, 4]
```

## Green: Write the Minimal Code to Pass

Now let's implement our list operations:

```python
# list_operations.py
class ListOperations:
    """
    A class that provides various list operations.
    """
    
    def append(self, lst, item):
        """
        Append an item to the end of a list.
        
        Args:
            lst (list): The list to append to
            item: The item to append
            
        Returns:
            list: New list with item appended
        """
        return lst + [item]
    
    def prepend(self, lst, item):
        """
        Prepend an item to the beginning of a list.
        
        Args:
            lst (list): The list to prepend to
            item: The item to prepend
            
        Returns:
            list: New list with item prepended
        """
        return [item] + lst
    
    def remove_first(self, lst):
        """
        Remove the first element from a list.
        
        Args:
            lst (list): The list to remove from
            
        Returns:
            list: New list without first element
        """
        if not lst:
            return []
        return lst[1:]
    
    def remove_last(self, lst):
        """
        Remove the last element from a list.
        
        Args:
            lst (list): The list to remove from
            
        Returns:
            list: New list without last element
        """
        if not lst:
            return []
        return lst[:-1]
    
    def find_index(self, lst, item):
        """
        Find the index of an item in a list.
        
        Args:
            lst (list): The list to search
            item: The item to find
            
        Returns:
            int: Index of item, or -1 if not found
        """
        try:
            return lst.index(item)
        except ValueError:
            return -1
    
    def slice_list(self, lst, start, end):
        """
        Slice a list from start to end index.
        
        Args:
            lst (list): The list to slice
            start (int): Start index
            end (int): End index
            
        Returns:
            list: Sliced list
        """
        return lst[start:end]
    
    def concatenate(self, lst1, lst2):
        """
        Concatenate two lists.
        
        Args:
            lst1 (list): First list
            lst2 (list): Second list
            
        Returns:
            list: Concatenated list
        """
        return lst1 + lst2
```

## Run the Tests

```bash
pytest list_operations_test.py -v
```

## Refactor: Improve the Code

Let's improve our code with better error handling and documentation:

```python
# list_operations.py
class ListOperations:
    """
    A class that provides various list operations.
    """
    
    def append(self, lst, item):
        """
        Append an item to the end of a list.
        
        Args:
            lst (list): The list to append to
            item: The item to append
            
        Returns:
            list: New list with item appended
        """
        if not isinstance(lst, list):
            raise TypeError("First argument must be a list")
        return lst + [item]
    
    def prepend(self, lst, item):
        """
        Prepend an item to the beginning of a list.
        
        Args:
            lst (list): The list to prepend to
            item: The item to prepend
            
        Returns:
            list: New list with item prepended
        """
        if not isinstance(lst, list):
            raise TypeError("First argument must be a list")
        return [item] + lst
    
    def remove_first(self, lst):
        """
        Remove the first element from a list.
        
        Args:
            lst (list): The list to remove from
            
        Returns:
            list: New list without first element
        """
        if not isinstance(lst, list):
            raise TypeError("Argument must be a list")
        if not lst:
            return []
        return lst[1:]
    
    def remove_last(self, lst):
        """
        Remove the last element from a list.
        
        Args:
            lst (list): The list to remove from
            
        Returns:
            list: New list without last element
        """
        if not isinstance(lst, list):
            raise TypeError("Argument must be a list")
        if not lst:
            return []
        return lst[:-1]
    
    def find_index(self, lst, item):
        """
        Find the index of an item in a list.
        
        Args:
            lst (list): The list to search
            item: The item to find
            
        Returns:
            int: Index of item, or -1 if not found
        """
        if not isinstance(lst, list):
            raise TypeError("First argument must be a list")
        try:
            return lst.index(item)
        except ValueError:
            return -1
    
    def slice_list(self, lst, start, end):
        """
        Slice a list from start to end index.
        
        Args:
            lst (list): The list to slice
            start (int): Start index
            end (int): End index
            
        Returns:
            list: Sliced list
        """
        if not isinstance(lst, list):
            raise TypeError("First argument must be a list")
        if not isinstance(start, int) or not isinstance(end, int):
            raise TypeError("Start and end must be integers")
        return lst[start:end]
    
    def concatenate(self, lst1, lst2):
        """
        Concatenate two lists.
        
        Args:
            lst1 (list): First list
            lst2 (list): Second list
            
        Returns:
            list: Concatenated list
        """
        if not isinstance(lst1, list) or not isinstance(lst2, list):
            raise TypeError("Both arguments must be lists")
        return lst1 + lst2
```

## Advanced Examples

Let's add some more complex list operations:

```python
# list_operations_test.py (additional tests)
def test_remove_duplicates():
    ops = ListOperations()
    result = ops.remove_duplicates([1, 2, 2, 3, 4, 4, 5])
    assert result == [1, 2, 3, 4, 5]

def test_sort_list():
    ops = ListOperations()
    result = ops.sort_list([3, 1, 4, 1, 5, 9, 2, 6])
    assert result == [1, 1, 2, 3, 4, 5, 6, 9]

def test_reverse_list():
    ops = ListOperations()
    result = ops.reverse_list([1, 2, 3, 4, 5])
    assert result == [5, 4, 3, 2, 1]

def test_intersection():
    ops = ListOperations()
    result = ops.intersection([1, 2, 3, 4], [3, 4, 5, 6])
    assert result == [3, 4]

def test_union():
    ops = ListOperations()
    result = ops.union([1, 2, 3], [3, 4, 5])
    assert result == [1, 2, 3, 4, 5]
```

```python
# list_operations.py (additional methods)
def remove_duplicates(self, lst):
    """
    Remove duplicate elements from a list.
    
    Args:
        lst (list): The list to remove duplicates from
        
    Returns:
        list: List without duplicates
    """
    if not isinstance(lst, list):
        raise TypeError("Argument must be a list")
    
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def sort_list(self, lst):
    """
    Sort a list in ascending order.
    
    Args:
        lst (list): The list to sort
        
    Returns:
        list: Sorted list
    """
    if not isinstance(lst, list):
        raise TypeError("Argument must be a list")
    return sorted(lst)

def reverse_list(self, lst):
    """
    Reverse a list.
    
    Args:
        lst (list): The list to reverse
        
    Returns:
        list: Reversed list
    """
    if not isinstance(lst, list):
        raise TypeError("Argument must be a list")
    return lst[::-1]

def intersection(self, lst1, lst2):
    """
    Find the intersection of two lists.
    
    Args:
        lst1 (list): First list
        lst2 (list): Second list
        
    Returns:
        list: List of common elements
    """
    if not isinstance(lst1, list) or not isinstance(lst2, list):
        raise TypeError("Both arguments must be lists")
    
    set1 = set(lst1)
    set2 = set(lst2)
    return list(set1.intersection(set2))

def union(self, lst1, lst2):
    """
    Find the union of two lists.
    
    Args:
        lst1 (list): First list
        lst2 (list): Second list
        
    Returns:
        list: List of all unique elements
    """
    if not isinstance(lst1, list) or not isinstance(lst2, list):
        raise TypeError("Both arguments must be lists")
    
    set1 = set(lst1)
    set2 = set(lst2)
    return list(set1.union(set2))
```

## What We've Learned

1. **List Operations**: Basic list manipulation functions
2. **Error Handling**: Type checking and validation
3. **Set Operations**: Using sets for efficient operations
4. **List Comprehensions**: Pythonic ways to create lists
5. **Data Structures**: Understanding list behavior

## Exercises

1. Write a function to find the median of a list
2. Write a function to rotate a list by n positions
3. Write a function to find the longest common subsequence
4. Write a function to implement a simple stack using lists

## Key Concepts

- **List Manipulation**: Adding, removing, and modifying elements
- **Searching**: Finding elements in lists
- **Sorting**: Organizing data
- **Set Operations**: Working with unique elements
- **Error Handling**: Validating inputs and handling edge cases

