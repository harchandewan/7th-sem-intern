class Student_Record:
    def __init__(self, student_name, student_caste, student_roll):
        self.student_name = student_name
        self.student_caste = student_caste
        self.student_roll = student_roll

    def create_student():
        name = input("enter your name:")
        caste = input("enter your caste:")
        roll = int(input("enter your roll:"))
        details = Student_Record(name, caste, roll)
        print("student created successfully")
        return details

    def student_grade():
        id = int(input("enter the student id:"))
        roll = next((x for x in student_details if x.student_roll == id), None)
        if roll:
            grade = input("enter the grade:")
            print("grade added successfully")
            return roll, grade
        else:
            print("student not found")


# list to store the details of students, courses and teachers
student_details = []
course_details = []
teacher_details = []
student_enrollment = []
student_grades = []


class Course:
    def __init__(self, course_id, course_name):
        self.course_id = course_id
        self.course_name = course_name

    def create_course():
        id = int(input("enter the course id:"))
        name = input("enter your course name:")
        details = Course(id, name)
        print("course created successfully")
        return details

    def student_enrollment():
        id = int(input("enter the student id:"))
        course_id = int(input("enter the course id:"))
        roll = next((x for x in student_details if x.student_roll == id), None)
        course_no = next((x for x in course_details if x.course_id == course_id), None)
        if roll and course_no:
            print("student enrolled successfully")
            return roll, course_no
        else:
            print("incorrect data")


class Teacher_details:
    def __init__(self, teacher_name, teacher_id):
        self.teacher_name = teacher_name
        self.teacher_id = teacher_id

    def create_teacher():
        name = input("enter your name:")
        id = int(input("enter your id:"))
        details = Teacher_details(name, id)
        print("teacher created successfully")
        return details


def display():
    choice = int(input(
        " 1 for student\n 2 for course \n 3 for enrollment\n 4 for grade\n 5 for teacher\n 6 to display:\n 7 to logout\n enter your choice:"))
    match choice:
        case 1:
            for student in student_details:
                print(
                    f"student name: {student.student_name}, student caste: {student.student_caste}, student roll: {student.student_roll}")
        case 2:
            for course in course_details:
                print(f"course id: {course.course_id}, course name: {course.course_name}")
        case 3:
            for teacher in teacher_details:
                print(f"teacher name: {teacher.teacher_name}, teacher id: {teacher.teacher_id}")
        case 4:
            for student, grade in student_grades:
                print(f"student: {student.student_name}, grade: {grade}")
        case 5:
            print("logout successful")


class main:
    while True:
        choice = int(input(
            "\n 1 for student\n 2 for course \n 3 for enrollment\n 4 for grade\n 5 for teacher\n 6 to display:\n 7 to logout \n enter a choice:"))
        if choice == 1:
            student = Student_Record.create_student()
            student_details.append(student)

        elif choice == 2:
            course = Course.create_course()
            course_details.append(course)

        elif choice == 3:
            enroll = Course.student_enrollment()
            if enroll:
                student_enrollment.append(enroll)

        elif choice == 4:
            grade = Student_Record.student_grade()
            if grade:
                student_grades.append(grade)

        elif choice == 5:
            teacher = Teacher_details.create_teacher()
            teacher_details.append(teacher)
        elif choice == 6:
            display()
        else:
            print("Logout successful")
            break


main()
