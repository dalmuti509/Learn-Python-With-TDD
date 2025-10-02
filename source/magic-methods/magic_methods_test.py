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

def test_matrix_addition():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[5, 6], [7, 8]])
    m3 = m1 + m2
    assert m3[0, 0] == 6
    assert m3[0, 1] == 8
    assert m3[1, 0] == 10
    assert m3[1, 1] == 12

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

def test_fraction_float_conversion():
    f = Fraction(3, 4)
    assert float(f) == 0.75
    assert int(f) == 0

def test_fraction_boolean():
    f1 = Fraction(0, 1)
    f2 = Fraction(1, 2)
    
    assert not f1
    assert f2

def test_shopping_cart():
    cart = ShoppingCart()
    cart.add_item("apple", 1.50)
    cart.add_item("banana", 0.75)
    
    assert len(cart) == 2
    assert "apple" in cart
    assert cart["apple"] == 1.50
    
    total = sum(cart)
    assert total == 2.25

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

