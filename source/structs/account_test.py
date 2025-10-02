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

