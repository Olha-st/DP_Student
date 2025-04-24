# Діалог для введення/редагування даних предмета

from PyQt5.QtWidgets import QLabel, QComboBox, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox

class CourseDialog(QDialog):
    def __init__(self, parent=None, course=None):
        super().__init__(parent)
        self.setWindowTitle("Дані предмета")
        self.course = course
        self.course_id = course[0] if course else None
        self.initUI()

    def initUI(self):
        self.setFixedSize(350, 300)

        # Стиль діалогового вікна
        self.setStyleSheet("""
            QDialog {
                background-color: #E8F5E9;  /* світло-зелений фон */
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QComboBox {
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
        self.layout = QFormLayout(self)

        # Поля для введення
        # ID
        if self.course is not None:
            self.id_edit = QLineEdit()
            self.id_edit.setReadOnly(True)
            self.id_edit.setText(str(self.course[0]))
            self.layout.addRow("ID:", self.id_edit)
        else:
            self.id_label = QLabel("автоматично")
            self.layout.addRow("ID:", self.id_label)

        self.name_edit = QLineEdit()
        self.hours_edit = QLineEdit()

        self.form_control_cb = QComboBox()
        self.form_control_cb.addItems(["екзамен", "диф.залік"])

        self.semester_edit = QLineEdit()

        self.add_to_supplement_cb = QComboBox()
        self.add_to_supplement_cb.addItems(["✅", "✖"])

        # Додавання у форму
        self.layout.addRow("Назва:", self.name_edit)
        self.layout.addRow("Години:", self.hours_edit)
        self.layout.addRow("Форма контролю:", self.form_control_cb)
        self.layout.addRow("Семестр:", self.semester_edit)
        self.layout.addRow("В додаток:", self.add_to_supplement_cb)

        # Якщо переданий курс — заповнюємо поля
        if self.course is not None:
            self.name_edit.setText(self.course[1])
            self.hours_edit.setText(str(self.course[2]))
            self.form_control_cb.setCurrentText(self.course[3])
            self.semester_edit.setText(self.course[4])
            # курс[5] — булеве поле: 1 або 0
            self.add_to_supplement_cb.setCurrentText("✅" if self.course[5] else "✖")

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

    # def get_data(self):
    #     return {
    #         'course_id': int(self.id_edit.text()) if hasattr(self, 'id_edit') and self.id_edit.text().isdigit() else None,
    #         'name': self.name_edit.text(),
    #         'number_hours': int(self.hours_edit.text()),
    #         'form_control': self.form_control_cb.currentText(),
    #         'semester': self.semester_edit.text(),
    #         'in_supplement': 1 if self.add_to_supplement_cb.currentText() == "✅" else 0
    #     }

    # def get_data(self):
    #     name = self.name_edit.text().strip()
    #     hours_text = self.hours_edit.text().strip()
    #     semester = self.semester_edit.text().strip()

    #     if not name or not hours_text or not semester:
    #         raise ValueError("Будь ласка, заповніть усі поля: Назва, Години, Семестр")

    #     try:
    #         number_hours = int(hours_text)
    #     except ValueError:
    #         raise ValueError("Години мають бути числом!")

    #     return {
    #         'course_id': int(self.id_edit.text()) if hasattr(self, 'id_edit') and self.id_edit.text().isdigit() else None,
    #         'name': name,
    #         'number_hours': number_hours,
    #         'form_control': self.form_control_cb.currentText(),
    #         'semester': semester,
    #         'in_supplement': 1 if self.supplement_cb.currentText() == "✅" else 0
        # }

    def get_data(self):
        return {
            'course_id': int(self.id_edit.text()) if hasattr(self, 'id_edit') and self.id_edit.text().isdigit() else None,
            'name': self.name_edit.text().strip(),
            'number_hours': int(self.hours_edit.text().strip()),
            'form_control': self.form_control_cb.currentText(),
            'semester': self.semester_edit.text().strip(),
            'in_supplement': 1 if self.supplement_cb.currentText() == "✅" else 0
        }




    def on_accept(self):
        name = self.name_edit.text().strip()
        hours_text = self.hours_edit.text().strip()
        semester = self.semester_edit.text().strip()

        if not name or not hours_text or not semester:
            QMessageBox.warning(self, "Помилка", "Будь ласка, заповніть усі поля: Назва, Години, Семестр")
            return

        try:
            int(hours_text)
        except ValueError:
            QMessageBox.warning(self, "Помилка", "Години мають бути числом!")
            return

        self.accept()  # ✅ Лише якщо все гаразд
