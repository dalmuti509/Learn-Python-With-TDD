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

