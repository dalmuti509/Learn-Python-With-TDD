import pytest

def test_read_existing_file():
    # Create a test file first
    with open("test.txt", "w") as f:
        f.write("Hello, World!")
    
    result = read_file("test.txt")
    assert result == "Hello, World!"

def test_read_nonexistent_file():
    result = read_file("nonexistent.txt")
    assert result is None

def test_validate_file_extension():
    with pytest.raises(InvalidFileTypeError):
        validate_file("document.pdf")




