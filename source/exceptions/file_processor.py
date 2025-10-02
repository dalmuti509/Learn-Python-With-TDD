class InvalidFileTypeError(Exception):
    pass

def read_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None

def validate_file(filename):
    if not filename.endswith('.txt'):
        raise InvalidFileTypeError("Only .txt files are allowed")




