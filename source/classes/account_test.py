def test_account_creation():
    account = Account("John", 1000)
    assert account.owner == "John"
    assert account.balance == 1000

def test_deposit():
    account = Account("John", 1000)
    account.deposit(500)
    assert account.balance == 1500

def test_withdraw():
    account = Account("John", 1000)
    account.withdraw(300)
    assert account.balance == 700




