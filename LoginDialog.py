import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog, QFormLayout, QLineEdit,
                             QMessageBox)

# стартове вікно програми
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вхід в систему")
        self.setFixedSize(400, 300)
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

        layout = QVBoxLayout()

        # Привітання з переносом слів
        welcome_label = QLabel("<html>👋 Ласкаво просимо <br> до системи обліку успішності студентів!</html>")
        welcome_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2E7D32;")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)
        layout.addSpacing(15)

        form_layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.pass_edit = QLineEdit()
        self.pass_edit.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Ім’я користувача:", self.name_edit)
        form_layout.addRow("Пароль:", self.pass_edit)
        layout.addLayout(form_layout)

        # Стилізовані кнопки
        self.buttonBox = QHBoxLayout()  # Використовуємо QHBoxLayout для кнопок
        self.login_btn = QPushButton("Увійти")
        self.cancel_btn = QPushButton("Скасувати")

        self.buttonBox.addWidget(self.login_btn)
        self.buttonBox.addWidget(self.cancel_btn)

        # Додавання стилів кнопок
        self.login_btn.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            font-size: 14px;
            font-weight: bold;
            padding: 6px 12px;
            border-radius: 6px;
        """)
        self.cancel_btn.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            font-size: 14px;
            font-weight: bold;
            padding: 6px 12px;
            border-radius: 6px;
        """)

        self.login_btn.clicked.connect(self.login)
        self.cancel_btn.clicked.connect(self.reject)

        layout.addLayout(self.buttonBox)  # Додаємо горизонтальний layout з кнопками
        self.setLayout(layout)

        self.user_data = None

    def login(self):
        name = self.name_edit.text().strip()
        password = self.pass_edit.text().strip()

        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, position FROM users WHERE name = ? AND password = ?", (name, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            self.user_data = {"id": result[0], "name": name, "position": result[1]}
            self.accept()
        else:
            QMessageBox.warning(self, "Помилка", "Невірні дані для входу.")


