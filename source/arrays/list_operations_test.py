import pytest
from list_operations import ListOperations

def test_append():
    ops = ListOperations()
    result = ops.append([1, 2, 3], 4)
    assert result == [1, 2, 3, 4]

def test_prepend():
    ops = ListOperations()
    result = ops.prepend([2, 3, 4], 1)
    assert result == [1, 2, 3, 4]

def test_remove_first():
    ops = ListOperations()
    result = ops.remove_first([1, 2, 3, 4])
    assert result == [2, 3, 4]

def test_remove_last():
    ops = ListOperations()
    result = ops.remove_last([1, 2, 3, 4])
    assert result == [1, 2, 3]

def test_find_index():
    ops = ListOperations()
    result = ops.find_index([1, 2, 3, 4], 3)
    assert result == 2

def test_find_index_not_found():
    ops = ListOperations()
    result = ops.find_index([1, 2, 3, 4], 5)
    assert result == -1

def test_slice_list():
    ops = ListOperations()
    result = ops.slice_list([1, 2, 3, 4, 5], 1, 4)
    assert result == [2, 3, 4]

def test_concatenate():
    ops = ListOperations()
    result = ops.concatenate([1, 2], [3, 4])
    assert result == [1, 2, 3, 4]

def test_remove_duplicates():
    ops = ListOperations()
    result = ops.remove_duplicates([1, 2, 2, 3, 4, 4, 5])
    assert result == [1, 2, 3, 4, 5]

def test_sort_list():
    ops = ListOperations()
    result = ops.sort_list([3, 1, 4, 1, 5, 9, 2, 6])
    assert result == [1, 1, 2, 3, 4, 5, 6, 9]

def test_reverse_list():
    ops = ListOperations()
    result = ops.reverse_list([1, 2, 3, 4, 5])
    assert result == [5, 4, 3, 2, 1]

def test_intersection():
    ops = ListOperations()
    result = ops.intersection([1, 2, 3, 4], [3, 4, 5, 6])
    assert result == [3, 4]

def test_union():
    ops = ListOperations()
    result = ops.union([1, 2, 3], [3, 4, 5])
    assert result == [1, 2, 3, 4, 5]

