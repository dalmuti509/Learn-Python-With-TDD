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

