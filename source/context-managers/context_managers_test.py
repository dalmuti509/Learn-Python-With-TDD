import pytest
import tempfile
import os
from context_managers import (DatabaseConnection, FileManager, Timer, TransactionManager, 
                            ResourcePool, multiple_files, temporary_file)
from contextlib import ExitStack

def test_database_connection():
    with DatabaseConnection("test_db") as db:
        assert db.is_connected() == True
        assert db.database_name == "test_db"
    
    # Connection should be closed after context
    assert db.is_connected() == False

def test_database_connection_with_error():
    with pytest.raises(ValueError):
        with DatabaseConnection("") as db:
            pass

def test_file_manager():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write("Hello, World!")
        temp_file_path = temp_file.name
    
    with FileManager(temp_file_path, 'r') as file:
        content = file.read()
        assert content == "Hello, World!"
    
    # File should be closed
    assert file.closed == True
    
    # Cleanup
    os.unlink(temp_file_path)

def test_timer_context_manager():
    with Timer() as timer:
        import time
        time.sleep(0.1)
    
    assert timer.elapsed_time > 0
    assert timer.elapsed_time < 1.0

def test_transaction_manager():
    with TransactionManager() as tx:
        tx.add_operation("INSERT INTO users VALUES (1, 'John')")
        tx.add_operation("UPDATE users SET name = 'Jane' WHERE id = 1")
        assert len(tx.operations) == 2
    
    # Transaction should be committed
    assert tx.committed == True

def test_transaction_manager_rollback():
    with pytest.raises(ValueError):
        with TransactionManager() as tx:
            tx.add_operation("INSERT INTO users VALUES (1, 'John')")
            raise ValueError("Simulated error")
    
    # Transaction should be rolled back
    assert tx.committed == False

def test_resource_pool():
    pool = ResourcePool(max_size=2)
    
    with pool.get_resource() as resource1:
        assert resource1 is not None
        with pool.get_resource() as resource2:
            assert resource2 is not None
            assert resource1 != resource2
    
    # Resources should be returned to pool
    assert len(pool.available_resources) == 2

def test_resource_pool_exhausted():
    pool = ResourcePool(max_size=1)
    
    with pool.get_resource() as resource1:
        with pytest.raises(RuntimeError):
            with pool.get_resource() as resource2:
                pass

def test_nested_context_managers():
    with DatabaseConnection("db1") as db1:
        with DatabaseConnection("db2") as db2:
            assert db1.is_connected() == True
            assert db2.is_connected() == True
    
    assert db1.is_connected() == False
    assert db2.is_connected() == False

def test_context_manager_decorator():
    @DatabaseConnection.context
    def database_operation(db):
        return db.database_name
    
    result = database_operation("test_db")
    assert result == "test_db"

def test_multiple_files():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f1:
        f1.write("File 1 content")
        f1_path = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f2:
        f2.write("File 2 content")
        f2_path = f2.name
    
    try:
        with multiple_files(f1_path, f2_path) as files:
            assert len(files) == 2
            assert files[0].read() == "File 1 content"
            assert files[1].read() == "File 2 content"
    finally:
        os.unlink(f1_path)
        os.unlink(f2_path)

def test_temporary_file():
    with temporary_file("Hello, World!") as temp_path:
        with open(temp_path, 'r') as f:
            content = f.read()
            assert content == "Hello, World!"
    
    # File should be deleted
    assert not os.path.exists(temp_path)

def test_exit_stack():
    with ExitStack() as stack:
        db1 = stack.enter_context(DatabaseConnection("db1"))
        db2 = stack.enter_context(DatabaseConnection("db2"))
        
        assert db1.is_connected() == True
        assert db2.is_connected() == True
    
    assert db1.is_connected() == False
    assert db2.is_connected() == False

