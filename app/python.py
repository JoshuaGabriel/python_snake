

class Student():


    StudentCount = 0
    StudentLegs  = 0

    def __init__(self,name,grade):
        self.name = name
        self.grade = grade
        Student.StudentCount+=1

        for num in range(2):
            Student.StudentLegs +=1
    

    @staticmethod
    def getStudentCount():
        return Student.StudentCount
    
    @staticmethod
    def getStudentLegs():
        return Student.StudentLegs


obj1 = Student("Joshua",90)
obj1 = Student("Cia",80)

print(Student.getStudentCount())
print(Student.getStudentLegs())


