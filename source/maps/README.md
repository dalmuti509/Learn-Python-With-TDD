# Dictionaries

Let's explore working with dictionaries in Python using TDD. We'll build various functions that demonstrate dictionary operations, data structures, and algorithms.

## The Problem

We want to create a student management system that uses dictionaries to store and manipulate student data.

## Red: Write Failing Tests

Let's start with some basic dictionary operations:

```python
# student_manager_test.py
import pytest
from student_manager import StudentManager

def test_add_student():
    manager = StudentManager()
    manager.add_student("001", "John Doe", 85)
    assert "001" in manager.students
    assert manager.students["001"]["name"] == "John Doe"
    assert manager.students["001"]["grade"] == 85

def test_get_student():
    manager = StudentManager()
    manager.add_student("001", "John Doe", 85)
    student = manager.get_student("001")
    assert student["name"] == "John Doe"
    assert student["grade"] == 85

def test_get_student_not_found():
    manager = StudentManager()
    with pytest.raises(KeyError):
        manager.get_student("999")

def test_update_grade():
    manager = StudentManager()
    manager.add_student("001", "John Doe", 85)
    manager.update_grade("001", 90)
    assert manager.students["001"]["grade"] == 90

def test_remove_student():
    manager = StudentManager()
    manager.add_student("001", "John Doe", 85)
    manager.remove_student("001")
    assert "001" not in manager.students

def test_get_all_students():
    manager = StudentManager()
    manager.add_student("001", "John Doe", 85)
    manager.add_student("002", "Jane Smith", 92)
    students = manager.get_all_students()
    assert len(students) == 2

def test_get_students_by_grade():
    manager = StudentManager()
    manager.add_student("001", "John Doe", 85)
    manager.add_student("002", "Jane Smith", 92)
    manager.add_student("003", "Bob Johnson", 85)
    
    students = manager.get_students_by_grade(85)
    assert len(students) == 2
    assert all(student["grade"] == 85 for student in students)

def test_get_average_grade():
    manager = StudentManager()
    manager.add_student("001", "John Doe", 85)
    manager.add_student("002", "Jane Smith", 92)
    manager.add_student("003", "Bob Johnson", 78)
    
    average = manager.get_average_grade()
    assert average == 85.0

def test_get_top_students():
    manager = StudentManager()
    manager.add_student("001", "John Doe", 85)
    manager.add_student("002", "Jane Smith", 92)
    manager.add_student("003", "Bob Johnson", 78)
    
    top_students = manager.get_top_students(2)
    assert len(top_students) == 2
    assert top_students[0]["grade"] == 92
    assert top_students[1]["grade"] == 85
```

## Green: Write the Minimal Code to Pass

Now let's implement our student manager:

```python
# student_manager.py
class StudentManager:
    """
    A student management system using dictionaries.
    """
    
    def __init__(self):
        self.students = {}
    
    def add_student(self, student_id, name, grade):
        """
        Add a new student to the system.
        
        Args:
            student_id (str): Unique student identifier
            name (str): Student's name
            grade (int): Student's grade
        """
        self.students[student_id] = {
            "name": name,
            "grade": grade
        }
    
    def get_student(self, student_id):
        """
        Get a student by ID.
        
        Args:
            student_id (str): Student identifier
            
        Returns:
            dict: Student information
            
        Raises:
            KeyError: If student not found
        """
        return self.students[student_id]
    
    def update_grade(self, student_id, new_grade):
        """
        Update a student's grade.
        
        Args:
            student_id (str): Student identifier
            new_grade (int): New grade
        """
        if student_id in self.students:
            self.students[student_id]["grade"] = new_grade
    
    def remove_student(self, student_id):
        """
        Remove a student from the system.
        
        Args:
            student_id (str): Student identifier
        """
        if student_id in self.students:
            del self.students[student_id]
    
    def get_all_students(self):
        """
        Get all students.
        
        Returns:
            dict: All students
        """
        return self.students
    
    def get_students_by_grade(self, grade):
        """
        Get students with a specific grade.
        
        Args:
            grade (int): Grade to filter by
            
        Returns:
            list: Students with the specified grade
        """
        return [student for student in self.students.values() if student["grade"] == grade]
    
    def get_average_grade(self):
        """
        Calculate the average grade of all students.
        
        Returns:
            float: Average grade
        """
        if not self.students:
            return 0.0
        
        total = sum(student["grade"] for student in self.students.values())
        return total / len(self.students)
    
    def get_top_students(self, n):
        """
        Get the top n students by grade.
        
        Args:
            n (int): Number of top students to return
            
        Returns:
            list: Top students sorted by grade
        """
        sorted_students = sorted(self.students.values(), key=lambda x: x["grade"], reverse=True)
        return sorted_students[:n]
```

## Run the Tests

```bash
pytest student_manager_test.py -v
```

## Refactor: Improve the Code

Let's improve our code with better error handling and additional functionality:

```python
# student_manager.py
class StudentManager:
    """
    A student management system using dictionaries.
    """
    
    def __init__(self):
        self.students = {}
    
    def add_student(self, student_id, name, grade):
        """
        Add a new student to the system.
        
        Args:
            student_id (str): Unique student identifier
            name (str): Student's name
            grade (int): Student's grade
            
        Raises:
            ValueError: If student_id already exists or grade is invalid
        """
        if student_id in self.students:
            raise ValueError(f"Student {student_id} already exists")
        if not isinstance(grade, (int, float)) or grade < 0 or grade > 100:
            raise ValueError("Grade must be a number between 0 and 100")
        
        self.students[student_id] = {
            "name": name,
            "grade": grade
        }
    
    def get_student(self, student_id):
        """
        Get a student by ID.
        
        Args:
            student_id (str): Student identifier
            
        Returns:
            dict: Student information
            
        Raises:
            KeyError: If student not found
        """
        if student_id not in self.students:
            raise KeyError(f"Student {student_id} not found")
        return self.students[student_id]
    
    def update_grade(self, student_id, new_grade):
        """
        Update a student's grade.
        
        Args:
            student_id (str): Student identifier
            new_grade (int): New grade
            
        Raises:
            KeyError: If student not found
            ValueError: If grade is invalid
        """
        if student_id not in self.students:
            raise KeyError(f"Student {student_id} not found")
        if not isinstance(new_grade, (int, float)) or new_grade < 0 or new_grade > 100:
            raise ValueError("Grade must be a number between 0 and 100")
        
        self.students[student_id]["grade"] = new_grade
    
    def remove_student(self, student_id):
        """
        Remove a student from the system.
        
        Args:
            student_id (str): Student identifier
            
        Returns:
            bool: True if student was removed, False if not found
        """
        if student_id in self.students:
            del self.students[student_id]
            return True
        return False
    
    def get_all_students(self):
        """
        Get all students.
        
        Returns:
            dict: All students
        """
        return self.students.copy()
    
    def get_students_by_grade(self, grade):
        """
        Get students with a specific grade.
        
        Args:
            grade (int): Grade to filter by
            
        Returns:
            list: Students with the specified grade
        """
        return [student for student in self.students.values() if student["grade"] == grade]
    
    def get_average_grade(self):
        """
        Calculate the average grade of all students.
        
        Returns:
            float: Average grade
        """
        if not self.students:
            return 0.0
        
        total = sum(student["grade"] for student in self.students.values())
        return total / len(self.students)
    
    def get_top_students(self, n):
        """
        Get the top n students by grade.
        
        Args:
            n (int): Number of top students to return
            
        Returns:
            list: Top students sorted by grade
        """
        if n <= 0:
            return []
        
        sorted_students = sorted(self.students.values(), key=lambda x: x["grade"], reverse=True)
        return sorted_students[:n]
    
    def get_grade_distribution(self):
        """
        Get the distribution of grades.
        
        Returns:
            dict: Grade distribution
        """
        distribution = {}
        for student in self.students.values():
            grade = student["grade"]
            if grade in distribution:
                distribution[grade] += 1
            else:
                distribution[grade] = 1
        return distribution
    
    def search_students(self, name_pattern):
        """
        Search students by name pattern.
        
        Args:
            name_pattern (str): Pattern to search for
            
        Returns:
            list: Students matching the pattern
        """
        matching_students = []
        for student in self.students.values():
            if name_pattern.lower() in student["name"].lower():
                matching_students.append(student)
        return matching_students
```

## Advanced Examples

Let's add some more complex dictionary operations:

```python
# student_manager_test.py (additional tests)
def test_grade_distribution():
    manager = StudentManager()
    manager.add_student("001", "John Doe", 85)
    manager.add_student("002", "Jane Smith", 92)
    manager.add_student("003", "Bob Johnson", 85)
    
    distribution = manager.get_grade_distribution()
    assert distribution[85] == 2
    assert distribution[92] == 1

def test_search_students():
    manager = StudentManager()
    manager.add_student("001", "John Doe", 85)
    manager.add_student("002", "Jane Smith", 92)
    manager.add_student("003", "Bob Johnson", 78)
    
    results = manager.search_students("john")
    assert len(results) == 2
    assert all("john" in student["name"].lower() for student in results)

def test_merge_students():
    manager1 = StudentManager()
    manager1.add_student("001", "John Doe", 85)
    
    manager2 = StudentManager()
    manager2.add_student("002", "Jane Smith", 92)
    
    manager1.merge_students(manager2)
    assert len(manager1.students) == 2
    assert "002" in manager1.students

def test_export_to_dict():
    manager = StudentManager()
    manager.add_student("001", "John Doe", 85)
    manager.add_student("002", "Jane Smith", 92)
    
    data = manager.export_to_dict()
    assert "students" in data
    assert len(data["students"]) == 2
```

```python
# student_manager.py (additional methods)
def merge_students(self, other_manager):
    """
    Merge students from another manager.
    
    Args:
        other_manager (StudentManager): Another student manager
    """
    for student_id, student_data in other_manager.students.items():
        if student_id not in self.students:
            self.students[student_id] = student_data

def export_to_dict(self):
    """
    Export all data to a dictionary.
    
    Returns:
        dict: All student data
    """
    return {
        "students": self.students,
        "total_students": len(self.students),
        "average_grade": self.get_average_grade()
    }

def import_from_dict(self, data):
    """
    Import students from a dictionary.
    
    Args:
        data (dict): Student data to import
    """
    if "students" in data:
        self.students.update(data["students"])

def get_statistics(self):
    """
    Get comprehensive statistics about students.
    
    Returns:
        dict: Statistics including min, max, average, and distribution
    """
    if not self.students:
        return {
            "total_students": 0,
            "average_grade": 0.0,
            "min_grade": 0,
            "max_grade": 0,
            "grade_distribution": {}
        }
    
    grades = [student["grade"] for student in self.students.values()]
    
    return {
        "total_students": len(self.students),
        "average_grade": sum(grades) / len(grades),
        "min_grade": min(grades),
        "max_grade": max(grades),
        "grade_distribution": self.get_grade_distribution()
    }
```

## What We've Learned

1. **Dictionary Operations**: Adding, removing, and updating key-value pairs
2. **Data Filtering**: Finding specific values in dictionaries
3. **Data Aggregation**: Calculating statistics from dictionary data
4. **Error Handling**: Validating inputs and handling edge cases
5. **Data Export/Import**: Serializing and deserializing dictionary data

## Exercises

1. Add a method to find students with grades in a specific range
2. Implement a method to get students sorted by name
3. Add support for student subjects and calculate subject averages
4. Create a method to find the most common grade

## Key Concepts

- **Dictionary Manipulation**: Working with key-value pairs
- **Data Filtering**: Finding specific data in collections
- **Data Aggregation**: Calculating statistics and summaries
- **Error Handling**: Validating inputs and handling edge cases
- **Data Serialization**: Converting data to/from different formats

