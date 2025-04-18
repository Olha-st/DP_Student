from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox
import sqlite3

class ChangePasswordDialog(QDialog):
    def __init__(self, user_id, username, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.username = username
        self.setWindowTitle("Зміна пароля")
        self.setFixedSize(300, 200)

        layout = QFormLayout(self)

        self.old_password = QLineEdit()
        self.old_password.setEchoMode(QLineEdit.Password)
        layout.addRow("Старий пароль:", self.old_password)

        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)
        layout.addRow("Новий пароль:", self.new_password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        layout.addRow("Підтвердити пароль:", self.confirm_password)

        self.save_btn = QPushButton("Зберегти")
        self.save_btn.clicked.connect(self.change_password)
        layout.addWidget(self.save_btn)

    def change_password(self):
        old_pwd = self.old_password.text().strip()
        new_pwd = self.new_password.text().strip()
        confirm_pwd = self.confirm_password.text().strip()

        if not old_pwd or not new_pwd or not confirm_pwd:
            QMessageBox.warning(self, "Помилка", "Усі поля повинні бути заповнені!")
            return

        if new_pwd != confirm_pwd:
            QMessageBox.warning(self, "Помилка", "Нові паролі не співпадають!")
            return

        # Перевірка старого пароля
        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE id = ?", (self.user_id,))
        result = cursor.fetchone()
        if not result or result[0] != old_pwd:
            QMessageBox.warning(self, "Помилка", "Старий пароль введено неправильно!")
            conn.close()
            return

        # Оновлення пароля
        cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_pwd, self.user_id))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Успіх", "Пароль змінено успішно!")
        self.accept()
