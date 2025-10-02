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

