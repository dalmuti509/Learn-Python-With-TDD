# Context Managers

Let's explore context managers in Python using TDD. We'll build various examples that demonstrate resource management, the `with` statement, and custom context managers.

## The Problem

We want to create a database connection system that properly manages resources, handles errors, and ensures cleanup using context managers.

## Red: Write Failing Tests

Let's start with some basic context manager tests:

```python
# context_managers_test.py
import pytest
import tempfile
import os
from context_managers import DatabaseConnection, FileManager, Timer, TransactionManager, ResourcePool

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
```

## Green: Write the Minimal Code to Pass

Now let's implement our context managers:

```python
# context_managers.py
import time
import threading
from typing import List, Optional, Any
from contextlib import contextmanager

class DatabaseConnection:
    """
    A database connection context manager.
    """
    
    def __init__(self, database_name: str):
        self.database_name = database_name
        self._connected = False
    
    def __enter__(self):
        if not self.database_name:
            raise ValueError("Database name cannot be empty")
        
        self._connected = True
        print(f"Connected to database: {self.database_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connected = False
        print(f"Disconnected from database: {self.database_name}")
        
        # Handle exceptions
        if exc_type is not None:
            print(f"Exception occurred: {exc_val}")
        
        return False  # Don't suppress exceptions
    
    def is_connected(self) -> bool:
        """Check if the connection is active."""
        return self._connected
    
    @classmethod
    def context(cls, database_name: str):
        """Context manager decorator."""
        @contextmanager
        def database_context():
            with cls(database_name) as db:
                yield db
        return database_context

class FileManager:
    """
    A file context manager that ensures proper file handling.
    """
    
    def __init__(self, filename: str, mode: str = 'r'):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        
        # Handle exceptions
        if exc_type is not None:
            print(f"File operation failed: {exc_val}")
        
        return False  # Don't suppress exceptions

class Timer:
    """
    A timer context manager.
    """
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.elapsed_time = 0.0
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        print(f"Elapsed time: {self.elapsed_time:.4f} seconds")
        return False

class TransactionManager:
    """
    A transaction context manager.
    """
    
    def __init__(self):
        self.operations = []
        self.committed = False
    
    def __enter__(self):
        self.operations = []
        self.committed = False
        print("Transaction started")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # No exception, commit transaction
            self.commit()
        else:
            # Exception occurred, rollback
            self.rollback()
            print(f"Transaction rolled back due to: {exc_val}")
        
        return False  # Don't suppress exceptions
    
    def add_operation(self, operation: str):
        """Add an operation to the transaction."""
        self.operations.append(operation)
        print(f"Added operation: {operation}")
    
    def commit(self):
        """Commit the transaction."""
        print(f"Committing {len(self.operations)} operations")
        self.committed = True
    
    def rollback(self):
        """Rollback the transaction."""
        print(f"Rolling back {len(self.operations)} operations")
        self.committed = False

class ResourcePool:
    """
    A resource pool context manager.
    """
    
    def __init__(self, max_size: int = 5):
        self.max_size = max_size
        self.available_resources = []
        self.used_resources = set()
        self.lock = threading.Lock()
    
    def get_resource(self):
        """Get a resource from the pool."""
        return ResourceContext(self)
    
    def _acquire_resource(self):
        """Acquire a resource from the pool."""
        with self.lock:
            if self.available_resources:
                resource = self.available_resources.pop()
            else:
                if len(self.used_resources) >= self.max_size:
                    raise RuntimeError("No resources available")
                resource = f"Resource_{len(self.used_resources) + 1}"
            
            self.used_resources.add(resource)
            return resource
    
    def _release_resource(self, resource):
        """Release a resource back to the pool."""
        with self.lock:
            if resource in self.used_resources:
                self.used_resources.remove(resource)
                self.available_resources.append(resource)

class ResourceContext:
    """
    Context manager for individual resources.
    """
    
    def __init__(self, pool: ResourcePool):
        self.pool = pool
        self.resource = None
    
    def __enter__(self):
        self.resource = self.pool._acquire_resource()
        return self.resource
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.resource:
            self.pool._release_resource(self.resource)
        return False
```

## Run the Tests

```bash
pytest context_managers_test.py -v
```

## Refactor: Improve the Code

Let's improve our code with better error handling and additional features:

```python
# context_managers.py
import time
import threading
import logging
from typing import List, Optional, Any, Generator
from contextlib import contextmanager, ExitStack

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """
    A database connection context manager with proper error handling.
    """
    
    def __init__(self, database_name: str, connection_timeout: float = 5.0):
        self.database_name = database_name
        self.connection_timeout = connection_timeout
        self._connected = False
        self._connection_id = None
    
    def __enter__(self):
        if not self.database_name:
            raise ValueError("Database name cannot be empty")
        
        start_time = time.time()
        while time.time() - start_time < self.connection_timeout:
            try:
                self._connection_id = f"conn_{int(time.time())}"
                self._connected = True
                logger.info(f"Connected to database: {self.database_name} (ID: {self._connection_id})")
                return self
            except Exception as e:
                logger.warning(f"Connection attempt failed: {e}")
                time.sleep(0.1)
        
        raise ConnectionError(f"Failed to connect to {self.database_name} within {self.connection_timeout} seconds")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connected = False
        logger.info(f"Disconnected from database: {self.database_name} (ID: {self._connection_id})")
        
        # Handle exceptions
        if exc_type is not None:
            logger.error(f"Database operation failed: {exc_val}")
        
        return False  # Don't suppress exceptions
    
    def is_connected(self) -> bool:
        """Check if the connection is active."""
        return self._connected
    
    def execute_query(self, query: str) -> str:
        """Execute a database query."""
        if not self._connected:
            raise RuntimeError("Database connection is not active")
        return f"Executed: {query}"
    
    @classmethod
    def context(cls, database_name: str):
        """Context manager decorator."""
        @contextmanager
        def database_context():
            with cls(database_name) as db:
                yield db
        return database_context

class FileManager:
    """
    A file context manager with enhanced error handling.
    """
    
    def __init__(self, filename: str, mode: str = 'r', encoding: str = 'utf-8'):
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.file = None
    
    def __enter__(self):
        try:
            self.file = open(self.filename, self.mode, encoding=self.encoding)
            logger.info(f"Opened file: {self.filename} in mode: {self.mode}")
            return self.file
        except FileNotFoundError:
            logger.error(f"File not found: {self.filename}")
            raise
        except PermissionError:
            logger.error(f"Permission denied: {self.filename}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
            logger.info(f"Closed file: {self.filename}")
        
        # Handle exceptions
        if exc_type is not None:
            logger.error(f"File operation failed: {exc_val}")
        
        return False  # Don't suppress exceptions

class Timer:
    """
    A timer context manager with detailed timing information.
    """
    
    def __init__(self, name: str = "Timer"):
        self.name = name
        self.start_time = None
        self.end_time = None
        self.elapsed_time = 0.0
    
    def __enter__(self):
        self.start_time = time.time()
        logger.info(f"{self.name} started")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        logger.info(f"{self.name} completed in {self.elapsed_time:.4f} seconds")
        return False
    
    def get_elapsed_time(self) -> float:
        """Get the elapsed time."""
        if self.start_time is None:
            return 0.0
        current_time = time.time()
        return current_time - self.start_time

class TransactionManager:
    """
    A transaction context manager with rollback capabilities.
    """
    
    def __init__(self, auto_commit: bool = True):
        self.operations = []
        self.committed = False
        self.auto_commit = auto_commit
    
    def __enter__(self):
        self.operations = []
        self.committed = False
        logger.info("Transaction started")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # No exception, commit transaction
            if self.auto_commit:
                self.commit()
        else:
            # Exception occurred, rollback
            self.rollback()
            logger.error(f"Transaction rolled back due to: {exc_val}")
        
        return False  # Don't suppress exceptions
    
    def add_operation(self, operation: str):
        """Add an operation to the transaction."""
        self.operations.append(operation)
        logger.info(f"Added operation: {operation}")
    
    def commit(self):
        """Commit the transaction."""
        logger.info(f"Committing {len(self.operations)} operations")
        self.committed = True
    
    def rollback(self):
        """Rollback the transaction."""
        logger.info(f"Rolling back {len(self.operations)} operations")
        self.committed = False

class ResourcePool:
    """
    A thread-safe resource pool context manager.
    """
    
    def __init__(self, max_size: int = 5, resource_factory=None):
        self.max_size = max_size
        self.resource_factory = resource_factory or (lambda: f"Resource_{int(time.time())}")
        self.available_resources = []
        self.used_resources = set()
        self.lock = threading.Lock()
        self.resource_counter = 0
    
    def get_resource(self):
        """Get a resource from the pool."""
        return ResourceContext(self)
    
    def _acquire_resource(self):
        """Acquire a resource from the pool."""
        with self.lock:
            if self.available_resources:
                resource = self.available_resources.pop()
            else:
                if len(self.used_resources) >= self.max_size:
                    raise RuntimeError("No resources available")
                self.resource_counter += 1
                resource = self.resource_factory()
            
            self.used_resources.add(resource)
            logger.info(f"Acquired resource: {resource}")
            return resource
    
    def _release_resource(self, resource):
        """Release a resource back to the pool."""
        with self.lock:
            if resource in self.used_resources:
                self.used_resources.remove(resource)
                self.available_resources.append(resource)
                logger.info(f"Released resource: {resource}")

class ResourceContext:
    """
    Context manager for individual resources.
    """
    
    def __init__(self, pool: ResourcePool):
        self.pool = pool
        self.resource = None
    
    def __enter__(self):
        self.resource = self.pool._acquire_resource()
        return self.resource
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.resource:
            self.pool._release_resource(self.resource)
        return False

@contextmanager
def multiple_files(*filenames):
    """
    Context manager for multiple files.
    
    Args:
        *filenames: File paths to open
        
    Yields:
        List of file objects
    """
    files = []
    try:
        for filename in filenames:
            files.append(open(filename, 'r'))
        yield files
    finally:
        for file in files:
            file.close()

@contextmanager
def temporary_file(content: str = ""):
    """
    Context manager for temporary files.
    
    Args:
        content: Content to write to the file
        
    Yields:
        str: Path to the temporary file
    """
    import tempfile
    import os
    
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    try:
        temp_file.write(content)
        temp_file.close()
        yield temp_file.name
    finally:
        os.unlink(temp_file.name)
```

## Advanced Examples

Let's add some more sophisticated context manager patterns:

```python
# context_managers_test.py (additional tests)
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
```

## What We've Learned

1. **Context Managers**: Objects that define `__enter__` and `__exit__` methods
2. **Resource Management**: Automatic cleanup of resources
3. **Exception Handling**: Proper error handling in context managers
4. **Nested Contexts**: Managing multiple resources simultaneously
5. **Context Manager Decorators**: Using `@contextmanager` for simple cases

## Exercises

1. Create a context manager for database transactions
2. Implement a context manager for temporary directories
3. Build a context manager that measures memory usage
4. Create a context manager for API rate limiting

## Key Concepts

- **Context Managers**: Objects that manage resources with `with` statements
- **Resource Management**: Automatic cleanup and error handling
- **Exception Safety**: Proper handling of exceptions in context managers
- **Nested Contexts**: Managing multiple resources together
- **Context Manager Decorators**: Simple context managers using `@contextmanager`

