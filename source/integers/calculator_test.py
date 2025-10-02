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

