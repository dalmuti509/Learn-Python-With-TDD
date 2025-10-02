import math
from typing import List, Union, Any, Iterator
from functools import total_ordering

class Vector:
    """
    A 3D vector class with comprehensive magic methods.
    """
    
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __str__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"
    
    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Can only add Vector to Vector")
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Can only subtract Vector from Vector")
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        if not isinstance(scalar, (int, float)):
            raise TypeError("Can only multiply Vector by scalar")
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar):
        if not isinstance(scalar, (int, float)):
            raise TypeError("Can only divide Vector by scalar")
        if scalar == 0:
            raise ValueError("Cannot divide Vector by zero")
        return Vector(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __len__(self):
        return 3
    
    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise IndexError("Vector index out of range")
    
    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
        else:
            raise IndexError("Vector index out of range")
    
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
    
    def __bool__(self):
        return self.x != 0 or self.y != 0 or self.z != 0
    
    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)
    
    def __pos__(self):
        return Vector(self.x, self.y, self.z)
    
    def dot(self, other):
        """Calculate dot product with another vector."""
        if not isinstance(other, Vector):
            raise TypeError("Can only calculate dot product with Vector")
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        """Calculate cross product with another vector."""
        if not isinstance(other, Vector):
            raise TypeError("Can only calculate cross product with Vector")
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

class Matrix:
    """
    A matrix class with comprehensive magic methods.
    """
    
    def __init__(self, data: List[List[float]]):
        if not data:
            raise ValueError("Matrix cannot be empty")
        
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0
        
        # Validate that all rows have the same length
        for row in data:
            if len(row) != self.cols:
                raise ValueError("All rows must have the same length")
    
    def __str__(self):
        return f"Matrix({self.rows}x{self.cols})"
    
    def __repr__(self):
        return f"Matrix({self.data})"
    
    def __getitem__(self, key):
        if isinstance(key, tuple) and len(key) == 2:
            row, col = key
            return self.data[row][col]
        else:
            raise TypeError("Matrix indexing requires (row, col) tuple")
    
    def __setitem__(self, key, value):
        if isinstance(key, tuple) and len(key) == 2:
            row, col = key
            self.data[row][col] = value
        else:
            raise TypeError("Matrix indexing requires (row, col) tuple")
    
    def __mul__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Can only multiply Matrix by Matrix")
        
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions incompatible for multiplication")
        
        result = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                sum_val = 0
                for k in range(self.cols):
                    sum_val += self.data[i][k] * other.data[k][j]
                row.append(sum_val)
            result.append(row)
        
        return Matrix(result)
    
    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Can only add Matrix to Matrix")
        
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition")
        
        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.data[i][j] + other.data[i][j])
            result.append(row)
        
        return Matrix(result)
    
    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        return self.data == other.data
    
    def __len__(self):
        return self.rows
    
    def __iter__(self):
        return iter(self.data)

@total_ordering
class Fraction:
    """
    A fraction class with comprehensive magic methods.
    """
    
    def __init__(self, numerator: int, denominator: int = 1):
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        
        # Simplify the fraction
        gcd_val = self._gcd(abs(numerator), abs(denominator))
        self.numerator = numerator // gcd_val
        self.denominator = denominator // gcd_val
        
        # Ensure denominator is positive
        if self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator
    
    def _gcd(self, a: int, b: int) -> int:
        """Calculate greatest common divisor."""
        while b:
            a, b = b, a % b
        return a
    
    def __str__(self):
        return f"{self.numerator}/{self.denominator}"
    
    def __repr__(self):
        return f"Fraction({self.numerator}, {self.denominator})"
    
    def __add__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        
        new_num = self.numerator * other.denominator + other.numerator * self.denominator
        new_den = self.denominator * other.denominator
        return Fraction(new_num, new_den)
    
    def __sub__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        
        new_num = self.numerator * other.denominator - other.numerator * self.denominator
        new_den = self.denominator * other.denominator
        return Fraction(new_num, new_den)
    
    def __mul__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        
        return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)
    
    def __truediv__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        
        return Fraction(self.numerator * other.denominator, self.denominator * other.numerator)
    
    def __eq__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        return self.numerator == other.numerator and self.denominator == other.denominator
    
    def __lt__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        return self.numerator * other.denominator < other.numerator * self.denominator
    
    def __float__(self):
        return self.numerator / self.denominator
    
    def __int__(self):
        return int(self.__float__())
    
    def __bool__(self):
        return self.numerator != 0

class ShoppingCart:
    """
    A shopping cart class with comprehensive magic methods.
    """
    
    def __init__(self):
        self.items = {}
    
    def add_item(self, name: str, price: float):
        """Add an item to the cart."""
        self.items[name] = price
    
    def __len__(self):
        return len(self.items)
    
    def __contains__(self, item):
        return item in self.items
    
    def __getitem__(self, item):
        return self.items[item]
    
    def __setitem__(self, item, price):
        self.items[item] = price
    
    def __delitem__(self, item):
        del self.items[item]
    
    def __iter__(self):
        return iter(self.items.values())
    
    def __str__(self):
        return f"ShoppingCart({len(self.items)} items)"
    
    def __repr__(self):
        return f"ShoppingCart({self.items})"
    
    def __bool__(self):
        return len(self.items) > 0
    
    def __call__(self, item):
        """Make the cart callable to get item price."""
        return self.items[item]

