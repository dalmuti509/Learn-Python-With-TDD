# Exceptions and Error Handling

Let's explore exception handling in Python using TDD. We'll build various functions that demonstrate different types of error handling and custom exceptions.

## The Problem

We want to create a file processing system that handles various types of errors gracefully.

## Red: Write Failing Tests

Let's start with some basic error handling:

```python
# file_processor_test.py
import pytest
from file_processor import FileProcessor, FileNotFoundError, InvalidFileFormatError, ProcessingError

def test_read_file_success():
    processor = FileProcessor()
    result = processor.read_file("test.txt")
    assert result == "Hello, World!"

def test_read_file_not_found():
    processor = FileProcessor()
    with pytest.raises(FileNotFoundError):
        processor.read_file("nonexistent.txt")

def test_read_file_invalid_format():
    processor = FileProcessor()
    with pytest.raises(InvalidFileFormatError):
        processor.read_file("test.bin")

def test_process_file_success():
    processor = FileProcessor()
    result = processor.process_file("test.txt")
    assert result == "HELLO, WORLD!"

def test_process_file_processing_error():
    processor = FileProcessor()
    with pytest.raises(ProcessingError):
        processor.process_file("error.txt")

def test_safe_read_file():
    processor = FileProcessor()
    result = processor.safe_read_file("test.txt")
    assert result == "Hello, World!"

def test_safe_read_file_not_found():
    processor = FileProcessor()
    result = processor.safe_read_file("nonexistent.txt")
    assert result is None

def test_validate_file_extension():
    processor = FileProcessor()
    assert processor.validate_file_extension("test.txt") == True
    assert processor.validate_file_extension("test.bin") == False

def test_validate_file_size():
    processor = FileProcessor()
    assert processor.validate_file_size("test.txt") == True
    with pytest.raises(ValueError):
        processor.validate_file_size("large.txt")
```

## Green: Write the Minimal Code to Pass

Now let's implement our file processor with error handling:

```python
# file_processor.py
import os

class FileNotFoundError(Exception):
    """Raised when a file is not found."""
    pass

class InvalidFileFormatError(Exception):
    """Raised when a file has an invalid format."""
    pass

class ProcessingError(Exception):
    """Raised when file processing fails."""
    pass

class FileProcessor:
    """
    A file processor that handles various file operations with error handling.
    """
    
    def __init__(self):
        self.supported_extensions = ['.txt', '.csv', '.json']
        self.max_file_size = 1024 * 1024  # 1MB
    
    def read_file(self, filename):
        """
        Read a file and return its contents.
        
        Args:
            filename (str): Path to the file
            
        Returns:
            str: File contents
            
        Raises:
            FileNotFoundError: If file doesn't exist
            InvalidFileFormatError: If file format is not supported
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")
        
        if not self.validate_file_extension(filename):
            raise InvalidFileFormatError(f"Unsupported file format: {filename}")
        
        with open(filename, 'r') as file:
            return file.read()
    
    def process_file(self, filename):
        """
        Process a file and return the processed content.
        
        Args:
            filename (str): Path to the file
            
        Returns:
            str: Processed file contents
            
        Raises:
            ProcessingError: If processing fails
        """
        try:
            content = self.read_file(filename)
            if "error" in content.lower():
                raise ProcessingError("File contains error content")
            return content.upper()
        except (FileNotFoundError, InvalidFileFormatError):
            raise
        except Exception as e:
            raise ProcessingError(f"Processing failed: {str(e)}")
    
    def safe_read_file(self, filename):
        """
        Safely read a file, returning None if it fails.
        
        Args:
            filename (str): Path to the file
            
        Returns:
            str or None: File contents or None if failed
        """
        try:
            return self.read_file(filename)
        except (FileNotFoundError, InvalidFileFormatError):
            return None
    
    def validate_file_extension(self, filename):
        """
        Validate if a file has a supported extension.
        
        Args:
            filename (str): Path to the file
            
        Returns:
            bool: True if extension is supported
        """
        _, ext = os.path.splitext(filename)
        return ext.lower() in self.supported_extensions
    
    def validate_file_size(self, filename):
        """
        Validate if a file size is within limits.
        
        Args:
            filename (str): Path to the file
            
        Returns:
            bool: True if file size is valid
            
        Raises:
            ValueError: If file size exceeds limit
        """
        if not os.path.exists(filename):
            return False
        
        file_size = os.path.getsize(filename)
        if file_size > self.max_file_size:
            raise ValueError(f"File size {file_size} exceeds limit {self.max_file_size}")
        
        return True
```

## Run the Tests

```bash
pytest file_processor_test.py -v
```

## Refactor: Improve the Code

Let's improve our code with better error handling and logging:

```python
# file_processor.py
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileNotFoundError(Exception):
    """Raised when a file is not found."""
    pass

class InvalidFileFormatError(Exception):
    """Raised when a file has an invalid format."""
    pass

class ProcessingError(Exception):
    """Raised when file processing fails."""
    pass

class FileProcessor:
    """
    A file processor that handles various file operations with error handling.
    """
    
    def __init__(self, max_file_size=1024 * 1024):
        """
        Initialize the file processor.
        
        Args:
            max_file_size (int): Maximum file size in bytes
        """
        self.supported_extensions = ['.txt', '.csv', '.json']
        self.max_file_size = max_file_size
    
    def read_file(self, filename):
        """
        Read a file and return its contents.
        
        Args:
            filename (str): Path to the file
            
        Returns:
            str: File contents
            
        Raises:
            FileNotFoundError: If file doesn't exist
            InvalidFileFormatError: If file format is not supported
        """
        logger.info(f"Attempting to read file: {filename}")
        
        if not os.path.exists(filename):
            logger.error(f"File not found: {filename}")
            raise FileNotFoundError(f"File not found: {filename}")
        
        if not self.validate_file_extension(filename):
            logger.error(f"Unsupported file format: {filename}")
            raise InvalidFileFormatError(f"Unsupported file format: {filename}")
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                logger.info(f"Successfully read file: {filename}")
                return content
        except UnicodeDecodeError as e:
            logger.error(f"Unicode decode error for {filename}: {e}")
            raise InvalidFileFormatError(f"File encoding error: {filename}")
        except Exception as e:
            logger.error(f"Unexpected error reading {filename}: {e}")
            raise ProcessingError(f"Failed to read file: {filename}")
    
    def process_file(self, filename):
        """
        Process a file and return the processed content.
        
        Args:
            filename (str): Path to the file
            
        Returns:
            str: Processed file contents
            
        Raises:
            ProcessingError: If processing fails
        """
        logger.info(f"Processing file: {filename}")
        
        try:
            content = self.read_file(filename)
            if "error" in content.lower():
                logger.error(f"File contains error content: {filename}")
                raise ProcessingError("File contains error content")
            
            processed_content = content.upper()
            logger.info(f"Successfully processed file: {filename}")
            return processed_content
            
        except (FileNotFoundError, InvalidFileFormatError):
            logger.error(f"File validation failed for {filename}")
            raise
        except Exception as e:
            logger.error(f"Processing failed for {filename}: {e}")
            raise ProcessingError(f"Processing failed: {str(e)}")
    
    def safe_read_file(self, filename):
        """
        Safely read a file, returning None if it fails.
        
        Args:
            filename (str): Path to the file
            
        Returns:
            str or None: File contents or None if failed
        """
        try:
            return self.read_file(filename)
        except (FileNotFoundError, InvalidFileFormatError, ProcessingError) as e:
            logger.warning(f"Safe read failed for {filename}: {e}")
            return None
    
    def validate_file_extension(self, filename):
        """
        Validate if a file has a supported extension.
        
        Args:
            filename (str): Path to the file
            
        Returns:
            bool: True if extension is supported
        """
        _, ext = os.path.splitext(filename)
        return ext.lower() in self.supported_extensions
    
    def validate_file_size(self, filename):
        """
        Validate if a file size is within limits.
        
        Args:
            filename (str): Path to the file
            
        Returns:
            bool: True if file size is valid
            
        Raises:
            ValueError: If file size exceeds limit
        """
        if not os.path.exists(filename):
            return False
        
        file_size = os.path.getsize(filename)
        if file_size > self.max_file_size:
            logger.error(f"File size {file_size} exceeds limit {self.max_file_size} for {filename}")
            raise ValueError(f"File size {file_size} exceeds limit {self.max_file_size}")
        
        return True
```

## Advanced Examples

Let's add some more complex error handling:

```python
# file_processor_test.py (additional tests)
def test_batch_process_files():
    processor = FileProcessor()
    filenames = ["test1.txt", "test2.txt", "error.txt"]
    results = processor.batch_process_files(filenames)
    
    assert len(results) == 3
    assert results[0]['success'] == True
    assert results[1]['success'] == True
    assert results[2]['success'] == False
    assert 'error' in results[2]['error'].lower()

def test_retry_mechanism():
    processor = FileProcessor()
    result = processor.read_file_with_retry("test.txt", max_retries=3)
    assert result == "Hello, World!"

def test_context_manager():
    processor = FileProcessor()
    with processor.open_file("test.txt") as file:
        content = file.read()
        assert content == "Hello, World!"
```

```python
# file_processor.py (additional methods)
import time
from contextlib import contextmanager

def batch_process_files(self, filenames):
    """
    Process multiple files and return results with error information.
    
    Args:
        filenames (list): List of file paths
        
    Returns:
        list: List of dictionaries with success status and results/errors
    """
    results = []
    
    for filename in filenames:
        try:
            content = self.process_file(filename)
            results.append({
                'filename': filename,
                'success': True,
                'content': content
            })
        except Exception as e:
            results.append({
                'filename': filename,
                'success': False,
                'error': str(e)
            })
    
    return results

def read_file_with_retry(self, filename, max_retries=3, delay=1):
    """
    Read a file with retry mechanism.
    
    Args:
        filename (str): Path to the file
        max_retries (int): Maximum number of retries
        delay (float): Delay between retries in seconds
        
    Returns:
        str: File contents
        
    Raises:
        FileNotFoundError: If file is not found after all retries
    """
    for attempt in range(max_retries):
        try:
            return self.read_file(filename)
        except FileNotFoundError:
            if attempt == max_retries - 1:
                raise
            logger.warning(f"File not found, retrying in {delay} seconds... (attempt {attempt + 1})")
            time.sleep(delay)
        except Exception as e:
            logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
            raise

@contextmanager
def open_file(self, filename):
    """
    Context manager for opening files.
    
    Args:
        filename (str): Path to the file
        
    Yields:
        file: Open file object
    """
    try:
        file = open(filename, 'r', encoding='utf-8')
        yield file
    except Exception as e:
        logger.error(f"Error opening file {filename}: {e}")
        raise
    finally:
        if 'file' in locals():
            file.close()
```

## What We've Learned

1. **Custom Exceptions**: Creating specific exception types
2. **Exception Handling**: Using try/except blocks
3. **Error Logging**: Recording errors for debugging
4. **Retry Mechanisms**: Handling transient failures
5. **Context Managers**: Safe resource management

## Exercises

1. Add a method to validate file permissions
2. Implement a circuit breaker pattern for file operations
3. Add support for different file encodings
4. Create a file watcher that monitors file changes

## Key Concepts

- **Exception Handling**: Catching and handling errors gracefully
- **Custom Exceptions**: Creating specific error types
- **Logging**: Recording application events and errors
- **Retry Logic**: Handling transient failures
- **Resource Management**: Safe handling of file resources

