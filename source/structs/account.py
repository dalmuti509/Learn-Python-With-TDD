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

