# Magic Methods

Let's explore magic methods (dunder methods) in Python using TDD. We'll build various examples that demonstrate object representation, arithmetic operations, comparison, and container behavior.

## The Problem

We want to create a Vector class that behaves like a mathematical vector with proper arithmetic operations, comparisons, and string representation.

## Red: Write Failing Tests

Let's start with some basic magic method tests:

```python
# magic_methods_test.py
import pytest
from magic_methods import Vector, Matrix, Fraction, ShoppingCart

def test_vector_creation():
    v = Vector(1, 2, 3)
    assert v.x == 1
    assert v.y == 2
    assert v.z == 3

def test_vector_string_representation():
    v = Vector(1, 2, 3)
    assert str(v) == "Vector(1, 2, 3)"
    assert repr(v) == "Vector(1, 2, 3)"

def test_vector_addition():
    v1 = Vector(1, 2, 3)
    v2 = Vector(4, 5, 6)
    v3 = v1 + v2
    assert v3.x == 5
    assert v3.y == 7
    assert v3.z == 9

def test_vector_subtraction():
    v1 = Vector(4, 5, 6)
    v2 = Vector(1, 2, 3)
    v3 = v1 - v2
    assert v3.x == 3
    assert v3.y == 3
    assert v3.z == 3

def test_vector_multiplication():
    v1 = Vector(1, 2, 3)
    v2 = v1 * 2
    assert v2.x == 2
    assert v2.y == 4
    assert v2.z == 6

def test_vector_equality():
    v1 = Vector(1, 2, 3)
    v2 = Vector(1, 2, 3)
    v3 = Vector(1, 2, 4)
    
    assert v1 == v2
    assert v1 != v3

def test_vector_length():
    v = Vector(3, 4, 0)
    assert len(v) == 3
    assert abs(v) == 5.0  # Magnitude

def test_vector_indexing():
    v = Vector(1, 2, 3)
    assert v[0] == 1
    assert v[1] == 2
    assert v[2] == 3
    
    v[0] = 10
    assert v[0] == 10

def test_vector_iteration():
    v = Vector(1, 2, 3)
    components = list(v)
    assert components == [1, 2, 3]

def test_matrix_creation():
    m = Matrix([[1, 2], [3, 4]])
    assert m.rows == 2
    assert m.cols == 2

def test_matrix_multiplication():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[5, 6], [7, 8]])
    m3 = m1 * m2
    assert m3[0, 0] == 19
    assert m3[0, 1] == 22
    assert m3[1, 0] == 43
    assert m3[1, 1] == 50

def test_fraction_creation():
    f = Fraction(3, 4)
    assert f.numerator == 3
    assert f.denominator == 4

def test_fraction_arithmetic():
    f1 = Fraction(1, 2)
    f2 = Fraction(1, 3)
    f3 = f1 + f2
    assert f3.numerator == 5
    assert f3.denominator == 6

def test_fraction_comparison():
    f1 = Fraction(1, 2)
    f2 = Fraction(2, 4)
    f3 = Fraction(1, 3)
    
    assert f1 == f2
    assert f1 > f3
    assert f3 < f1

def test_shopping_cart():
    cart = ShoppingCart()
    cart.add_item("apple", 1.50)
    cart.add_item("banana", 0.75)
    
    assert len(cart) == 2
    assert "apple" in cart
    assert cart["apple"] == 1.50
    
    total = sum(cart)
    assert total == 2.25
```

## Green: Write the Minimal Code to Pass

Now let's implement our classes with magic methods:

```python
# magic_methods.py
import math
from typing import List, Union, Any

class Vector:
    """
    A 3D vector class with magic methods.
    """
    
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z
    
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

class Matrix:
    """
    A matrix class with magic methods.
    """
    
    def __init__(self, data: List[List[float]]):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0
    
    def __str__(self):
        return f"Matrix({self.rows}x{self.cols})"
    
    def __repr__(self):
        return f"Matrix({self.data})"
    
    def __getitem__(self, key):
        row, col = key
        return self.data[row][col]
    
    def __setitem__(self, key, value):
        row, col = key
        self.data[row][col] = value
    
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

class Fraction:
    """
    A fraction class with magic methods.
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
    
    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)
    
    def __gt__(self, other):
        return not self.__le__(other)
    
    def __ge__(self, other):
        return not self.__lt__(other)

class ShoppingCart:
    """
    A shopping cart class with magic methods.
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
```

## Run the Tests

```bash
pytest magic_methods_test.py -v
```

## Refactor: Improve the Code

Let's improve our code with better error handling and additional features:

```python
# magic_methods.py
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
```

## Advanced Examples

Let's add some more sophisticated magic method patterns:

```python
# magic_methods_test.py (additional tests)
def test_vector_dot_product():
    v1 = Vector(1, 2, 3)
    v2 = Vector(4, 5, 6)
    dot_product = v1.dot(v2)
    assert dot_product == 32  # 1*4 + 2*5 + 3*6

def test_vector_cross_product():
    v1 = Vector(1, 0, 0)
    v2 = Vector(0, 1, 0)
    cross_product = v1.cross(v2)
    assert cross_product == Vector(0, 0, 1)

def test_vector_negation():
    v = Vector(1, 2, 3)
    neg_v = -v
    assert neg_v == Vector(-1, -2, -3)

def test_vector_boolean():
    v1 = Vector(0, 0, 0)
    v2 = Vector(1, 0, 0)
    
    assert not v1
    assert v2

def test_fraction_float_conversion():
    f = Fraction(3, 4)
    assert float(f) == 0.75
    assert int(f) == 0

def test_fraction_boolean():
    f1 = Fraction(0, 1)
    f2 = Fraction(1, 2)
    
    assert not f1
    assert f2

def test_shopping_cart_callable():
    cart = ShoppingCart()
    cart.add_item("apple", 1.50)
    
    assert cart("apple") == 1.50

def test_shopping_cart_boolean():
    cart1 = ShoppingCart()
    cart2 = ShoppingCart()
    cart2.add_item("apple", 1.50)
    
    assert not cart1
    assert cart2
```

## What We've Learned

1. **String Representation**: `__str__` and `__repr__` methods
2. **Arithmetic Operations**: `__add__`, `__sub__`, `__mul__`, `__truediv__`
3. **Comparison Operations**: `__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__`
4. **Container Behavior**: `__len__`, `__getitem__`, `__setitem__`, `__contains__`
5. **Iteration**: `__iter__` method for making objects iterable

## Exercises

1. Create a class that implements a custom number type
2. Build a class that behaves like a dictionary
3. Implement a class that supports matrix operations
4. Create a class that implements a custom sequence

## Key Concepts

- **Magic Methods**: Special methods that define object behavior
- **String Representation**: How objects are displayed as strings
- **Arithmetic Operations**: Mathematical operations on objects
- **Comparison Operations**: How objects are compared
- **Container Behavior**: Making objects behave like containers

