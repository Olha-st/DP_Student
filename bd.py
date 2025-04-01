import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    
    last_name TEXT,
    first_name TEXT,
    middle_name TEXT,
    birth_date TEXT
)
""")

students = [
    (1, "Петренко", "Іван", "Миколайович", "2001-05-15"),
    (2, "Іваненко", "Марія", "Володимирівнв", "2002-07-22"),
    (3, "Сидоренко", "Олег", "Олександрович", "2000-12-30"),
    
]

cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?)", students)
conn.commit()
conn.close()
