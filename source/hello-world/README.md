# Hello, world

Let's start with the traditional "Hello, world" example, but we'll use Test-Driven Development (TDD) to build it.

## The Problem

We want to create a function that returns the string "Hello, world".

## Red: Write a Failing Test

First, let's write a test that describes what we want our function to do:

```python
# hello_world_test.py
import pytest
from hello_world import hello

def test_hello_returns_hello_world():
    result = hello()
    assert result == "Hello, world"
```

## Green: Write the Minimal Code to Pass

Now let's write the minimal code to make our test pass:

```python
# hello_world.py
def hello():
    return "Hello, world"
```

## Run the Test

Let's run our test to make sure it passes:

```bash
pytest hello_world_test.py -v
```

You should see output like:

```
hello_world_test.py::test_hello_returns_hello_world PASSED
```

## Refactor: Improve the Code

Our code is already quite simple, but let's add some documentation:

```python
# hello_world.py
def hello():
    """
    Returns a greeting message.
    
    Returns:
        str: The string "Hello, world"
    """
    return "Hello, world"
```

## What We've Learned

1. **Red-Green-Refactor Cycle**: We wrote a failing test (Red), made it pass (Green), then improved the code (Refactor)
2. **Test-First Development**: We wrote the test before the implementation
3. **Minimal Implementation**: We wrote just enough code to make the test pass
4. **Documentation**: We added docstrings to document our function

## Next Steps

This simple example demonstrates the TDD cycle. In the next chapters, we'll explore more complex examples that show how TDD helps us design better software.

## Exercises

1. Try modifying the test to expect a different message and see the test fail
2. Add a parameter to the `hello` function to make it more flexible
3. Write tests for edge cases (empty strings, None values, etc.)

## Key TDD Principles

- **Write tests first**: Always write a failing test before writing code
- **Make it pass**: Write the minimal code to make the test pass
- **Refactor**: Improve the code while keeping tests green
- **Repeat**: Continue this cycle for each new feature

