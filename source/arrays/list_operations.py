class ListOperations:
    """
    A class that provides various list operations.
    """
    
    def append(self, lst, item):
        """
        Append an item to the end of a list.
        
        Args:
            lst (list): The list to append to
            item: The item to append
            
        Returns:
            list: New list with item appended
        """
        if not isinstance(lst, list):
            raise TypeError("First argument must be a list")
        return lst + [item]
    
    def prepend(self, lst, item):
        """
        Prepend an item to the beginning of a list.
        
        Args:
            lst (list): The list to prepend to
            item: The item to prepend
            
        Returns:
            list: New list with item prepended
        """
        if not isinstance(lst, list):
            raise TypeError("First argument must be a list")
        return [item] + lst
    
    def remove_first(self, lst):
        """
        Remove the first element from a list.
        
        Args:
            lst (list): The list to remove from
            
        Returns:
            list: New list without first element
        """
        if not isinstance(lst, list):
            raise TypeError("Argument must be a list")
        if not lst:
            return []
        return lst[1:]
    
    def remove_last(self, lst):
        """
        Remove the last element from a list.
        
        Args:
            lst (list): The list to remove from
            
        Returns:
            list: New list without last element
        """
        if not isinstance(lst, list):
            raise TypeError("Argument must be a list")
        if not lst:
            return []
        return lst[:-1]
    
    def find_index(self, lst, item):
        """
        Find the index of an item in a list.
        
        Args:
            lst (list): The list to search
            item: The item to find
            
        Returns:
            int: Index of item, or -1 if not found
        """
        if not isinstance(lst, list):
            raise TypeError("First argument must be a list")
        try:
            return lst.index(item)
        except ValueError:
            return -1
    
    def slice_list(self, lst, start, end):
        """
        Slice a list from start to end index.
        
        Args:
            lst (list): The list to slice
            start (int): Start index
            end (int): End index
            
        Returns:
            list: Sliced list
        """
        if not isinstance(lst, list):
            raise TypeError("First argument must be a list")
        if not isinstance(start, int) or not isinstance(end, int):
            raise TypeError("Start and end must be integers")
        return lst[start:end]
    
    def concatenate(self, lst1, lst2):
        """
        Concatenate two lists.
        
        Args:
            lst1 (list): First list
            lst2 (list): Second list
            
        Returns:
            list: Concatenated list
        """
        if not isinstance(lst1, list) or not isinstance(lst2, list):
            raise TypeError("Both arguments must be lists")
        return lst1 + lst2
    
    def remove_duplicates(self, lst):
        """
        Remove duplicate elements from a list.
        
        Args:
            lst (list): The list to remove duplicates from
            
        Returns:
            list: List without duplicates
        """
        if not isinstance(lst, list):
            raise TypeError("Argument must be a list")
        
        seen = set()
        result = []
        for item in lst:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    def sort_list(self, lst):
        """
        Sort a list in ascending order.
        
        Args:
            lst (list): The list to sort
            
        Returns:
            list: Sorted list
        """
        if not isinstance(lst, list):
            raise TypeError("Argument must be a list")
        return sorted(lst)
    
    def reverse_list(self, lst):
        """
        Reverse a list.
        
        Args:
            lst (list): The list to reverse
            
        Returns:
            list: Reversed list
        """
        if not isinstance(lst, list):
            raise TypeError("Argument must be a list")
        return lst[::-1]
    
    def intersection(self, lst1, lst2):
        """
        Find the intersection of two lists.
        
        Args:
            lst1 (list): First list
            lst2 (list): Second list
            
        Returns:
            list: List of common elements
        """
        if not isinstance(lst1, list) or not isinstance(lst2, list):
            raise TypeError("Both arguments must be lists")
        
        set1 = set(lst1)
        set2 = set(lst2)
        return list(set1.intersection(set2))
    
    def union(self, lst1, lst2):
        """
        Find the union of two lists.
        
        Args:
            lst1 (list): First list
            lst2 (list): Second list
            
        Returns:
            list: List of all unique elements
        """
        if not isinstance(lst1, list) or not isinstance(lst2, list):
            raise TypeError("Both arguments must be lists")
        
        set1 = set(lst1)
        set2 = set(lst2)
        return list(set1.union(set2))

