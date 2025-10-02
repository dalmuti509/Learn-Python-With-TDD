def test_create_student():
    manager = StudentManager()
    manager.add_student("Alice", 20, "Computer Science")
    assert "Alice" in manager.students
    assert manager.students["Alice"]["age"] == 20
    assert manager.students["Alice"]["major"] == "Computer Science"

def test_get_student():
    manager = StudentManager()
    manager.add_student("Bob", 22, "Mathematics")
    student = manager.get_student("Bob")
    assert student["age"] == 22
    assert student["major"] == "Mathematics"

def test_get_nonexistent_student():
    manager = StudentManager()
    student = manager.get_student("Charlie")
    assert student is None




