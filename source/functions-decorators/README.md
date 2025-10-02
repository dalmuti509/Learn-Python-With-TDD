# Functions & Decorators

Let's explore functions and decorators in Python using TDD. We'll build various examples that demonstrate function composition, decorators, closures, and higher-order functions.

## The Problem

We want to create a caching system that can be applied to any function using decorators, along with logging and timing functionality.

## Red: Write Failing Tests

Let's start with some basic function and decorator tests:

```python
# functions_test.py
import pytest
import time
from functions import fibonacci, memoize, timing, logging_decorator, retry, validate_input

def test_fibonacci_basic():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(2) == 1
    assert fibonacci(3) == 2
    assert fibonacci(4) == 3
    assert fibonacci(5) == 5

def test_fibonacci_large():
    assert fibonacci(10) == 55
    assert fibonacci(20) == 6765

def test_memoize_decorator():
    @memoize
    def slow_function(n):
        time.sleep(0.1)  # Simulate slow operation
        return n * 2
    
    # First call should be slow
    start = time.time()
    result1 = slow_function(5)
    first_duration = time.time() - start
    
    # Second call should be fast (cached)
    start = time.time()
    result2 = slow_function(5)
    second_duration = time.time() - start
    
    assert result1 == result2 == 10
    assert second_duration < first_duration

def test_timing_decorator():
    @timing
    def test_function():
        time.sleep(0.1)
        return "done"
    
    result = test_function()
    assert result == "done"

def test_logging_decorator():
    @logging_decorator
    def add_numbers(a, b):
        return a + b
    
    result = add_numbers(3, 4)
    assert result == 7

def test_retry_decorator():
    call_count = 0
    
    @retry(max_attempts=3)
    def flaky_function():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("Temporary failure")
        return "success"
    
    result = flaky_function()
    assert result == "success"
    assert call_count == 3

def test_validate_input_decorator():
    @validate_input(int, int)
    def multiply(a, b):
        return a * b
    
    assert multiply(3, 4) == 12
    
    with pytest.raises(TypeError):
        multiply("3", 4)

def test_function_composition():
    def add_one(x):
        return x + 1
    
    def multiply_by_two(x):
        return x * 2
    
    def compose(f, g):
        return lambda x: f(g(x))
    
    composed = compose(add_one, multiply_by_two)
    assert composed(5) == 11  # (5 * 2) + 1

def test_closure():
    def create_multiplier(factor):
        def multiplier(x):
            return x * factor
        return multiplier
    
    double = create_multiplier(2)
    triple = create_multiplier(3)
    
    assert double(5) == 10
    assert triple(5) == 15
```

## Green: Write the Minimal Code to Pass

Now let's implement our functions and decorators:

```python
# functions.py
import time
import functools
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fibonacci(n):
    """
    Calculate the nth Fibonacci number.
    
    Args:
        n (int): The position in the Fibonacci sequence
        
    Returns:
        int: The nth Fibonacci number
    """
    if n < 0:
        raise ValueError("Fibonacci sequence is not defined for negative numbers")
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def memoize(func):
    """
    Memoization decorator that caches function results.
    
    Args:
        func: The function to memoize
        
    Returns:
        function: The memoized function
    """
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    return wrapper

def timing(func):
    """
    Timing decorator that logs function execution time.
    
    Args:
        func: The function to time
        
    Returns:
        function: The wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    
    return wrapper

def logging_decorator(func):
    """
    Logging decorator that logs function calls and results.
    
    Args:
        func: The function to log
        
    Returns:
        function: The wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} returned {result}")
        return result
    
    return wrapper

def retry(max_attempts=3, delay=1):
    """
    Retry decorator that retries a function on failure.
    
    Args:
        max_attempts (int): Maximum number of attempts
        delay (float): Delay between attempts in seconds
        
    Returns:
        function: The retry decorator
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        logger.error(f"All {max_attempts} attempts failed")
            
            raise last_exception
        
        return wrapper
    return decorator

def validate_input(*types):
    """
    Input validation decorator.
    
    Args:
        *types: Expected types for positional arguments
        
    Returns:
        function: The validation decorator
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) != len(types):
                raise TypeError(f"Expected {len(types)} arguments, got {len(args)}")
            
            for i, (arg, expected_type) in enumerate(zip(args, types)):
                if not isinstance(arg, expected_type):
                    raise TypeError(f"Argument {i} must be {expected_type.__name__}, got {type(arg).__name__}")
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator
```

## Run the Tests

```bash
pytest functions_test.py -v
```

## Refactor: Improve the Code

Let's improve our code with better error handling and additional features:

```python
# functions.py
import time
import functools
import logging
from typing import Callable, Any, Type, Union, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number using memoization.
    
    Args:
        n (int): The position in the Fibonacci sequence
        
    Returns:
        int: The nth Fibonacci number
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Fibonacci sequence is not defined for negative numbers")
    if n <= 1:
        return n
    
    # Use memoization for efficiency
    return _fibonacci_memoized(n, {})

def _fibonacci_memoized(n: int, memo: dict) -> int:
    """Helper function for memoized Fibonacci calculation."""
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    
    memo[n] = _fibonacci_memoized(n - 1, memo) + _fibonacci_memoized(n - 2, memo)
    return memo[n]

def memoize(func: Callable) -> Callable:
    """
    Memoization decorator that caches function results.
    
    Args:
        func: The function to memoize
        
    Returns:
        function: The memoized function
    """
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a cache key from arguments
        key = str(args) + str(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    # Add cache management methods
    wrapper.cache_clear = lambda: cache.clear()
    wrapper.cache_info = lambda: f"Cache size: {len(cache)}"
    
    return wrapper

def timing(func: Callable) -> Callable:
    """
    Timing decorator that logs function execution time.
    
    Args:
        func: The function to time
        
    Returns:
        function: The wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            end = time.time()
            logger.info(f"{func.__name__} took {end - start:.4f} seconds")
            return result
        except Exception as e:
            end = time.time()
            logger.error(f"{func.__name__} failed after {end - start:.4f} seconds: {e}")
            raise
    
    return wrapper

def logging_decorator(func: Callable) -> Callable:
    """
    Logging decorator that logs function calls and results.
    
    Args:
        func: The function to log
        
    Returns:
        function: The wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} returned {result}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised {type(e).__name__}: {e}")
            raise
    
    return wrapper

def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """
    Retry decorator that retries a function on failure.
    
    Args:
        max_attempts (int): Maximum number of attempts
        delay (float): Delay between attempts in seconds
        exceptions (tuple): Exception types to catch and retry
        
    Returns:
        function: The retry decorator
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        logger.error(f"All {max_attempts} attempts failed")
            
            raise last_exception
        
        return wrapper
    return decorator

def validate_input(*types: Type) -> Callable:
    """
    Input validation decorator.
    
    Args:
        *types: Expected types for positional arguments
        
    Returns:
        function: The validation decorator
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) != len(types):
                raise TypeError(f"Expected {len(types)} arguments, got {len(args)}")
            
            for i, (arg, expected_type) in enumerate(zip(args, types)):
                if not isinstance(arg, expected_type):
                    raise TypeError(f"Argument {i} must be {expected_type.__name__}, got {type(arg).__name__}")
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

def count_calls(func: Callable) -> Callable:
    """
    Decorator that counts function calls.
    
    Args:
        func: The function to count calls for
        
    Returns:
        function: The wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        return func(*args, **kwargs)
    
    wrapper.call_count = 0
    return wrapper

def rate_limit(calls_per_second: float = 1.0):
    """
    Rate limiting decorator.
    
    Args:
        calls_per_second (float): Maximum calls per second
        
    Returns:
        function: The rate limit decorator
    """
    def decorator(func: Callable) -> Callable:
        last_called = [0.0]
        min_interval = 1.0 / calls_per_second
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            time_since_last = now - last_called[0]
            
            if time_since_last < min_interval:
                sleep_time = min_interval - time_since_last
                time.sleep(sleep_time)
            
            last_called[0] = time.time()
            return func(*args, **kwargs)
        
        return wrapper
    return decorator
```

## Advanced Examples

Let's add some more sophisticated decorator patterns:

```python
# functions_test.py (additional tests)
def test_count_calls_decorator():
    @count_calls
    def test_function():
        return "called"
    
    assert test_function.call_count == 0
    test_function()
    assert test_function.call_count == 1
    test_function()
    assert test_function.call_count == 2

def test_rate_limit_decorator():
    @rate_limit(calls_per_second=2.0)
    def fast_function():
        return time.time()
    
    start = time.time()
    fast_function()
    fast_function()
    end = time.time()
    
    # Should take at least 0.5 seconds (1/2 calls per second)
    assert end - start >= 0.4

def test_decorator_composition():
    @memoize
    @timing
    @logging_decorator
    def expensive_function(n):
        time.sleep(0.1)
        return n * n
    
    result = expensive_function(5)
    assert result == 25

def test_class_decorator():
    @count_calls
    class Counter:
        def __init__(self):
            self.value = 0
        
        def increment(self):
            self.value += 1
    
    counter = Counter()
    assert Counter.call_count == 1
    counter.increment()
    assert counter.value == 1
```

## What We've Learned

1. **Function Decorators**: Modifying function behavior without changing the function
2. **Closures**: Functions that capture variables from their enclosing scope
3. **Function Composition**: Combining functions to create new functionality
4. **Memoization**: Caching function results for performance
5. **Higher-Order Functions**: Functions that take or return other functions

## Exercises

1. Create a decorator that measures memory usage
2. Implement a decorator that validates return types
3. Create a decorator that implements circuit breaker pattern
4. Build a decorator that provides function profiling

## Key Concepts

- **Decorators**: Functions that modify other functions
- **Closures**: Functions that capture external variables
- **Function Composition**: Combining functions for new behavior
- **Memoization**: Caching for performance optimization
- **Higher-Order Functions**: Functions as first-class citizens

