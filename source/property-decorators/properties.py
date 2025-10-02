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

