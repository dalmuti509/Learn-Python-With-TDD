# Integers

Let's explore working with integers in Python using TDD. We'll build a simple calculator that demonstrates basic arithmetic operations.

## The Problem

We want to create a calculator that can perform basic arithmetic operations: addition, subtraction, multiplication, and division.

## Red: Write Failing Tests

Let's start by writing tests for our calculator:

```python
# calculator_test.py
import pytest
from calculator import Calculator

def test_addition():
    calc = Calculator()
    result = calc.add(2, 3)
    assert result == 5

def test_subtraction():
    calc = Calculator()
    result = calc.subtract(5, 3)
    assert result == 2

def test_multiplication():
    calc = Calculator()
    result = calc.multiply(4, 3)
    assert result == 12

def test_division():
    calc = Calculator()
    result = calc.divide(10, 2)
    assert result == 5

def test_division_by_zero():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.divide(10, 0)
```

## Green: Write the Minimal Code to Pass

Now let's implement our calculator:

```python
# calculator.py
class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
```

## Run the Tests

```bash
pytest calculator_test.py -v
```

## Refactor: Improve the Code

Let's add some documentation and improve our calculator:

```python
# calculator.py
class Calculator:
    """
    A simple calculator that performs basic arithmetic operations.
    """
    
    def add(self, a, b):
        """
        Add two numbers.
        
        Args:
            a (int): First number
            b (int): Second number
            
        Returns:
            int: The sum of a and b
        """
        return a + b
    
    def subtract(self, a, b):
        """
        Subtract b from a.
        
        Args:
            a (int): First number
            b (int): Second number
            
        Returns:
            int: The difference of a and b
        """
        return a - b
    
    def multiply(self, a, b):
        """
        Multiply two numbers.
        
        Args:
            a (int): First number
            b (int): Second number
            
        Returns:
            int: The product of a and b
        """
        return a * b
    
    def divide(self, a, b):
        """
        Divide a by b.
        
        Args:
            a (int): Dividend
            b (int): Divisor
            
        Returns:
            float: The quotient of a and b
            
        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
```

## What We've Learned

1. **Class-based Design**: We created a Calculator class to organize our methods
2. **Error Handling**: We handled the edge case of division by zero
3. **Type Hints**: We documented the expected types in our docstrings
4. **Exception Testing**: We tested that our code raises the correct exception

## Advanced Examples

Let's add some more advanced functionality:

```python
# calculator_test.py (additional tests)
def test_power():
    calc = Calculator()
    result = calc.power(2, 3)
    assert result == 8

def test_square_root():
    calc = Calculator()
    result = calc.square_root(9)
    assert result == 3

def test_square_root_negative():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.square_root(-1)
```

```python
# calculator.py (additional methods)
import math

def power(self, base, exponent):
    """
    Raise base to the power of exponent.
    
    Args:
        base (int): The base number
        exponent (int): The exponent
        
    Returns:
        float: base raised to the power of exponent
    """
    return base ** exponent

def square_root(self, number):
    """
    Calculate the square root of a number.
    
    Args:
        number (int): The number to find the square root of
        
    Returns:
        float: The square root of the number
        
    Raises:
        ValueError: If the number is negative
    """
    if number < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(number)
```

## Exercises

1. Add a method to calculate the factorial of a number
2. Add a method to check if a number is prime
3. Add a method to find the greatest common divisor of two numbers
4. Add a method to find the least common multiple of two numbers

## Key Concepts

- **Classes and Objects**: Organizing code into logical units
- **Error Handling**: Dealing with edge cases and invalid inputs
- **Mathematical Operations**: Working with Python's built-in math functions
- **Test Coverage**: Ensuring all code paths are tested

