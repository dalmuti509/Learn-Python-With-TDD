import pytest
from hello_world import hello

def test_hello_returns_hello_world():
    result = hello()
    assert result == "Hello, world"

