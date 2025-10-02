#!/usr/bin/env python3
"""
Tests for Sets & Data Structures chapter.
Learn Python with Tests - Advanced Data Structures
"""

import pytest
from collections import Counter, deque, namedtuple
from data_structures import DataStructures


class TestSets:
    """Test set operations and functionality."""
    
    def test_get_unique_items_from_list(self):
        """Should return unique items as a set."""
        ds = DataStructures()
        result = ds.get_unique_items([1, 2, 2, 3, 3, 4, 1])
        assert result == {1, 2, 3, 4}
        assert isinstance(result, set)
    
    def test_get_unique_items_empty_list(self):
        """Should return empty set for empty list."""
        ds = DataStructures()
        result = ds.get_unique_items([])
        assert result == set()
    
    def test_find_common_elements(self):
        """Should find intersection of two sets."""
        ds = DataStructures()
        set1 = {1, 2, 3, 4}
        set2 = {3, 4, 5, 6}
        result = ds.find_common_elements(set1, set2)
        assert result == {3, 4}
    
    def test_find_common_elements_no_overlap(self):
        """Should return empty set when no common elements."""
        ds = DataStructures()
        set1 = {1, 2, 3}
        set2 = {4, 5, 6}
        result = ds.find_common_elements(set1, set2)
        assert result == set()
    
    def test_union_sets(self):
        """Should return union of two sets."""
        ds = DataStructures()
        set1 = {1, 2, 3}
        set2 = {3, 4, 5}
        result = ds.union_sets(set1, set2)
        assert result == {1, 2, 3, 4, 5}
    
    def test_difference_sets(self):
        """Should return elements in first set but not second."""
        ds = DataStructures()
        set1 = {1, 2, 3, 4}
        set2 = {3, 4, 5, 6}
        result = ds.difference_sets(set1, set2)
        assert result == {1, 2}


class TestTuples:
    """Test tuple and named tuple functionality."""
    
    def test_create_person_named_tuple(self):
        """Should create a Person named tuple."""
        ds = DataStructures()
        person = ds.create_person("Alice", 30, "Engineer")
        
        assert person.name == "Alice"
        assert person.age == 30
        assert person.job == "Engineer"
        assert hasattr(person, '_fields')  # Named tuple characteristic
    
    def test_create_coordinate_tuple(self):
        """Should create coordinate tuple."""
        ds = DataStructures()
        coord = ds.create_coordinate(10.5, 20.3)
        
        assert coord.x == 10.5
        assert coord.y == 20.3
    
    def test_tuple_immutability(self):
        """Should demonstrate tuple immutability."""
        ds = DataStructures()
        person = ds.create_person("Bob", 25, "Designer")
        
        # Should not be able to modify
        with pytest.raises(AttributeError):
            person.name = "Charlie"


class TestCounter:
    """Test Counter functionality for frequency analysis."""
    
    def test_count_words(self):
        """Should count word frequencies."""
        ds = DataStructures()
        text = "hello world hello python world"
        result = ds.count_words(text)
        
        expected = Counter({'hello': 2, 'world': 2, 'python': 1})
        assert result == expected
    
    def test_count_characters(self):
        """Should count character frequencies."""
        ds = DataStructures()
        text = "hello"
        result = ds.count_characters(text)
        
        expected = Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})
        assert result == expected
    
    def test_most_common_items(self):
        """Should return most common items."""
        ds = DataStructures()
        items = ['a', 'b', 'a', 'c', 'b', 'a']
        result = ds.most_common_items(items, 2)
        
        # Should return list of tuples: [('a', 3), ('b', 2)]
        assert result == [('a', 3), ('b', 2)]


class TestDeque:
    """Test deque (double-ended queue) functionality."""
    
    def test_create_queue(self):
        """Should create an empty deque."""
        ds = DataStructures()
        queue = ds.create_queue()
        
        assert isinstance(queue, deque)
        assert len(queue) == 0
    
    def test_enqueue_and_dequeue(self):
        """Should add and remove items from queue (FIFO)."""
        ds = DataStructures()
        queue = ds.create_queue()
        
        ds.enqueue(queue, "first")
        ds.enqueue(queue, "second")
        ds.enqueue(queue, "third")
        
        assert ds.dequeue(queue) == "first"
        assert ds.dequeue(queue) == "second"
        assert len(queue) == 1
    
    def test_stack_operations(self):
        """Should support stack operations (LIFO)."""
        ds = DataStructures()
        stack = ds.create_queue()  # Same structure, different usage
        
        ds.push(stack, "bottom")
        ds.push(stack, "middle")
        ds.push(stack, "top")
        
        assert ds.pop(stack) == "top"
        assert ds.pop(stack) == "middle"
        assert len(stack) == 1
    
    def test_dequeue_empty_queue(self):
        """Should handle empty queue gracefully."""
        ds = DataStructures()
        queue = ds.create_queue()
        
        with pytest.raises(IndexError):
            ds.dequeue(queue)


class TestDefaultDict:
    """Test defaultdict functionality."""
    
    def test_group_by_length(self):
        """Should group words by their length using defaultdict."""
        ds = DataStructures()
        words = ["cat", "dog", "elephant", "ant", "horse"]
        result = ds.group_by_length(words)
        
        expected = {
            3: ["cat", "dog", "ant"],
            8: ["elephant"],
            5: ["horse"]
        }
        
        # Convert to regular dict for comparison
        assert dict(result) == expected
    
    def test_count_by_first_letter(self):
        """Should count words by their first letter."""
        ds = DataStructures()
        words = ["apple", "banana", "cherry", "apricot", "blueberry"]
        result = ds.count_by_first_letter(words)
        
        expected = {'a': 2, 'b': 2, 'c': 1}
        assert dict(result) == expected


class TestAdvancedOperations:
    """Test advanced data structure operations."""
    
    def test_find_duplicates(self):
        """Should find duplicate items in a list."""
        ds = DataStructures()
        items = [1, 2, 3, 2, 4, 3, 5]
        result = ds.find_duplicates(items)
        
        assert result == {2, 3}
    
    def test_is_subset(self):
        """Should check if one set is subset of another."""
        ds = DataStructures()
        set1 = {1, 2, 3}
        set2 = {1, 2, 3, 4, 5}
        
        assert ds.is_subset(set1, set2) is True
        assert ds.is_subset(set2, set1) is False
    
    def test_symmetric_difference(self):
        """Should find elements in either set but not both."""
        ds = DataStructures()
        set1 = {1, 2, 3, 4}
        set2 = {3, 4, 5, 6}
        result = ds.symmetric_difference(set1, set2)
        
        assert result == {1, 2, 5, 6}
    
    def test_merge_counters(self):
        """Should merge multiple counters."""
        ds = DataStructures()
        counter1 = Counter({'a': 3, 'b': 1})
        counter2 = Counter({'a': 1, 'c': 2})
        result = ds.merge_counters([counter1, counter2])
        
        expected = Counter({'a': 4, 'b': 1, 'c': 2})
        assert result == expected


if __name__ == '__main__':
    pytest.main([__file__])
