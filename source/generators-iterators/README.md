# Generators & Iterators

Let's explore generators and iterators in Python using TDD. We'll build various examples that demonstrate lazy evaluation, memory efficiency, and custom iteration patterns.

## The Problem

We want to create a data processing pipeline that can handle large datasets efficiently using generators and custom iterators.

## Red: Write Failing Tests

Let's start with some basic generator and iterator tests:

```python
# generators_test.py
import pytest
from generators import fibonacci_generator, prime_generator, data_processor, custom_range, batch_processor

def test_fibonacci_generator():
    fib = fibonacci_generator(10)
    fib_list = list(fib)
    assert fib_list == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

def test_fibonacci_generator_infinite():
    fib = fibonacci_generator()
    first_ten = [next(fib) for _ in range(10)]
    assert first_ten == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

def test_prime_generator():
    primes = prime_generator(10)
    prime_list = list(primes)
    assert prime_list == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def test_data_processor():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    processor = data_processor(data)
    
    # Test filtering
    filtered = processor.filter(lambda x: x % 2 == 0)
    assert list(filtered) == [2, 4, 6, 8, 10]
    
    # Test mapping
    mapped = processor.map(lambda x: x * 2)
    assert list(mapped) == [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    
    # Test chaining
    result = processor.filter(lambda x: x % 2 == 0).map(lambda x: x * 2)
    assert list(result) == [4, 8, 12, 16, 20]

def test_custom_range():
    range_obj = custom_range(1, 10, 2)
    assert list(range_obj) == [1, 3, 5, 7, 9]
    
    # Test negative step
    range_obj = custom_range(10, 1, -2)
    assert list(range_obj) == [10, 8, 6, 4, 2]

def test_batch_processor():
    data = list(range(20))
    batches = batch_processor(data, batch_size=5)
    batch_list = list(batches)
    
    assert len(batch_list) == 4
    assert batch_list[0] == [0, 1, 2, 3, 4]
    assert batch_list[1] == [5, 6, 7, 8, 9]
    assert batch_list[2] == [10, 11, 12, 13, 14]
    assert batch_list[3] == [15, 16, 17, 18, 19]

def test_generator_expression():
    squares = (x**2 for x in range(5))
    assert list(squares) == [0, 1, 4, 9, 16]

def test_generator_send():
    def echo_generator():
        while True:
            value = yield
            yield value * 2
    
    gen = echo_generator()
    next(gen)  # Start the generator
    result = gen.send(5)
    assert result == 10

def test_generator_throw():
    def error_generator():
        try:
            yield 1
            yield 2
        except ValueError:
            yield "Error handled"
    
    gen = error_generator()
    assert next(gen) == 1
    assert gen.throw(ValueError) == "Error handled"

def test_custom_iterator():
    class NumberIterator:
        def __init__(self, start, end):
            self.start = start
            self.end = end
            self.current = start
        
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.current >= self.end:
                raise StopIteration
            value = self.current
            self.current += 1
            return value
    
    iterator = NumberIterator(1, 5)
    assert list(iterator) == [1, 2, 3, 4]
```

## Green: Write the Minimal Code to Pass

Now let's implement our generators and iterators:

```python
# generators.py
import math
from typing import Iterator, List, Any, Callable, Optional

def fibonacci_generator(n: Optional[int] = None) -> Iterator[int]:
    """
    Generate Fibonacci numbers.
    
    Args:
        n (int, optional): Maximum number of values to generate
        
    Yields:
        int: Fibonacci numbers
    """
    a, b = 0, 1
    count = 0
    
    while n is None or count < n:
        yield a
        a, b = b, a + b
        count += 1

def prime_generator(n: int) -> Iterator[int]:
    """
    Generate prime numbers.
    
    Args:
        n (int): Number of primes to generate
        
    Yields:
        int: Prime numbers
    """
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    
    count = 0
    num = 2
    while count < n:
        if is_prime(num):
            yield num
            count += 1
        num += 1

class DataProcessor:
    """
    A data processor that uses generators for efficient processing.
    """
    
    def __init__(self, data: List[Any]):
        self.data = data
    
    def filter(self, predicate: Callable) -> 'DataProcessor':
        """
        Filter data based on a predicate.
        
        Args:
            predicate: Function that returns True/False
            
        Returns:
            DataProcessor: New processor with filtered data
        """
        filtered_data = (item for item in self.data if predicate(item))
        return DataProcessor(list(filtered_data))
    
    def map(self, func: Callable) -> 'DataProcessor':
        """
        Map a function over the data.
        
        Args:
            func: Function to apply to each item
            
        Returns:
            DataProcessor: New processor with mapped data
        """
        mapped_data = (func(item) for item in self.data)
        return DataProcessor(list(mapped_data))
    
    def __iter__(self):
        return iter(self.data)

def data_processor(data: List[Any]) -> DataProcessor:
    """
    Create a data processor.
    
    Args:
        data: List of data to process
        
    Returns:
        DataProcessor: Processor instance
    """
    return DataProcessor(data)

def custom_range(start: int, stop: int, step: int = 1) -> Iterator[int]:
    """
    Custom range implementation using generators.
    
    Args:
        start: Starting value
        stop: Stopping value
        step: Step size
        
    Yields:
        int: Values in the range
    """
    current = start
    while (step > 0 and current < stop) or (step < 0 and current > stop):
        yield current
        current += step

def batch_processor(data: List[Any], batch_size: int) -> Iterator[List[Any]]:
    """
    Process data in batches.
    
    Args:
        data: Data to process
        batch_size: Size of each batch
        
    Yields:
        List: Batches of data
    """
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

class NumberIterator:
    """
    Custom iterator for numbers.
    """
    
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value
```

## Run the Tests

```bash
pytest generators_test.py -v
```

## Refactor: Improve the Code

Let's improve our code with better error handling and additional features:

```python
# generators.py
import math
from typing import Iterator, List, Any, Callable, Optional, Union
import itertools

def fibonacci_generator(n: Optional[int] = None) -> Iterator[int]:
    """
    Generate Fibonacci numbers.
    
    Args:
        n (int, optional): Maximum number of values to generate
        
    Yields:
        int: Fibonacci numbers
    """
    if n is not None and n < 0:
        raise ValueError("n must be non-negative")
    
    a, b = 0, 1
    count = 0
    
    while n is None or count < n:
        yield a
        a, b = b, a + b
        count += 1

def prime_generator(n: int) -> Iterator[int]:
    """
    Generate prime numbers using Sieve of Eratosthenes.
    
    Args:
        n (int): Number of primes to generate
        
    Yields:
        int: Prime numbers
    """
    if n <= 0:
        return
    
    def is_prime(num):
        if num < 2:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(num)) + 1, 2):
            if num % i == 0:
                return False
        return True
    
    count = 0
    num = 2
    while count < n:
        if is_prime(num):
            yield num
            count += 1
        num += 1

class DataProcessor:
    """
    A data processor that uses generators for efficient processing.
    """
    
    def __init__(self, data: Union[List[Any], Iterator[Any]]):
        self.data = data
    
    def filter(self, predicate: Callable) -> 'DataProcessor':
        """
        Filter data based on a predicate.
        
        Args:
            predicate: Function that returns True/False
            
        Returns:
            DataProcessor: New processor with filtered data
        """
        filtered_data = (item for item in self.data if predicate(item))
        return DataProcessor(filtered_data)
    
    def map(self, func: Callable) -> 'DataProcessor':
        """
        Map a function over the data.
        
        Args:
            func: Function to apply to each item
            
        Returns:
            DataProcessor: New processor with mapped data
        """
        mapped_data = (func(item) for item in self.data)
        return DataProcessor(mapped_data)
    
    def take(self, n: int) -> 'DataProcessor':
        """
        Take only the first n items.
        
        Args:
            n: Number of items to take
            
        Returns:
            DataProcessor: New processor with limited data
        """
        limited_data = itertools.islice(self.data, n)
        return DataProcessor(limited_data)
    
    def skip(self, n: int) -> 'DataProcessor':
        """
        Skip the first n items.
        
        Args:
            n: Number of items to skip
            
        Returns:
            DataProcessor: New processor with skipped data
        """
        skipped_data = itertools.islice(self.data, n, None)
        return DataProcessor(skipped_data)
    
    def __iter__(self):
        return iter(self.data)

def data_processor(data: List[Any]) -> DataProcessor:
    """
    Create a data processor.
    
    Args:
        data: List of data to process
        
    Returns:
        DataProcessor: Processor instance
    """
    return DataProcessor(data)

def custom_range(start: int, stop: int, step: int = 1) -> Iterator[int]:
    """
    Custom range implementation using generators.
    
    Args:
        start: Starting value
        stop: Stopping value
        step: Step size
        
    Yields:
        int: Values in the range
    """
    if step == 0:
        raise ValueError("step cannot be zero")
    
    current = start
    while (step > 0 and current < stop) or (step < 0 and current > stop):
        yield current
        current += step

def batch_processor(data: List[Any], batch_size: int) -> Iterator[List[Any]]:
    """
    Process data in batches.
    
    Args:
        data: Data to process
        batch_size: Size of each batch
        
    Yields:
        List: Batches of data
    """
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

def sliding_window(data: List[Any], window_size: int) -> Iterator[List[Any]]:
    """
    Create sliding windows over data.
    
    Args:
        data: Data to create windows from
        window_size: Size of each window
        
    Yields:
        List: Windows of data
    """
    if window_size <= 0:
        raise ValueError("window_size must be positive")
    
    for i in range(len(data) - window_size + 1):
        yield data[i:i + window_size]

def pairwise(data: List[Any]) -> Iterator[tuple]:
    """
    Create pairs of adjacent elements.
    
    Args:
        data: Data to create pairs from
        
    Yields:
        tuple: Pairs of adjacent elements
    """
    for i in range(len(data) - 1):
        yield (data[i], data[i + 1])

class NumberIterator:
    """
    Custom iterator for numbers.
    """
    
    def __init__(self, start: int, end: int, step: int = 1):
        self.start = start
        self.end = end
        self.step = step
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if (self.step > 0 and self.current >= self.end) or (self.step < 0 and self.current <= self.end):
            raise StopIteration
        value = self.current
        self.current += self.step
        return value

def infinite_counter(start: int = 0, step: int = 1) -> Iterator[int]:
    """
    Infinite counter generator.
    
    Args:
        start: Starting value
        step: Step size
        
    Yields:
        int: Counter values
    """
    current = start
    while True:
        yield current
        current += step

def cycle_generator(data: List[Any]) -> Iterator[Any]:
    """
    Cycle through data infinitely.
    
    Args:
        data: Data to cycle through
        
    Yields:
        Any: Cycled data
    """
    while True:
        for item in data:
            yield item
```

## Advanced Examples

Let's add some more sophisticated generator patterns:

```python
# generators_test.py (additional tests)
def test_sliding_window():
    data = [1, 2, 3, 4, 5]
    windows = sliding_window(data, 3)
    window_list = list(windows)
    
    assert window_list == [[1, 2, 3], [2, 3, 4], [3, 4, 5]]

def test_pairwise():
    data = [1, 2, 3, 4, 5]
    pairs = pairwise(data)
    pair_list = list(pairs)
    
    assert pair_list == [(1, 2), (2, 3), (3, 4), (4, 5)]

def test_infinite_counter():
    counter = infinite_counter(5, 2)
    values = [next(counter) for _ in range(5)]
    assert values == [5, 7, 9, 11, 13]

def test_cycle_generator():
    data = [1, 2, 3]
    cycle = cycle_generator(data)
    values = [next(cycle) for _ in range(7)]
    assert values == [1, 2, 3, 1, 2, 3, 1]

def test_generator_send():
    def echo_generator():
        while True:
            value = yield
            yield value * 2
    
    gen = echo_generator()
    next(gen)  # Start the generator
    result = gen.send(5)
    assert result == 10

def test_generator_throw():
    def error_generator():
        try:
            yield 1
            yield 2
        except ValueError:
            yield "Error handled"
    
    gen = error_generator()
    assert next(gen) == 1
    assert gen.throw(ValueError) == "Error handled"

def test_data_processor_chaining():
    data = list(range(10))
    processor = data_processor(data)
    
    result = (processor
              .filter(lambda x: x % 2 == 0)
              .map(lambda x: x * 2)
              .take(3))
    
    assert list(result) == [0, 4, 8]
```

## What We've Learned

1. **Generators**: Functions that yield values instead of returning them
2. **Iterators**: Objects that implement the iterator protocol
3. **Lazy Evaluation**: Computing values only when needed
4. **Memory Efficiency**: Processing large datasets without loading everything into memory
5. **Generator Expressions**: Concise way to create generators

## Exercises

1. Create a generator that produces all permutations of a list
2. Implement a generator that reads a file line by line
3. Build a generator that produces all combinations of a list
4. Create a generator that implements a sliding window over data

## Key Concepts

- **Generators**: Functions that yield values lazily
- **Iterators**: Objects that can be iterated over
- **Lazy Evaluation**: Computing values on demand
- **Memory Efficiency**: Processing large datasets efficiently
- **Generator Expressions**: Concise generator syntax

