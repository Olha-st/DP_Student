import sqlite3

def fix_grades_table(db_path="Student.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Видаляємо записи, де student_id або course_id є NULL
    cursor.execute("DELETE FROM Grades WHERE student_id IS NULL OR course_id IS NULL")
    conn.commit()
    
    # Вимикаємо перевірку зовнішніх ключів перед змінами структури
    cursor.execute("PRAGMA foreign_keys = OFF")
    
    # Створюємо нову таблицю з коректними обмеженнями
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Grades_new (
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            grade INTEGER,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES Student_info(student_id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES Course(course_id) ON DELETE CASCADE
        )
    """)
    
    # Переносимо коректні дані у нову таблицю
    cursor.execute("""
        INSERT INTO Grades_new (student_id, course_id, grade)
        SELECT student_id, course_id, grade FROM Grades
        WHERE student_id IS NOT NULL AND course_id IS NOT NULL
    """)
    conn.commit()
    
    # Видаляємо стару таблицю
    cursor.execute("DROP TABLE Grades")
    
    # Перейменовуємо нову таблицю в Grades
    cursor.execute("ALTER TABLE Grades_new RENAME TO Grades")
    
    # Увімкнення перевірки зовнішніх ключів назад
    cursor.execute("PRAGMA foreign_keys = ON")
    
    conn.commit()
    conn.close()
    print("✅ Таблиця Grades виправлена!")

# Виконати виправлення
fix_grades_table()
