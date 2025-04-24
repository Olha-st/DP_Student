from PyQt5.QtWidgets import QLabel, QComboBox, QDialog, QFormLayout, QLineEdit, QDialogButtonBox
from PyQt5.QtCore import Qt

class CourseDialog(QDialog):
    def __init__(self, parent=None, course=None):
        super().__init__(parent)
        self.setWindowTitle("Дані предмета")
        self.course = course
        self.course_id = course[0] if course else None
        self.initUI()

    def initUI(self):
        self.setFixedSize(350, 380)
        self.setStyleSheet("""
            QDialog {
                background-color: #E8F5E9;
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
                width: 150px;
                margin: 5px;
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

        self.layout = QFormLayout(self)

        # Поля для введення
        if self.course is not None:
            self.id_edit = QLineEdit(str(self.course[0]))
            self.id_edit.setReadOnly(True)
            self.layout.addRow("ID:", self.id_edit)
        else:
            self.id_label = QLabel("автоматично")
            self.layout.addRow("ID:", self.id_label)

        self.name_edit = QLineEdit()
        self.hours_edit = QLineEdit()
        self.form_control_cb = QComboBox()
        self.form_control_cb.addItems(["екзамен", "диф.залік"])
        self.semester_edit = QLineEdit()

        self.supplement_cb = QComboBox()
        self.supplement_cb.addItems(["✅", "✖"])

        self.layout.addRow("Назва:", self.name_edit)
        self.layout.addRow("Години:", self.hours_edit)
        self.layout.addRow("Форма контролю:", self.form_control_cb)
        self.layout.addRow("Семестр:", self.semester_edit)
        self.layout.addRow("В додаток:", self.supplement_cb)

        if self.course is not None:
            self.name_edit.setText(self.course[1])
            self.hours_edit.setText(str(self.course[2]))
            self.form_control_cb.setCurrentText(self.course[3])
            self.semester_edit.setText(self.course[4])
            in_supplement = self.course[5] if len(self.course) > 5 else 0
            self.supplement_cb.setCurrentText("✅" if in_supplement else "✖")

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

    def get_data(self):
        return {
            'course_id': int(self.id_edit.text()) if hasattr(self, 'id_edit') and self.id_edit.text().isdigit() else None,
            'name': self.name_edit.text().strip(),
            'number_hours': int(self.hours_edit.text().strip()) if self.hours_edit.text().strip().isdigit() else 0,
            'form_control': self.form_control_cb.currentText(),
            'semester': self.semester_edit.text().strip(),
            'in_supplement': 1 if self.supplement_cb.currentText() == "✅" else 0
        }
