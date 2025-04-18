# Діалог для введення/редагування даних студента
from PyQt5.QtWidgets import QHBoxLayout, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QDateEdit
class StudentDialog(QDialog):
    from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDateEdit, QDialogButtonBox
)
from PyQt5.QtCore import QDate

class StudentDialog(QDialog):
    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.setWindowTitle("Дані студента")
        self.setFixedWidth(400)  # опціонально
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
            QDateEdit::down-arrow {
                image: url(:/qt-project.org/styles/commonstyle/images/arrowdown-16.png);
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
            QDialogButtonBox QPushButton:cancel {
                background-color: #d9534f;
            }
            QDialogButtonBox QPushButton:cancel:hover {
                background-color: #c9302c;
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

        self.layout.addRow("ID:", self.id_edit)
        self.layout.addRow("Прізвище:", self.last_name_edit)
        self.layout.addRow("Ім'я:", self.first_name_edit)
        self.layout.addRow("По батькові:", self.middle_name_edit)
        self.layout.addRow("Дата народження:", self.date_edit)
        self.layout.addRow("Група:", self.group_name_edit)

        if self.student is not None:
            self.id_edit.setText(str(self.student.student_id))
            self.last_name_edit.setText(self.student.last_name)
            self.first_name_edit.setText(self.student.first_name)
            self.middle_name_edit.setText(self.student.middle_name)
            self.group_name_edit.setText(self.student.group_name)
            try:
                day, month, year = map(int, self.student.date.split('.'))
                self.date_edit.setDate(QDate(year, month, day))
            except:
                pass

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

                # Отримуємо кнопки
        ok_button = self.buttonBox.button(QDialogButtonBox.Ok)
        cancel_button = self.buttonBox.button(QDialogButtonBox.Cancel)

        # Встановлюємо однаковий розмір
        button_width = 100
        button_height = 32
        ok_button.setFixedSize(button_width, button_height)
        cancel_button.setFixedSize(button_width, button_height)

        # Центруємо кнопки
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.buttonBox)
        button_layout.addStretch()
        self.layout.addRow(button_layout)
        self.layout.addWidget(self.buttonBox)


    def get_data(self):
        return {
            'student_id': int(self.id_edit.text()) if self.id_edit.text().isdigit() else None,
            'last_name': self.last_name_edit.text(),
            'first_name': self.first_name_edit.text(),
            'middle_name': self.middle_name_edit.text(),
            'date': self.date_edit.date().toString("dd.MM.yyyy"),  # Отримуємо дату як рядок
            'group_name': self.group_name_edit.text()
        }


    def get_data(self):
        return {
            'student_id': int(self.id_edit.text()) if self.id_edit.text().isdigit() else None,  # Перевірка на число,
            'last_name': self.last_name_edit.text(),
            'first_name': self.first_name_edit.text(),
            'middle_name': self.middle_name_edit.text(),
            'date': self.date_edit.text(),
            'group_name': self.group_name_edit.text()
        }

