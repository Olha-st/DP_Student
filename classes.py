import sqlite3

class Student:
    def __init__(self, student_id, last_name, first_name, middle_name, date, group_name):
        self.student_id = student_id
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self. date = date
        self.group_name = group_name
    
    def add_to_db(self):
        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Student_info (last_name, first_name, middle_name, date, group_name) VALUES (?, ?, ?, ?, ?)",
            (self.last_name, self.first_name, self.middle_name, self.date, self.group_name)
        )
        conn.commit()
        conn.close()

    def update_in_db(self):
        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Student_info
            SET last_name = ?, first_name = ?, middle_name = ?, date = ?, group_name = ?
            WHERE student_id = ?
        """, (self.last_name, self.first_name, self.middle_name, self.date, self.group_name, self.student_id))
        conn.commit()
        conn.close()

    def delete_from_db(self):
        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Student_info WHERE student_id = ?", (self.student_id,))
        conn.commit()
        conn.close()

    


class Course:
    def __init__(self, course_id, name, number_hours: int,form_control):
        self.course_id = course_id
        self.name = name
        self.number_hours = number_hours
        self.form_control = form_control

    def __str__(self):
        return self.name


class GradesBook:
    def __init__(self):
        self.grades = {}  # {student_id: {course_id: [оцінки]}}

    def add_grade(self, student, course, score):
        """Додає оцінку студенту по певному предмету"""
        if student.student_id not in self.grades:
            self.grades[student.student_id] = {}
        if course.course_id not in self.grades[student.student_id]:
            self.grades[student.student_id][course.course_id] = []
        self.grades[student.student_id][course.course_id].append(score)

    def get_student_grades(self, student):
        """Отримує всі оцінки студента"""
        if student.student_id not in self.grades:
            return {}
        return self.grades[student.student_id]

    def get_average_grade(self, student):
        """Обчислює середній бал студента"""
        all_scores = []
        for scores in self.get_student_grades(student).values():
            all_scores.extend(scores)
        return sum(all_scores) / len(all_scores) if all_scores else 0

    def __str__(self):
        return str(self.grades)


class Teacher:
    def __init__(self, teacher_id, first_name, last_name, subject):
        self.teacher_id = teacher_id
        self.first_name = first_name
        self.last_name = last_name
        self.subject = subject

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Предмет: {self.subject})"


class Report:
    @staticmethod
    def generate_student_report(student, grades_book):
        """Генерує звіт про успішність студента"""
        grades = grades_book.get_student_grades(student)
        report = f"Звіт для {student}:\n"
        for course_id, scores in grades.items():
            avg_score = sum(scores) / len(scores)
            report += f"- {course_id}: {scores} (Середній бал: {avg_score:.2f})\n"
        report += f"Загальний середній бал: {grades_book.get_average_grade(student):.2f}"
        return report
