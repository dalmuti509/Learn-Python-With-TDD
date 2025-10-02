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

