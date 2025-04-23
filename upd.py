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


import sqlite3

conn = sqlite3.connect("Student.db")
cursor = conn.cursor()

# Додаємо поле 'contact_info', якщо ще не існує
try:
    cursor.execute("ALTER TABLE Student_info ADD COLUMN contact_info TEXT")
except sqlite3.OperationalError:
    print("Поле 'contact_info' вже існує")

# Додаємо поле 'note', якщо ще не існує
try:
    cursor.execute("ALTER TABLE Student_info ADD COLUMN note TEXT")
except sqlite3.OperationalError:
    print("Поле 'note' вже існує")

conn.commit()
conn.close()
