# Діалог для введення/редагування даних студента
from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDateEdit, QDialogButtonBox, QHBoxLayout
)
from PyQt5.QtCore import QDate


class StudentDialog(QDialog):
    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.setWindowTitle("Дані студента")
        self.setFixedWidth(400)
        self.student = student
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #eaffea;
                font-size: 14px;
            }
            QLineEdit, QDateEdit {
                border: 1px solid #aaa;
                border-radius: 6px;
                padding: 6px;
                background-color: #fff;
            }
            QLineEdit:read-only {
                background-color: #e6e6e6;
                color: #555;
            }
            QDateEdit::drop-down {
                border: none;
            }
            QDialogButtonBox QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 6px 12px;
                border-radius: 6px;
                min-width: 100px;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.layout = QFormLayout(self)

        self.id_edit = QLineEdit()
        self.id_edit.setReadOnly(True)

        self.last_name_edit = QLineEdit()
        self.first_name_edit = QLineEdit()
        self.middle_name_edit = QLineEdit()

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_edit.setDate(QDate.currentDate())

        self.group_name_edit = QLineEdit()
        self.contact_edit = QLineEdit()
        self.contact_edit.setInputMask("+38 (000) 000-00-00;_")
        self.note_edit = QLineEdit()

        # Додавання елементів до форми
        self.layout.addRow("ID:", self.id_edit)
        self.layout.addRow("Прізвище:", self.last_name_edit)
        self.layout.addRow("Ім'я:", self.first_name_edit)
        self.layout.addRow("По батькові:", self.middle_name_edit)
        self.layout.addRow("Дата народження:", self.date_edit)
        self.layout.addRow("Група:", self.group_name_edit)
        self.layout.addRow("Контакти:", self.contact_edit)
        self.layout.addRow("Примітка:", self.note_edit)

        # Якщо студент редагується — заповнюємо поля
        if self.student is not None:
            self.id_edit.setText(str(self.student.student_id))
            self.last_name_edit.setText(self.student.last_name)
            self.first_name_edit.setText(self.student.first_name)
            self.middle_name_edit.setText(self.student.middle_name)
            self.group_name_edit.setText(self.student.group_name)
            self.contact_edit.setText(self.student.contact_info)
            self.note_edit.setText(self.student.note)
            try:
                day, month, year = map(int, self.student.date.split('.'))
                self.date_edit.setDate(QDate(year, month, day))
            except Exception as e:
                print("Помилка зчитування дати:", e)

        # Кнопки
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Центрування кнопок
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.buttonBox)
        button_layout.addStretch()
        self.layout.addRow(button_layout)

    def get_data(self):
        return {
            'student_id': int(self.id_edit.text()) if self.id_edit.text().isdigit() else None,
            'last_name': self.last_name_edit.text(),
            'first_name': self.first_name_edit.text(),
            'middle_name': self.middle_name_edit.text(),
            'date': self.date_edit.date().toString("dd.MM.yyyy"),
            'group_name': self.group_name_edit.text(),
            'contact_info': self.contact_edit.text(),
            'note': self.note_edit.text()
        }

