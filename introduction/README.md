# Introduction to Test-Driven Development

Welcome to "Learn Python with Tests"! This course will teach you Python programming through Test-Driven Development (TDD), a powerful software development approach that leads to better code, fewer bugs, and more confident programming.

## What is Test-Driven Development?

Test-Driven Development (TDD) is a software development methodology where you write tests before writing the actual code. The process follows a simple but powerful cycle:

### The Red-Green-Refactor Cycle

1. **Red** - Write a failing test
2. **Green** - Write the minimal code to make the test pass
3. **Refactor** - Improve the code while keeping tests green

This cycle is repeated for each new feature or piece of functionality.

## Why TDD?

### Benefits of Test-Driven Development

1. **Better Design**: Writing tests first forces you to think about the interface and design before implementation
2. **Confidence**: Tests give you confidence that your code works as expected
3. **Documentation**: Tests serve as living documentation of how your code should behave
4. **Regression Prevention**: Tests catch bugs when you make changes
5. **Faster Development**: TDD often leads to faster development in the long run
6. **Refactoring Safety**: You can refactor with confidence knowing tests will catch any issues

### The Psychology of TDD

TDD changes how you think about programming:

- **Specification First**: You specify what you want before implementing it
- **Small Steps**: You work in small, manageable increments
- **Immediate Feedback**: You get instant feedback on whether your code works
- **Focus**: You focus on one thing at a time

## Setting Up Your Environment

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- A text editor or IDE (VS Code, PyCharm, etc.)

### Installing Dependencies

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install pytest:
   ```bash
   pip install pytest
   ```

3. Verify installation:
   ```bash
   pytest --version
   ```

## Your First TDD Example

Let's walk through a simple example to understand the TDD process.

### Step 1: Red - Write a Failing Test

Create a file called `calculator_test.py`:

```python
import pytest
from calculator import add

def test_add_two_numbers():
    result = add(2, 3)
    assert result == 5
```

Run the test:
```bash
pytest calculator_test.py
```

You should see a failure because the `calculator` module doesn't exist yet.

### Step 2: Green - Write Minimal Code

Create a file called `calculator.py`:

```python
def add(a, b):
    return a + b
```

Run the test again:
```bash
pytest calculator_test.py
```

The test should now pass!

### Step 3: Refactor - Improve the Code

Let's improve our calculator with better documentation:

```python
def add(a, b):
    """
    Add two numbers.
    
    Args:
        a (int): First number
        b (int): Second number
        
    Returns:
        int: Sum of a and b
    """
    return a + b
```

Run the test to make sure it still passes:
```bash
pytest calculator_test.py
```

## TDD Best Practices

### 1. Write Tests First

Always write the test before the implementation. This forces you to think about:
- What should the function do?
- What are the inputs and outputs?
- What are the edge cases?

### 2. Make Tests Fail First

Your test should fail initially. This ensures:
- The test is actually running
- The test is testing the right thing
- You're not writing tests that always pass

### 3. Write Minimal Code

Write just enough code to make the test pass. Don't add extra features yet.

### 4. Refactor Safely

Once your test passes, you can refactor with confidence knowing the test will catch any issues.

### 5. Keep Tests Simple

Each test should test one thing. If a test is complex, consider breaking it into multiple tests.

## Common TDD Patterns

### 1. Arrange-Act-Assert (AAA)

Structure your tests with three clear sections:

```python
def test_calculate_tax():
    # Arrange
    price = 100
    tax_rate = 0.1
    
    # Act
    result = calculate_tax(price, tax_rate)
    
    # Assert
    assert result == 10
```

### 2. Test Naming

Use descriptive test names that explain what you're testing:

```python
def test_add_returns_sum_of_two_positive_numbers():
    # Test implementation
    pass

def test_add_handles_negative_numbers():
    # Test implementation
    pass

def test_add_raises_error_for_invalid_input():
    # Test implementation
    pass
```

### 3. Edge Cases

Always test edge cases:

```python
def test_add_with_zero():
    result = add(5, 0)
    assert result == 5

def test_add_with_negative_numbers():
    result = add(-2, -3)
    assert result == -5

def test_add_with_floats():
    result = add(1.5, 2.5)
    assert result == 4.0
```

## Running Tests

### Basic pytest Usage

```bash
# Run all tests
pytest

# Run tests in a specific file
pytest test_calculator.py

# Run tests with verbose output
pytest -v

# Run tests and stop on first failure
pytest -x

# Run tests with coverage
pytest --cov=calculator
```

### Test Discovery

pytest automatically discovers tests by looking for:
- Files named `test_*.py` or `*_test.py`
- Functions named `test_*`
- Classes named `Test*`

## Common TDD Mistakes

### 1. Writing Too Much Code

Don't write more code than necessary to make the test pass.

### 2. Skipping the Red Phase

Always make sure your test fails first.

### 3. Not Refactoring

The refactor step is crucial for maintaining clean code.

### 4. Testing Implementation Details

Test behavior, not implementation. Focus on what the code does, not how it does it.

### 5. Writing Tests After Code

This defeats the purpose of TDD. Always write tests first.

## What's Next?

Now that you understand the basics of TDD, you're ready to start the course! Each chapter will build upon these concepts with increasingly complex examples.

### Course Structure

1. **Hello, world** - Your first Python program with TDD
2. **Integers** - Working with numbers and basic math
3. **Iteration** - Loops and iteration in Python
4. **Arrays and slices** - Working with lists and arrays
5. **Structs** - Classes and objects in Python
6. **Pointers and errors** - References and exception handling
7. **Maps** - Dictionaries in Python
8. **Dependency Injection** - Dependency injection patterns
9. **Mocking** - Mocking and test doubles
10. **Concurrency** - Threading and async programming
11. And many more...

### Getting Help

If you get stuck:

1. Read the error messages carefully
2. Check the test output for clues
3. Make sure your test is actually failing first
4. Write the minimal code to make it pass
5. Don't skip the refactor step

Remember: TDD is a skill that improves with practice. Don't worry if it feels awkward at first - that's normal!

## Key Takeaways

- **TDD is a cycle**: Red → Green → Refactor
- **Write tests first**: Always write the test before the code
- **Make tests fail**: Ensure your test actually tests something
- **Write minimal code**: Just enough to make the test pass
- **Refactor safely**: Improve code while keeping tests green
- **Practice**: TDD gets easier with practice

Ready to start? Let's begin with [Hello, world](../hello-world/README.md)!


