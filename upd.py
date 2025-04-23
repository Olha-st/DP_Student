# import sqlite3

# # Підключення до існуючої бази
# conn = sqlite3.connect("Student.db")
# cursor = conn.cursor()

# # Створення таблиці users, якщо вона ще не існує
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     password TEXT NOT NULL,
#     position TEXT CHECK(position IN ('заввідділенням', 'секретар', 'студент')) NOT NULL
# )
# """)

# conn.commit()
# conn.close()

# print("Таблиця 'users' успішно створена.")


# import sqlite3

# conn = sqlite3.connect("Student.db")
# cursor = conn.cursor()

# # Додаємо поле 'contact_info', якщо ще не існує
# try:
#     cursor.execute("ALTER TABLE Student_info ADD COLUMN contact_info TEXT")
# except sqlite3.OperationalError:
#     print("Поле 'contact_info' вже існує")

# # Додаємо поле 'note', якщо ще не існує
# try:
#     cursor.execute("ALTER TABLE Student_info ADD COLUMN note TEXT")
# except sqlite3.OperationalError:
#     print("Поле 'note' вже існує")

# conn.commit()
# conn.close()

import sqlite3

def add_included_in_appendix_column():
    conn = sqlite3.connect("Student.db")
    cursor = conn.cursor()

    # Перевіряємо, чи колонка вже існує
    cursor.execute("PRAGMA table_info(Course)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if "included_in_appendix" not in columns:
        cursor.execute("""
            ALTER TABLE Course
            ADD COLUMN included_in_appendix INTEGER DEFAULT 0
        """)
        print("✅ Поле 'included_in_appendix' успішно додано до таблиці Course.")
    else:
        print("ℹ️ Поле 'included_in_appendix' вже існує.")

    conn.commit()
    conn.close()

add_included_in_appendix_column()
