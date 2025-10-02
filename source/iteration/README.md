# Iteration

Let's explore iteration in Python using TDD. We'll build various functions that demonstrate different types of loops and iteration patterns.

## The Problem

We want to create functions that work with sequences of data using different iteration techniques.

## Red: Write Failing Tests

Let's start with some basic iteration functions:

```python
# iteration_test.py
import pytest
from iteration import sum_numbers, find_max, count_occurrences, reverse_list

def test_sum_numbers():
    numbers = [1, 2, 3, 4, 5]
    result = sum_numbers(numbers)
    assert result == 15

def test_sum_empty_list():
    result = sum_numbers([])
    assert result == 0

def test_find_max():
    numbers = [3, 7, 2, 9, 1]
    result = find_max(numbers)
    assert result == 9

def test_find_max_empty_list():
    with pytest.raises(ValueError):
        find_max([])

def test_count_occurrences():
    numbers = [1, 2, 2, 3, 2, 4]
    result = count_occurrences(numbers, 2)
    assert result == 3

def test_reverse_list():
    numbers = [1, 2, 3, 4, 5]
    result = reverse_list(numbers)
    assert result == [5, 4, 3, 2, 1]
```

## Green: Write the Minimal Code to Pass

Now let's implement our iteration functions:

```python
# iteration.py
def sum_numbers(numbers):
    """
    Sum all numbers in a list.
    
    Args:
        numbers (list): List of numbers to sum
        
    Returns:
        int: Sum of all numbers
    """
    total = 0
    for number in numbers:
        total += number
    return total

def find_max(numbers):
    """
    Find the maximum number in a list.
    
    Args:
        numbers (list): List of numbers
        
    Returns:
        int: Maximum number
        
    Raises:
        ValueError: If the list is empty
    """
    if not numbers:
        raise ValueError("Cannot find max of empty list")
    
    max_num = numbers[0]
    for number in numbers[1:]:
        if number > max_num:
            max_num = number
    return max_num

def count_occurrences(numbers, target):
    """
    Count how many times a target number appears in a list.
    
    Args:
        numbers (list): List of numbers to search
        target (int): Number to count
        
    Returns:
        int: Number of occurrences
    """
    count = 0
    for number in numbers:
        if number == target:
            count += 1
    return count

def reverse_list(numbers):
    """
    Reverse a list of numbers.
    
    Args:
        numbers (list): List to reverse
        
    Returns:
        list: Reversed list
    """
    result = []
    for i in range(len(numbers) - 1, -1, -1):
        result.append(numbers[i])
    return result
```

## Run the Tests

```bash
pytest iteration_test.py -v
```

## Refactor: Improve the Code

Let's improve our code with better Python idioms:

```python
# iteration.py
def sum_numbers(numbers):
    """
    Sum all numbers in a list.
    
    Args:
        numbers (list): List of numbers to sum
        
    Returns:
        int: Sum of all numbers
    """
    return sum(numbers)

def find_max(numbers):
    """
    Find the maximum number in a list.
    
    Args:
        numbers (list): List of numbers
        
    Returns:
        int: Maximum number
        
    Raises:
        ValueError: If the list is empty
    """
    if not numbers:
        raise ValueError("Cannot find max of empty list")
    
    return max(numbers)

def count_occurrences(numbers, target):
    """
    Count how many times a target number appears in a list.
    
    Args:
        numbers (list): List of numbers to search
        target (int): Number to count
        
    Returns:
        int: Number of occurrences
    """
    return numbers.count(target)

def reverse_list(numbers):
    """
    Reverse a list of numbers.
    
    Args:
        numbers (list): List to reverse
        
    Returns:
        list: Reversed list
    """
    return numbers[::-1]
```

## Advanced Examples

Let's add some more complex iteration examples:

```python
# iteration_test.py (additional tests)
def test_filter_even_numbers():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = filter_even_numbers(numbers)
    assert result == [2, 4, 6, 8, 10]

def test_map_square():
    numbers = [1, 2, 3, 4, 5]
    result = map_square(numbers)
    assert result == [1, 4, 9, 16, 25]

def test_find_duplicates():
    numbers = [1, 2, 2, 3, 4, 4, 5]
    result = find_duplicates(numbers)
    assert result == [2, 4]

def test_group_by_parity():
    numbers = [1, 2, 3, 4, 5, 6]
    result = group_by_parity(numbers)
    assert result == {'odd': [1, 3, 5], 'even': [2, 4, 6]}
```

```python
# iteration.py (additional functions)
def filter_even_numbers(numbers):
    """
    Filter out odd numbers, keeping only even numbers.
    
    Args:
        numbers (list): List of numbers to filter
        
    Returns:
        list: List of even numbers
    """
    return [num for num in numbers if num % 2 == 0]

def map_square(numbers):
    """
    Square each number in a list.
    
    Args:
        numbers (list): List of numbers to square
        
    Returns:
        list: List of squared numbers
    """
    return [num ** 2 for num in numbers]

def find_duplicates(numbers):
    """
    Find duplicate numbers in a list.
    
    Args:
        numbers (list): List of numbers to check
        
    Returns:
        list: List of duplicate numbers
    """
    seen = set()
    duplicates = set()
    
    for num in numbers:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
    
    return list(duplicates)

def group_by_parity(numbers):
    """
    Group numbers by whether they are odd or even.
    
    Args:
        numbers (list): List of numbers to group
        
    Returns:
        dict: Dictionary with 'odd' and 'even' keys
    """
    result = {'odd': [], 'even': []}
    
    for num in numbers:
        if num % 2 == 0:
            result['even'].append(num)
        else:
            result['odd'].append(num)
    
    return result
```

## What We've Learned

1. **For Loops**: Basic iteration over sequences
2. **List Comprehensions**: Pythonic way to create lists
3. **Range Function**: Generating sequences of numbers
4. **Error Handling**: Dealing with edge cases like empty lists
5. **Data Transformation**: Mapping, filtering, and grouping data

## Exercises

1. Write a function to find the second largest number in a list
2. Write a function to check if a list is sorted
3. Write a function to merge two sorted lists
4. Write a function to find the longest increasing subsequence

## Key Concepts

- **Iteration**: Processing each element in a sequence
- **List Comprehensions**: Concise way to create lists
- **Error Handling**: Dealing with edge cases
- **Data Processing**: Transforming and filtering data

