class StudentManager:
    def __init__(self):
        self.students = {}
    
    def add_student(self, name, age, major):
        self.students[name] = {
            "age": age,
            "major": major
        }
    
    def get_student(self, name):
        return self.students.get(name)




