import sqlite3

# Підключення до існуючої бази
conn = sqlite3.connect("Student.db")
cursor = conn.cursor()

# Створення таблиці users, якщо вона ще не існує
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    position TEXT CHECK(position IN ('заввідділенням', 'секретар', 'студент')) NOT NULL
)
""")

conn.commit()
conn.close()

print("Таблиця 'users' успішно створена.")
