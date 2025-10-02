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

