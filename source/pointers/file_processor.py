import os
import logging
import time
from contextlib import contextmanager

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

