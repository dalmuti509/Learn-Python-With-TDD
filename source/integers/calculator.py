import math

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

