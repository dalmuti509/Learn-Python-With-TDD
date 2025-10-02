import pytest
import math
from properties import (Temperature, Circle, BankAccount, Person, ConfigManager, 
                       ExpensiveCalculation, cached_property)

def test_temperature_celsius_property():
    temp = Temperature(25)
    assert temp.celsius == 25
    assert temp.fahrenheit == 77.0
    assert temp.kelvin == 298.15

def test_temperature_fahrenheit_property():
    temp = Temperature()
    temp.fahrenheit = 86
    assert temp.celsius == 30.0
    assert temp.fahrenheit == 86
    assert temp.kelvin == 303.15

def test_temperature_kelvin_property():
    temp = Temperature()
    temp.kelvin = 273.15
    assert temp.celsius == 0.0
    assert temp.fahrenheit == 32.0
    assert temp.kelvin == 273.15

def test_temperature_validation():
    temp = Temperature()
    
    with pytest.raises(ValueError):
        temp.celsius = -300  # Below absolute zero
    
    with pytest.raises(ValueError):
        temp.fahrenheit = -500  # Below absolute zero

def test_circle_properties():
    circle = Circle(5)
    assert circle.radius == 5
    assert circle.diameter == 10
    assert circle.area == 78.54  # Approximately
    assert circle.circumference == 31.42  # Approximately

def test_circle_diameter_property():
    circle = Circle()
    circle.diameter = 20
    assert circle.radius == 10
    assert circle.diameter == 20

def test_circle_validation():
    circle = Circle()
    
    with pytest.raises(ValueError):
        circle.radius = -5
    
    with pytest.raises(ValueError):
        circle.diameter = -10

def test_bank_account_properties():
    account = BankAccount("12345", "John Doe", 1000.0)
    assert account.account_number == "12345"
    assert account.owner == "John Doe"
    assert account.balance == 1000.0
    assert account.is_overdrawn == False

def test_bank_account_balance_validation():
    account = BankAccount("12345", "John Doe", 1000.0)
    
    with pytest.raises(ValueError):
        account.balance = -1000  # Negative balance not allowed

def test_person_properties():
    person = Person("John", "Doe", 30)
    assert person.first_name == "John"
    assert person.last_name == "Doe"
    assert person.age == 30
    assert person.full_name == "John Doe"
    assert person.is_adult == True

def test_person_age_validation():
    person = Person("John", "Doe", 30)
    
    with pytest.raises(ValueError):
        person.age = -5
    
    with pytest.raises(ValueError):
        person.age = 150

def test_config_manager_properties():
    config = ConfigManager()
    config.database_url = "postgresql://localhost:5432/mydb"
    config.api_key = "secret123"
    
    assert config.database_url == "postgresql://localhost:5432/mydb"
    assert config.api_key == "secret123"
    assert config.is_configured == True

def test_config_manager_validation():
    config = ConfigManager()
    
    with pytest.raises(ValueError):
        config.database_url = "invalid-url"
    
    with pytest.raises(ValueError):
        config.api_key = ""

def test_property_deletion():
    person = Person("John", "Doe", 30)
    
    # Test property deletion
    del person.age
    assert person.age == 0  # Default value

def test_cached_property():
    calc = ExpensiveCalculation()
    
    # First access should calculate
    value1 = calc.expensive_value
    assert calc.calculation_count == 1
    
    # Second access should use cached value
    value2 = calc.expensive_value
    assert calc.calculation_count == 1
    assert value1 == value2

def test_cached_property_clear():
    calc = ExpensiveCalculation()
    
    # First access should calculate
    value1 = calc.expensive_value
    assert calc.calculation_count == 1
    
    # Clear cache and access again
    calc.clear_cache()
    value2 = calc.expensive_value
    assert calc.calculation_count == 2

def test_property_validation():
    temp = Temperature()
    
    # Test valid values
    temp.celsius = 25
    assert temp.celsius == 25
    
    # Test invalid values
    with pytest.raises(ValueError):
        temp.celsius = -300

def test_property_chaining():
    circle = Circle(5)
    circle.diameter = 20
    assert circle.radius == 10
    assert circle.area == math.pi * 100

def test_property_deletion():
    person = Person("John", "Doe", 30)
    
    # Test property deletion
    del person.age
    assert person.age == 0  # Default value

def test_property_readonly():
    class ReadOnlyProperty:
        def __init__(self, value):
            self._value = value
        
        @property
        def value(self):
            return self._value
    
    obj = ReadOnlyProperty(42)
    assert obj.value == 42
    
    # Should not be able to set
    with pytest.raises(AttributeError):
        obj.value = 100

