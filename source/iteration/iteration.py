def sum_numbers(numbers):
    """
    Sum all numbers in a list.
    
    Args:
        numbers (list): List of numbers to sum
        
    Returns:
        int: Sum of all numbers
    """
    return sum(numbers)

def find_max(numbers):
    """
    Find the maximum number in a list.
    
    Args:
        numbers (list): List of numbers
        
    Returns:
        int: Maximum number
        
    Raises:
        ValueError: If the list is empty
    """
    if not numbers:
        raise ValueError("Cannot find max of empty list")
    
    return max(numbers)

def count_occurrences(numbers, target):
    """
    Count how many times a target number appears in a list.
    
    Args:
        numbers (list): List of numbers to search
        target (int): Number to count
        
    Returns:
        int: Number of occurrences
    """
    return numbers.count(target)

def reverse_list(numbers):
    """
    Reverse a list of numbers.
    
    Args:
        numbers (list): List to reverse
        
    Returns:
        list: Reversed list
    """
    return numbers[::-1]

def filter_even_numbers(numbers):
    """
    Filter out odd numbers, keeping only even numbers.
    
    Args:
        numbers (list): List of numbers to filter
        
    Returns:
        list: List of even numbers
    """
    return [num for num in numbers if num % 2 == 0]

def map_square(numbers):
    """
    Square each number in a list.
    
    Args:
        numbers (list): List of numbers to square
        
    Returns:
        list: List of squared numbers
    """
    return [num ** 2 for num in numbers]

def find_duplicates(numbers):
    """
    Find duplicate numbers in a list.
    
    Args:
        numbers (list): List of numbers to check
        
    Returns:
        list: List of duplicate numbers
    """
    seen = set()
    duplicates = set()
    
    for num in numbers:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
    
    return list(duplicates)

def group_by_parity(numbers):
    """
    Group numbers by whether they are odd or even.
    
    Args:
        numbers (list): List of numbers to group
        
    Returns:
        dict: Dictionary with 'odd' and 'even' keys
    """
    result = {'odd': [], 'even': []}
    
    for num in numbers:
        if num % 2 == 0:
            result['even'].append(num)
        else:
            result['odd'].append(num)
    
    return result

