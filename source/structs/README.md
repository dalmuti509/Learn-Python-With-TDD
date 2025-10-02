# Classes and Methods

Let's explore object-oriented programming in Python using TDD. We'll build various classes that demonstrate encapsulation, inheritance, and polymorphism.

## The Problem

We want to create a banking system with accounts, transactions, and different types of accounts.

## Red: Write Failing Tests

Let's start with a basic Account class:

```python
# account_test.py
import pytest
from account import Account, SavingsAccount, CheckingAccount

def test_account_creation():
    account = Account("12345", "John Doe", 1000.0)
    assert account.account_number == "12345"
    assert account.owner == "John Doe"
    assert account.balance == 1000.0

def test_deposit():
    account = Account("12345", "John Doe", 1000.0)
    account.deposit(500.0)
    assert account.balance == 1500.0

def test_withdraw():
    account = Account("12345", "John Doe", 1000.0)
    account.withdraw(300.0)
    assert account.balance == 700.0

def test_withdraw_insufficient_funds():
    account = Account("12345", "John Doe", 100.0)
    with pytest.raises(ValueError):
        account.withdraw(200.0)

def test_get_balance():
    account = Account("12345", "John Doe", 1000.0)
    assert account.get_balance() == 1000.0

def test_savings_account_interest():
    account = SavingsAccount("12345", "John Doe", 1000.0, 0.05)
    account.add_interest()
    assert account.balance == 1050.0

def test_checking_account_overdraft():
    account = CheckingAccount("12345", "John Doe", 1000.0, 500.0)
    account.withdraw(1200.0)
    assert account.balance == -200.0

def test_checking_account_overdraft_limit():
    account = CheckingAccount("12345", "John Doe", 1000.0, 500.0)
    with pytest.raises(ValueError):
        account.withdraw(1600.0)
```

## Green: Write the Minimal Code to Pass

Now let's implement our classes:

```python
# account.py
class Account:
    """
    A basic bank account.
    """
    
    def __init__(self, account_number, owner, initial_balance=0.0):
        """
        Initialize a new account.
        
        Args:
            account_number (str): Unique account identifier
            owner (str): Account owner's name
            initial_balance (float): Initial account balance
        """
        self.account_number = account_number
        self.owner = owner
        self.balance = initial_balance
    
    def deposit(self, amount):
        """
        Deposit money into the account.
        
        Args:
            amount (float): Amount to deposit
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
    
    def withdraw(self, amount):
        """
        Withdraw money from the account.
        
        Args:
            amount (float): Amount to withdraw
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
    
    def get_balance(self):
        """
        Get the current account balance.
        
        Returns:
            float: Current balance
        """
        return self.balance

class SavingsAccount(Account):
    """
    A savings account that earns interest.
    """
    
    def __init__(self, account_number, owner, initial_balance=0.0, interest_rate=0.0):
        """
        Initialize a new savings account.
        
        Args:
            account_number (str): Unique account identifier
            owner (str): Account owner's name
            initial_balance (float): Initial account balance
            interest_rate (float): Annual interest rate
        """
        super().__init__(account_number, owner, initial_balance)
        self.interest_rate = interest_rate
    
    def add_interest(self):
        """
        Add interest to the account balance.
        """
        interest = self.balance * self.interest_rate
        self.balance += interest

class CheckingAccount(Account):
    """
    A checking account with overdraft protection.
    """
    
    def __init__(self, account_number, owner, initial_balance=0.0, overdraft_limit=0.0):
        """
        Initialize a new checking account.
        
        Args:
            account_number (str): Unique account identifier
            owner (str): Account owner's name
            initial_balance (float): Initial account balance
            overdraft_limit (float): Maximum overdraft amount
        """
        super().__init__(account_number, owner, initial_balance)
        self.overdraft_limit = overdraft_limit
    
    def withdraw(self, amount):
        """
        Withdraw money from the account with overdraft protection.
        
        Args:
            amount (float): Amount to withdraw
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        available_balance = self.balance + self.overdraft_limit
        if amount > available_balance:
            raise ValueError("Withdrawal exceeds available balance and overdraft limit")
        
        self.balance -= amount
```

## Run the Tests

```bash
pytest account_test.py -v
```

## Refactor: Improve the Code

Let's improve our code with better error handling and documentation:

```python
# account.py
class Account:
    """
    A basic bank account.
    """
    
    def __init__(self, account_number, owner, initial_balance=0.0):
        """
        Initialize a new account.
        
        Args:
            account_number (str): Unique account identifier
            owner (str): Account owner's name
            initial_balance (float): Initial account balance
            
        Raises:
            ValueError: If account_number or owner is empty
        """
        if not account_number:
            raise ValueError("Account number cannot be empty")
        if not owner:
            raise ValueError("Owner name cannot be empty")
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        
        self.account_number = account_number
        self.owner = owner
        self.balance = initial_balance
    
    def deposit(self, amount):
        """
        Deposit money into the account.
        
        Args:
            amount (float): Amount to deposit
            
        Raises:
            ValueError: If amount is not positive
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
    
    def withdraw(self, amount):
        """
        Withdraw money from the account.
        
        Args:
            amount (float): Amount to withdraw
            
        Raises:
            ValueError: If amount is not positive or insufficient funds
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
    
    def get_balance(self):
        """
        Get the current account balance.
        
        Returns:
            float: Current balance
        """
        return self.balance
    
    def __str__(self):
        """
        String representation of the account.
        
        Returns:
            str: Account information
        """
        return f"Account {self.account_number} ({self.owner}): ${self.balance:.2f}"

class SavingsAccount(Account):
    """
    A savings account that earns interest.
    """
    
    def __init__(self, account_number, owner, initial_balance=0.0, interest_rate=0.0):
        """
        Initialize a new savings account.
        
        Args:
            account_number (str): Unique account identifier
            owner (str): Account owner's name
            initial_balance (float): Initial account balance
            interest_rate (float): Annual interest rate
            
        Raises:
            ValueError: If interest_rate is negative
        """
        super().__init__(account_number, owner, initial_balance)
        if interest_rate < 0:
            raise ValueError("Interest rate cannot be negative")
        self.interest_rate = interest_rate
    
    def add_interest(self):
        """
        Add interest to the account balance.
        """
        interest = self.balance * self.interest_rate
        self.balance += interest
    
    def __str__(self):
        """
        String representation of the savings account.
        
        Returns:
            str: Account information with interest rate
        """
        return f"Savings Account {self.account_number} ({self.owner}): ${self.balance:.2f} (Rate: {self.interest_rate:.2%})"

class CheckingAccount(Account):
    """
    A checking account with overdraft protection.
    """
    
    def __init__(self, account_number, owner, initial_balance=0.0, overdraft_limit=0.0):
        """
        Initialize a new checking account.
        
        Args:
            account_number (str): Unique account identifier
            owner (str): Account owner's name
            initial_balance (float): Initial account balance
            overdraft_limit (float): Maximum overdraft amount
            
        Raises:
            ValueError: If overdraft_limit is negative
        """
        super().__init__(account_number, owner, initial_balance)
        if overdraft_limit < 0:
            raise ValueError("Overdraft limit cannot be negative")
        self.overdraft_limit = overdraft_limit
    
    def withdraw(self, amount):
        """
        Withdraw money from the account with overdraft protection.
        
        Args:
            amount (float): Amount to withdraw
            
        Raises:
            ValueError: If amount is not positive or exceeds available balance
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        available_balance = self.balance + self.overdraft_limit
        if amount > available_balance:
            raise ValueError("Withdrawal exceeds available balance and overdraft limit")
        
        self.balance -= amount
    
    def __str__(self):
        """
        String representation of the checking account.
        
        Returns:
            str: Account information with overdraft limit
        """
        return f"Checking Account {self.account_number} ({self.owner}): ${self.balance:.2f} (Overdraft: ${self.overdraft_limit:.2f})"
```

## Advanced Examples

Let's add some more complex functionality:

```python
# account_test.py (additional tests)
def test_transfer():
    account1 = Account("12345", "John Doe", 1000.0)
    account2 = Account("67890", "Jane Smith", 500.0)
    
    account1.transfer(account2, 200.0)
    
    assert account1.balance == 800.0
    assert account2.balance == 700.0

def test_transfer_insufficient_funds():
    account1 = Account("12345", "John Doe", 100.0)
    account2 = Account("67890", "Jane Smith", 500.0)
    
    with pytest.raises(ValueError):
        account1.transfer(account2, 200.0)

def test_account_history():
    account = Account("12345", "John Doe", 1000.0)
    account.deposit(500.0)
    account.withdraw(200.0)
    
    history = account.get_transaction_history()
    assert len(history) == 2
    assert history[0]['type'] == 'deposit'
    assert history[0]['amount'] == 500.0
    assert history[1]['type'] == 'withdrawal'
    assert history[1]['amount'] == 200.0
```

```python
# account.py (additional methods)
def transfer(self, other_account, amount):
    """
    Transfer money to another account.
    
    Args:
        other_account (Account): Destination account
        amount (float): Amount to transfer
        
    Raises:
        ValueError: If amount is not positive or insufficient funds
        TypeError: If other_account is not an Account instance
    """
    if not isinstance(other_account, Account):
        raise TypeError("Destination must be an Account instance")
    if amount <= 0:
        raise ValueError("Transfer amount must be positive")
    if amount > self.balance:
        raise ValueError("Insufficient funds for transfer")
    
    self.balance -= amount
    other_account.balance += amount

def get_transaction_history(self):
    """
    Get the transaction history for this account.
    
    Returns:
        list: List of transaction records
    """
    return getattr(self, '_transaction_history', [])

def _record_transaction(self, transaction_type, amount):
    """
    Record a transaction in the account history.
    
    Args:
        transaction_type (str): Type of transaction
        amount (float): Transaction amount
    """
    if not hasattr(self, '_transaction_history'):
        self._transaction_history = []
    
    self._transaction_history.append({
        'type': transaction_type,
        'amount': amount,
        'balance': self.balance
    })
```

## What We've Learned

1. **Classes and Objects**: Creating and using classes
2. **Inheritance**: Extending base classes
3. **Encapsulation**: Protecting data with methods
4. **Polymorphism**: Different behavior for different account types
5. **Error Handling**: Validating inputs and handling edge cases

## Exercises

1. Add a method to calculate account fees
2. Create a BusinessAccount class with different fee structure
3. Add transaction limits to accounts
4. Implement account freezing/unfreezing functionality

## Key Concepts

- **Object-Oriented Programming**: Classes, objects, and methods
- **Inheritance**: Code reuse and specialization
- **Encapsulation**: Data hiding and access control
- **Polymorphism**: Different implementations of the same interface
- **Error Handling**: Input validation and exception handling

