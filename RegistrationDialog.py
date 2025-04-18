from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QComboBox, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
import sqlite3


class RegistrationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Реєстрація студента")
        self.setFixedSize(450, 200)

        # Стиль діалогового вікна
        self.setStyleSheet("""
            QDialog {
                background-color: #E8F5E9;  /* світло-зелений фон */
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                padding: 6px;
                font-size: 14px;
                border-radius: 4px;
                border: 1px solid #A5D6A7;
            }
            QComboBox {
                padding: 6px;
                font-size: 14px;
                border-radius: 4px;
                border: 1px solid #A5D6A7;
            }
            QPushButton {
                width: 150px;  /* Одинаковий розмір кнопок */
                margin: 5px;  /* Відступи між кнопками */
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)

        # Основний Layout
        layout = QFormLayout(self)
        layout.setSpacing(10)  # Встановлюємо відступи між віджетами 0,5 см (10px)

        # Вибір студента
        self.student_cb = QComboBox()
        self.load_students()
        layout.addRow("Оберіть студента:", self.student_cb)

        # Ім’я користувача
        self.username_edit = QLineEdit()
        layout.addRow("Ім’я користувача (логін):", self.username_edit)

        # Пароль
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addRow("Пароль:", self.password_edit)

        # Кнопка реєстрації
        self.register_btn = QPushButton("Зареєструвати")
        self.register_btn.clicked.connect(self.register_user)

        # Горизонтальний layout для кнопки
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.register_btn)
        button_layout.setAlignment(Qt.AlignCenter)  # Вирівнюємо кнопку по центру

        button_layout.setSpacing(10)  # Встановлюємо відступи між кнопками
        layout.addRow(button_layout)

    def load_students(self):
        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT student_id, last_name || ' ' || first_name || ' ' || middle_name
            FROM Student_info
            WHERE student_id NOT IN (SELECT id FROM users WHERE position = 'студент')
        """)
        self.students = cursor.fetchall()
        conn.close()

        self.student_cb.clear()
        for student_id, full_name in self.students:
            self.student_cb.addItem(full_name, student_id)

    def register_user(self):
        student_id = self.student_cb.currentData()
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Помилка", "Усі поля мають бути заповнені!")
            return

        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()

        # 🔍 Перевірка: чи вже зареєстрований цей студент
        cursor.execute("SELECT 1 FROM users WHERE id = ?", (student_id,))
        if cursor.fetchone():
            QMessageBox.warning(self, "Помилка", "Цей студент вже має обліковий запис!")
            conn.close()
            return

        # 🔍 Перевірка: чи логін вже використовується
        cursor.execute("SELECT 1 FROM users WHERE name = ?", (username,))
        if cursor.fetchone():
            QMessageBox.warning(self, "Помилка", "Цей логін вже зайнятий. Виберіть інший.")
            conn.close()
            return

        try:
            cursor.execute("""
                INSERT INTO users (id, name, password, position)
                VALUES (?, ?, ?, ?)
            """, (student_id, username, password, "студент"))
            conn.commit()
            QMessageBox.information(self, "Успіх", "Студента успішно зареєстровано!")
            self.accept()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зареєструвати користувача:\n{e}")
        finally:
            conn.close()

