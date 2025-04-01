import sqlite3

# Підключення до бази даних
conn = sqlite3.connect("Student.db")
cursor = conn.cursor()

# Додавання нового поля 'group_name' до таблиці Student_info
try:
    cursor.execute("ALTER TABLE Student_info ADD COLUMN group_name TEXT")
    print("Поле 'group_name' успішно додано!")
except sqlite3.OperationalError:
    print("Поле 'group_name' вже існує!")

# Збереження змін і закриття з'єднання
conn.commit()
conn.close()
