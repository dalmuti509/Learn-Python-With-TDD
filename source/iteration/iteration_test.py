import pytest
from iteration import (sum_numbers, find_max, count_occurrences, reverse_list,
                      filter_even_numbers, map_square, find_duplicates, group_by_parity)

def test_sum_numbers():
    numbers = [1, 2, 3, 4, 5]
    result = sum_numbers(numbers)
    assert result == 15

def test_sum_empty_list():
    result = sum_numbers([])
    assert result == 0

def test_find_max():
    numbers = [3, 7, 2, 9, 1]
    result = find_max(numbers)
    assert result == 9

def test_find_max_empty_list():
    with pytest.raises(ValueError):
        find_max([])

def test_count_occurrences():
    numbers = [1, 2, 2, 3, 2, 4]
    result = count_occurrences(numbers, 2)
    assert result == 3

def test_reverse_list():
    numbers = [1, 2, 3, 4, 5]
    result = reverse_list(numbers)
    assert result == [5, 4, 3, 2, 1]

def test_filter_even_numbers():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = filter_even_numbers(numbers)
    assert result == [2, 4, 6, 8, 10]

def test_map_square():
    numbers = [1, 2, 3, 4, 5]
    result = map_square(numbers)
    assert result == [1, 4, 9, 16, 25]

def test_find_duplicates():
    numbers = [1, 2, 2, 3, 4, 4, 5]
    result = find_duplicates(numbers)
    assert result == [2, 4]

def test_group_by_parity():
    numbers = [1, 2, 3, 4, 5, 6]
    result = group_by_parity(numbers)
    assert result == {'odd': [1, 3, 5], 'even': [2, 4, 6]}

