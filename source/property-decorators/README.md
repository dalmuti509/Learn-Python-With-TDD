# Property Decorators

Let's explore property decorators in Python using TDD. We'll build various examples that demonstrate `@property`, `@setter`, `@deleter`, and advanced property patterns.

## The Problem

We want to create a temperature converter class that uses properties to provide a clean interface while maintaining data validation and encapsulation.

## Red: Write Failing Tests

Let's start with some basic property tests:

```python
# properties_test.py
import pytest
from properties import Temperature, Circle, BankAccount, Person, ConfigManager

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
    class ExpensiveCalculation:
        def __init__(self):
            self.calculation_count = 0
        
        @property
        def expensive_value(self):
            self.calculation_count += 1
            return sum(range(1000000))
    
    calc = ExpensiveCalculation()
    
    # First access should calculate
    value1 = calc.expensive_value
    assert calc.calculation_count == 1
    
    # Second access should use cached value
    value2 = calc.expensive_value
    assert calc.calculation_count == 1
    assert value1 == value2
```

## Green: Write the Minimal Code to Pass

Now let's implement our property classes:

```python
# properties.py
import math
import re
from typing import Optional

class Temperature:
    """
    A temperature class with properties for different units.
    """
    
    def __init__(self, celsius: float = 0.0):
        self._celsius = celsius
    
    @property
    def celsius(self) -> float:
        """Get temperature in Celsius."""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value: float):
        """Set temperature in Celsius."""
        if value < -273.15:  # Absolute zero
            raise ValueError("Temperature cannot be below absolute zero (-273.15°C)")
        self._celsius = value
    
    @property
    def fahrenheit(self) -> float:
        """Get temperature in Fahrenheit."""
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value: float):
        """Set temperature in Fahrenheit."""
        celsius = (value - 32) * 5/9
        if celsius < -273.15:
            raise ValueError("Temperature cannot be below absolute zero")
        self._celsius = celsius
    
    @property
    def kelvin(self) -> float:
        """Get temperature in Kelvin."""
        return self._celsius + 273.15
    
    @kelvin.setter
    def kelvin(self, value: float):
        """Set temperature in Kelvin."""
        if value < 0:
            raise ValueError("Temperature cannot be below absolute zero (0K)")
        self._celsius = value - 273.15

class Circle:
    """
    A circle class with radius, diameter, area, and circumference properties.
    """
    
    def __init__(self, radius: float = 1.0):
        self._radius = radius
    
    @property
    def radius(self) -> float:
        """Get the radius."""
        return self._radius
    
    @radius.setter
    def radius(self, value: float):
        """Set the radius."""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @property
    def diameter(self) -> float:
        """Get the diameter."""
        return self._radius * 2
    
    @diameter.setter
    def diameter(self, value: float):
        """Set the diameter."""
        if value < 0:
            raise ValueError("Diameter cannot be negative")
        self._radius = value / 2
    
    @property
    def area(self) -> float:
        """Get the area."""
        return math.pi * self._radius ** 2
    
    @property
    def circumference(self) -> float:
        """Get the circumference."""
        return 2 * math.pi * self._radius

class BankAccount:
    """
    A bank account class with balance validation.
    """
    
    def __init__(self, account_number: str, owner: str, initial_balance: float = 0.0):
        self.account_number = account_number
        self.owner = owner
        self._balance = initial_balance
    
    @property
    def balance(self) -> float:
        """Get the account balance."""
        return self._balance
    
    @balance.setter
    def balance(self, value: float):
        """Set the account balance."""
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value
    
    @property
    def is_overdrawn(self) -> bool:
        """Check if the account is overdrawn."""
        return self._balance < 0

class Person:
    """
    A person class with name and age properties.
    """
    
    def __init__(self, first_name: str, last_name: str, age: int = 0):
        self.first_name = first_name
        self.last_name = last_name
        self._age = age
    
    @property
    def age(self) -> int:
        """Get the person's age."""
        return self._age
    
    @age.setter
    def age(self, value: int):
        """Set the person's age."""
        if value < 0:
            raise ValueError("Age cannot be negative")
        if value > 150:
            raise ValueError("Age cannot be greater than 150")
        self._age = value
    
    @age.deleter
    def age(self):
        """Delete the age (reset to 0)."""
        self._age = 0
    
    @property
    def full_name(self) -> str:
        """Get the full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_adult(self) -> bool:
        """Check if the person is an adult."""
        return self._age >= 18

class ConfigManager:
    """
    A configuration manager with validation.
    """
    
    def __init__(self):
        self._database_url = ""
        self._api_key = ""
    
    @property
    def database_url(self) -> str:
        """Get the database URL."""
        return self._database_url
    
    @database_url.setter
    def database_url(self, value: str):
        """Set the database URL."""
        if not self._is_valid_url(value):
            raise ValueError("Invalid database URL format")
        self._database_url = value
    
    @property
    def api_key(self) -> str:
        """Get the API key."""
        return self._api_key
    
    @api_key.setter
    def api_key(self, value: str):
        """Set the API key."""
        if not value or len(value) < 8:
            raise ValueError("API key must be at least 8 characters long")
        self._api_key = value
    
    @property
    def is_configured(self) -> bool:
        """Check if the configuration is complete."""
        return bool(self._database_url and self._api_key)
    
    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format."""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(url_pattern.match(url))
```

## Run the Tests

```bash
pytest properties_test.py -v
```

## Refactor: Improve the Code

Let's improve our code with better error handling and additional features:

```python
# properties.py
import math
import re
from typing import Optional, Any, Callable
from functools import wraps

class Temperature:
    """
    A temperature class with properties for different units.
    """
    
    def __init__(self, celsius: float = 0.0):
        self._celsius = celsius
    
    @property
    def celsius(self) -> float:
        """Get temperature in Celsius."""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value: float):
        """Set temperature in Celsius."""
        if value < -273.15:  # Absolute zero
            raise ValueError("Temperature cannot be below absolute zero (-273.15°C)")
        self._celsius = value
    
    @property
    def fahrenheit(self) -> float:
        """Get temperature in Fahrenheit."""
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value: float):
        """Set temperature in Fahrenheit."""
        celsius = (value - 32) * 5/9
        if celsius < -273.15:
            raise ValueError("Temperature cannot be below absolute zero")
        self._celsius = celsius
    
    @property
    def kelvin(self) -> float:
        """Get temperature in Kelvin."""
        return self._celsius + 273.15
    
    @kelvin.setter
    def kelvin(self, value: float):
        """Set temperature in Kelvin."""
        if value < 0:
            raise ValueError("Temperature cannot be below absolute zero (0K)")
        self._celsius = value - 273.15
    
    def __str__(self):
        return f"{self._celsius:.2f}°C"
    
    def __repr__(self):
        return f"Temperature({self._celsius})"

class Circle:
    """
    A circle class with radius, diameter, area, and circumference properties.
    """
    
    def __init__(self, radius: float = 1.0):
        self._radius = radius
    
    @property
    def radius(self) -> float:
        """Get the radius."""
        return self._radius
    
    @radius.setter
    def radius(self, value: float):
        """Set the radius."""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @property
    def diameter(self) -> float:
        """Get the diameter."""
        return self._radius * 2
    
    @diameter.setter
    def diameter(self, value: float):
        """Set the diameter."""
        if value < 0:
            raise ValueError("Diameter cannot be negative")
        self._radius = value / 2
    
    @property
    def area(self) -> float:
        """Get the area."""
        return math.pi * self._radius ** 2
    
    @property
    def circumference(self) -> float:
        """Get the circumference."""
        return 2 * math.pi * self._radius
    
    def __str__(self):
        return f"Circle(radius={self._radius:.2f})"
    
    def __repr__(self):
        return f"Circle({self._radius})"

class BankAccount:
    """
    A bank account class with balance validation.
    """
    
    def __init__(self, account_number: str, owner: str, initial_balance: float = 0.0):
        self.account_number = account_number
        self.owner = owner
        self._balance = initial_balance
    
    @property
    def balance(self) -> float:
        """Get the account balance."""
        return self._balance
    
    @balance.setter
    def balance(self, value: float):
        """Set the account balance."""
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value
    
    @property
    def is_overdrawn(self) -> bool:
        """Check if the account is overdrawn."""
        return self._balance < 0
    
    def __str__(self):
        return f"BankAccount({self.account_number}, {self.owner}, ${self._balance:.2f})"

class Person:
    """
    A person class with name and age properties.
    """
    
    def __init__(self, first_name: str, last_name: str, age: int = 0):
        self.first_name = first_name
        self.last_name = last_name
        self._age = age
    
    @property
    def age(self) -> int:
        """Get the person's age."""
        return self._age
    
    @age.setter
    def age(self, value: int):
        """Set the person's age."""
        if value < 0:
            raise ValueError("Age cannot be negative")
        if value > 150:
            raise ValueError("Age cannot be greater than 150")
        self._age = value
    
    @age.deleter
    def age(self):
        """Delete the age (reset to 0)."""
        self._age = 0
    
    @property
    def full_name(self) -> str:
        """Get the full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_adult(self) -> bool:
        """Check if the person is an adult."""
        return self._age >= 18
    
    def __str__(self):
        return f"Person({self.full_name}, {self._age})"

class ConfigManager:
    """
    A configuration manager with validation.
    """
    
    def __init__(self):
        self._database_url = ""
        self._api_key = ""
    
    @property
    def database_url(self) -> str:
        """Get the database URL."""
        return self._database_url
    
    @database_url.setter
    def database_url(self, value: str):
        """Set the database URL."""
        if not self._is_valid_url(value):
            raise ValueError("Invalid database URL format")
        self._database_url = value
    
    @property
    def api_key(self) -> str:
        """Get the API key."""
        return self._api_key
    
    @api_key.setter
    def api_key(self, value: str):
        """Set the API key."""
        if not value or len(value) < 8:
            raise ValueError("API key must be at least 8 characters long")
        self._api_key = value
    
    @property
    def is_configured(self) -> bool:
        """Check if the configuration is complete."""
        return bool(self._database_url and self._api_key)
    
    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format."""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(url_pattern.match(url))

def cached_property(func):
    """
    A decorator that caches the result of a property.
    """
    @wraps(func)
    def wrapper(self):
        if not hasattr(self, '_cache'):
            self._cache = {}
        if func.__name__ not in self._cache:
            self._cache[func.__name__] = func(self)
        return self._cache[func.__name__]
    return property(wrapper)

class ExpensiveCalculation:
    """
    A class that demonstrates cached properties.
    """
    
    def __init__(self):
        self.calculation_count = 0
    
    @cached_property
    def expensive_value(self):
        """An expensive calculation that should be cached."""
        self.calculation_count += 1
        return sum(range(1000000))
    
    def clear_cache(self):
        """Clear the cached values."""
        if hasattr(self, '_cache'):
            self._cache.clear()
```

## Advanced Examples

Let's add some more sophisticated property patterns:

```python
# properties_test.py (additional tests)
def test_cached_property():
    calc = ExpensiveCalculation()
    
    # First access should calculate
    value1 = calc.expensive_value
    assert calc.calculation_count == 1
    
    # Second access should use cached value
    value2 = calc.expensive_value
    assert calc.calculation_count == 1
    assert value1 == value2
    
    # Clear cache and access again
    calc.clear_cache()
    value3 = calc.expensive_value
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
```

## What We've Learned

1. **Property Decorators**: Using `@property`, `@setter`, `@deleter`
2. **Data Validation**: Validating input in property setters
3. **Computed Properties**: Properties that calculate values on demand
4. **Property Chaining**: Properties that depend on other properties
5. **Cached Properties**: Properties that cache expensive calculations

## Exercises

1. Create a property that validates email addresses
2. Implement a property that converts between different units
3. Build a property that logs all access and modifications
4. Create a property that enforces business rules

## Key Concepts

- **Property Decorators**: `@property`, `@setter`, `@deleter`
- **Data Validation**: Input validation in property setters
- **Computed Properties**: Properties that calculate values
- **Property Chaining**: Properties that depend on other properties
- **Cached Properties**: Properties that cache expensive calculations

