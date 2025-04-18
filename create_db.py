import sqlite3

conn = sqlite3.connect("Student.db")
cursor = conn.cursor()

# Таблиця Student_info
cursor.execute("""
CREATE TABLE IF NOT EXISTS Student_info (
    student_id INTEGER PRIMARY KEY,
    last_name TEXT,
    first_name TEXT,
    middle_name TEXT,
    date TEXT,
    group_name TEXT
)
""")

# Таблиця Course
cursor.execute("""
CREATE TABLE IF NOT EXISTS Course (
    course_id INTEGER PRIMARY KEY,
    name TEXT,
    number_hours INTEGER,
    form_control TEXT,
    semester TEXT
)
""")

# Таблиця Grades
cursor.execute("""
CREATE TABLE IF NOT EXISTS Grades (
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    grade INTEGER,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES Student_info(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Course(course_id) ON DELETE CASCADE
)
""")

conn.commit()
conn.close()
