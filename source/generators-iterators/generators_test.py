import pytest
from generators import (fibonacci_generator, prime_generator, data_processor, custom_range, 
                       batch_processor, sliding_window, pairwise, NumberIterator, 
                       infinite_counter, cycle_generator)

def test_fibonacci_generator():
    fib = fibonacci_generator(10)
    fib_list = list(fib)
    assert fib_list == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

def test_fibonacci_generator_infinite():
    fib = fibonacci_generator()
    first_ten = [next(fib) for _ in range(10)]
    assert first_ten == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

def test_fibonacci_generator_negative():
    with pytest.raises(ValueError):
        list(fibonacci_generator(-1))

def test_prime_generator():
    primes = prime_generator(10)
    prime_list = list(primes)
    assert prime_list == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def test_prime_generator_zero():
    primes = prime_generator(0)
    assert list(primes) == []

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

def test_custom_range_zero_step():
    with pytest.raises(ValueError):
        list(custom_range(1, 10, 0))

def test_batch_processor():
    data = list(range(20))
    batches = batch_processor(data, batch_size=5)
    batch_list = list(batches)
    
    assert len(batch_list) == 4
    assert batch_list[0] == [0, 1, 2, 3, 4]
    assert batch_list[1] == [5, 6, 7, 8, 9]
    assert batch_list[2] == [10, 11, 12, 13, 14]
    assert batch_list[3] == [15, 16, 17, 18, 19]

def test_batch_processor_invalid_size():
    with pytest.raises(ValueError):
        list(batch_processor([1, 2, 3], 0))

def test_sliding_window():
    data = [1, 2, 3, 4, 5]
    windows = sliding_window(data, 3)
    window_list = list(windows)
    
    assert window_list == [[1, 2, 3], [2, 3, 4], [3, 4, 5]]

def test_sliding_window_invalid_size():
    with pytest.raises(ValueError):
        list(sliding_window([1, 2, 3], 0))

def test_pairwise():
    data = [1, 2, 3, 4, 5]
    pairs = pairwise(data)
    pair_list = list(pairs)
    
    assert pair_list == [(1, 2), (2, 3), (3, 4), (4, 5)]

def test_custom_iterator():
    iterator = NumberIterator(1, 5)
    assert list(iterator) == [1, 2, 3, 4]

def test_custom_iterator_with_step():
    iterator = NumberIterator(1, 10, 2)
    assert list(iterator) == [1, 3, 5, 7, 9]

def test_infinite_counter():
    counter = infinite_counter(5, 2)
    values = [next(counter) for _ in range(5)]
    assert values == [5, 7, 9, 11, 13]

def test_cycle_generator():
    data = [1, 2, 3]
    cycle = cycle_generator(data)
    values = [next(cycle) for _ in range(7)]
    assert values == [1, 2, 3, 1, 2, 3, 1]

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

def test_data_processor_chaining():
    data = list(range(10))
    processor = data_processor(data)
    
    result = (processor
              .filter(lambda x: x % 2 == 0)
              .map(lambda x: x * 2)
              .take(3))
    
    assert list(result) == [0, 4, 8]

