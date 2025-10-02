#!/usr/bin/env python3
"""
Tests for Functional Programming chapter.
Learn Python with Tests - Functional Programming Concepts
"""

import pytest
from functools import reduce
from functional_programming import FunctionalProgramming


class TestHigherOrderFunctions:
    """Test higher-order function implementations."""
    
    def test_map_function(self):
        """Should apply function to each element."""
        fp = FunctionalProgramming()
        numbers = [1, 2, 3, 4, 5]
        result = fp.map_function(lambda x: x * 2, numbers)
        assert result == [2, 4, 6, 8, 10]
    
    def test_filter_function(self):
        """Should filter elements based on predicate."""
        fp = FunctionalProgramming()
        numbers = [1, 2, 3, 4, 5, 6]
        result = fp.filter_function(lambda x: x % 2 == 0, numbers)
        assert result == [2, 4, 6]
    
    def test_reduce_function(self):
        """Should reduce list to single value."""
        fp = FunctionalProgramming()
        numbers = [1, 2, 3, 4, 5]
        result = fp.reduce_function(lambda x, y: x + y, numbers)
        assert result == 15
    
    def test_reduce_with_initial(self):
        """Should reduce with initial value."""
        fp = FunctionalProgramming()
        numbers = [1, 2, 3]
        result = fp.reduce_function(lambda x, y: x * y, numbers, 10)
        assert result == 60  # 10 * 1 * 2 * 3


class TestFunctionComposition:
    """Test function composition patterns."""
    
    def test_compose_two_functions(self):
        """Should compose two functions."""
        fp = FunctionalProgramming()
        add_one = lambda x: x + 1
        multiply_two = lambda x: x * 2
        
        composed = fp.compose(multiply_two, add_one)
        result = composed(5)
        assert result == 12  # (5 + 1) * 2
    
    def test_pipe_functions(self):
        """Should pipe multiple functions in sequence."""
        fp = FunctionalProgramming()
        add_one = lambda x: x + 1
        multiply_two = lambda x: x * 2
        square = lambda x: x ** 2
        
        piped = fp.pipe(add_one, multiply_two, square)
        result = piped(3)
        assert result == 64  # ((3 + 1) * 2) ** 2 = 64
    
    def test_compose_multiple_functions(self):
        """Should compose multiple functions."""
        fp = FunctionalProgramming()
        functions = [
            lambda x: x + 1,
            lambda x: x * 2,
            lambda x: x - 3
        ]
        
        composed = fp.compose_multiple(functions)
        result = composed(5)
        assert result == 9  # ((5 + 1) * 2) - 3


class TestCurrying:
    """Test currying and partial application."""
    
    def test_curry_multiply(self):
        """Should create curried multiplication function."""
        fp = FunctionalProgramming()
        multiply_by_3 = fp.curry_multiply(3)
        result = multiply_by_3(4)
        assert result == 12
    
    def test_curry_add(self):
        """Should create curried addition function."""
        fp = FunctionalProgramming()
        add_10 = fp.curry_add(10)
        result = add_10(5)
        assert result == 15
    
    def test_partial_application(self):
        """Should demonstrate partial function application."""
        fp = FunctionalProgramming()
        
        def power(base, exponent):
            return base ** exponent
        
        square = fp.partial_apply(power, exponent=2)
        cube = fp.partial_apply(power, exponent=3)
        
        assert square(4) == 16
        assert cube(3) == 27


class TestImmutability:
    """Test immutable data operations."""
    
    def test_immutable_append(self):
        """Should append without modifying original."""
        fp = FunctionalProgramming()
        original = [1, 2, 3]
        result = fp.immutable_append(original, 4)
        
        assert original == [1, 2, 3]  # Original unchanged
        assert result == [1, 2, 3, 4]  # New list with item
    
    def test_immutable_update_dict(self):
        """Should update dict without modifying original."""
        fp = FunctionalProgramming()
        original = {'a': 1, 'b': 2}
        result = fp.immutable_update_dict(original, 'c', 3)
        
        assert original == {'a': 1, 'b': 2}  # Original unchanged
        assert result == {'a': 1, 'b': 2, 'c': 3}  # New dict
    
    def test_immutable_remove(self):
        """Should remove item without modifying original."""
        fp = FunctionalProgramming()
        original = [1, 2, 3, 4, 5]
        result = fp.immutable_remove(original, 3)
        
        assert original == [1, 2, 3, 4, 5]  # Original unchanged
        assert result == [1, 2, 4, 5]  # New list without item


class TestPureFunctions:
    """Test pure function implementations."""
    
    def test_pure_factorial(self):
        """Should calculate factorial as pure function."""
        fp = FunctionalProgramming()
        assert fp.pure_factorial(0) == 1
        assert fp.pure_factorial(1) == 1
        assert fp.pure_factorial(5) == 120
    
    def test_pure_fibonacci(self):
        """Should calculate fibonacci as pure function."""
        fp = FunctionalProgramming()
        assert fp.pure_fibonacci(0) == 0
        assert fp.pure_fibonacci(1) == 1
        assert fp.pure_fibonacci(10) == 55
    
    def test_pure_is_palindrome(self):
        """Should check palindrome as pure function."""
        fp = FunctionalProgramming()
        assert fp.pure_is_palindrome("racecar") is True
        assert fp.pure_is_palindrome("hello") is False
        assert fp.pure_is_palindrome("A man a plan a canal Panama") is True


class TestDataProcessing:
    """Test functional data processing patterns."""
    
    def test_process_numbers(self):
        """Should process numbers using functional pipeline."""
        fp = FunctionalProgramming()
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        # Get squares of even numbers
        result = fp.process_numbers(
            numbers,
            filter_func=lambda x: x % 2 == 0,
            map_func=lambda x: x ** 2
        )
        
        assert result == [4, 16, 36, 64, 100]
    
    def test_group_by_function(self):
        """Should group items by function result."""
        fp = FunctionalProgramming()
        words = ["cat", "dog", "elephant", "ant", "horse"]
        
        result = fp.group_by_function(words, len)
        expected = {
            3: ["cat", "dog", "ant"],
            8: ["elephant"],
            5: ["horse"]
        }
        
        assert result == expected
    
    def test_chain_operations(self):
        """Should chain multiple operations."""
        fp = FunctionalProgramming()
        data = [1, 2, 3, 4, 5]
        
        operations = [
            lambda lst: [x * 2 for x in lst],  # Double each
            lambda lst: [x for x in lst if x > 5],  # Filter > 5
            lambda lst: sum(lst)  # Sum all
        ]
        
        result = fp.chain_operations(data, operations)
        assert result == 18  # [2,4,6,8,10] -> [6,8,10] -> 24


class TestMemoization:
    """Test memoization patterns."""
    
    def test_memoized_fibonacci(self):
        """Should use memoization for efficiency."""
        fp = FunctionalProgramming()
        
        # Should be fast even for larger numbers due to memoization
        result = fp.memoized_fibonacci(30)
        assert result == 832040
        
        # Call again to test memoization
        result2 = fp.memoized_fibonacci(30)
        assert result2 == 832040
    
    def test_custom_memoize(self):
        """Should create custom memoization decorator."""
        fp = FunctionalProgramming()
        
        call_count = 0
        
        def expensive_function(n):
            nonlocal call_count
            call_count += 1
            return n * n
        
        memoized_func = fp.memoize(expensive_function)
        
        # First call
        result1 = memoized_func(5)
        assert result1 == 25
        assert call_count == 1
        
        # Second call with same argument (should use cache)
        result2 = memoized_func(5)
        assert result2 == 25
        assert call_count == 1  # Should not increment


if __name__ == '__main__':
    pytest.main([__file__])
