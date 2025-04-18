# встановити бібліотеки pandas
import sys
import openpyxl  # Робота з Excel
import math
from PyQt5.QtGui import QColor
import sqlite3
import pandas as pd
from PyQt5.QtCore import Qt, QDate
from classes import Student
from RegistrationDialog import RegistrationDialog
from change_password_dialog import ChangePasswordDialog
from StudentDialog import StudentDialog
from LoginDialog import LoginDialog
from CourseDialog import CourseDialog
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QTabWidget, QLabel, QPushButton, QComboBox, QDialog, QFormLayout, QLineEdit,
                             QDialogButtonBox, QMessageBox, QInputDialog, QDateEdit, QAbstractItemView, QFileDialog)






# Клас для коректного числового сортування
class NumericItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except ValueError:
            return QTableWidgetItem.__lt__(self, other)


# 📌Вкладка1 "Інформація про студентів"
class StudentInfoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        # Горизонтальне розташування кнопок
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Додати")
        self.edit_btn = QPushButton("Редагувати")
        self.delete_btn = QPushButton("Видалити")
        self.sort_btn = QPushButton("Сортувати")
        self.register_btn = QPushButton("Зареєструвати студента")
        self.register_btn.setFixedSize(180, 30)
        self.register_btn.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;font-size:1px")
        btn_layout.addWidget(self.register_btn)

        main_layout.addSpacing(20)

        # Встановлюємо однаковий розмір кнопок та зелений відтінок
        btn_size = (120, 30)
        style = "background-color: #4CAF50; color: white; border: none; border-radius: 5px; font-size: 16px; font-size: 16px"
        for btn in (self.add_btn, self.edit_btn, self.delete_btn, self.sort_btn):
            btn.setFixedSize(*btn_size)
            btn.setStyleSheet(style)
            btn_layout.addWidget(btn)

        main_layout.addLayout(btn_layout)
        # Додаємо відступ після кнопок
        main_layout.addSpacing(20)


         # Таблиця студентів
        self.table = QTableWidget()
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

        # self.load_students()

        # Горизонтальна панель фільтрації груп
        main_layout.addSpacing(20)
        filter_layout = QHBoxLayout()
        self.all_students_btn = QPushButton("Весь список")
        self.group_ki_21_01_btn = QPushButton("КІ-21-01")
        self.group_ki_21_02_btn = QPushButton("КІ-21-02")
        

        # Додаємо кнопки до фільтраційного блоку
        for btn in (self.all_students_btn, self.group_ki_21_01_btn, self.group_ki_21_02_btn):
            btn.setFixedSize(120, 30)
            btn.setStyleSheet("background-color: #A0E0A0; color: white; border: none; border-radius: 5px; font-size: 14px;")
            filter_layout.addWidget(btn)
        
        main_layout.addLayout(filter_layout)

        self.load_students()  # Завантаження даних

        self.all_students_btn.clicked.connect(lambda: self.load_students(order_by="last_name"))  # Завантажити всіх студентів
        self.group_ki_21_01_btn.clicked.connect(lambda: self.load_students("КІ-21-01", "last_name"))  # Фільтр + сортування
        self.group_ki_21_02_btn.clicked.connect(lambda: self.load_students("КІ-21-02", "last_name"))  # Фільтр + сортування

        # Підключення слотів до кнопок
        self.add_btn.clicked.connect(self.add_student)
        self.edit_btn.clicked.connect(self.edit_student)
        self.delete_btn.clicked.connect(self.delete_student)
        self.sort_btn.clicked.connect(self.sort_students)
        self.register_btn.clicked.connect(self.register_student)


    def load_students(self, group_name=None, order_by=None):
        """Завантаження списку студентів, з можливістю фільтрації за групою."""
        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()

        query = "SELECT * FROM Student_info"
        params = []

        if group_name:
                query += " WHERE group_name = ?"
                params.append(group_name)

        if order_by:
            query += f" ORDER BY {order_by} ASC"

        cursor.execute(query, params)
        students = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(students))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Прізвище", "Ім'я", "По батькові", "Дата народження", "Група"])
        self.table.setColumnHidden(0, True)

        for row, student in enumerate(students):
            for col, data in enumerate(student):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))

        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #4CAF50; color: white; font-size: 16px; font-weight: bold; padding: 8px; }"
        )
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 180)
        self.table.setColumnWidth(5, 100)
        
    def add_student(self):
        dialog = StudentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            try:
                student = Student(data['student_id'], data['last_name'], data['first_name'],
                                  data['middle_name'], data['date'], data['group_name'])
                student.add_to_db()
            except Exception as e:
                QMessageBox.warning(self, "Помилка", f"Не вдалося додати студента:\n{e}")
            self.load_students()

    def edit_student(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Попередження", "Оберіть запис для редагування")
            return
        
        row = selected[0].row()
        student_id = int(self.table.item(row, 0).text())
        last_name = self.table.item(row, 1).text()
        first_name = self.table.item(row, 2).text()
        middle_name = self.table.item(row, 3).text()
        date = self.table.item(row, 4).text()
        group_name = self.table.item(row, 5).text()

        current_student = Student(student_id, last_name, first_name, middle_name, date, group_name)
        print("Відкриваємо діалогове вікно редагування")  # Перевірка
        dialog = StudentDialog(self, student=current_student)

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            try:
                updated_student = Student(data['student_id'], data['last_name'], data['first_name'],
                                        data['middle_name'], data['date'], data['group_name'])
                updated_student.update_in_db()

                # Закриваємо діалог явно
                dialog.done(QDialog.Accepted)
                
            except Exception as e:
                QMessageBox.warning(self, "Помилка", f"Не вдалося оновити дані студента:\n{e}")

            self.load_students()


    def delete_student(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Попередження", "Оберіть запис для видалення")
            return
        row = selected[0].row()
        student_id = int(self.table.item(row, 0).text())

        reply = QMessageBox.question(self, "Підтвердження", "Ви впевнені, що хочете видалити запис?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                student = Student(student_id, "", "", "", "", "")
                student.delete_from_db()
            except Exception as e:
                QMessageBox.warning(self, "Помилка", f"Не вдалося видалити студента:\n{e}")
            self.load_students()

    def sort_students(self):
        order, ok = QInputDialog.getItem(self, "Сортування", "Виберіть порядок сортування:",
                                         ["За зростанням", "За спаданням"], 0, False)
        if ok and order:
            if order == "За зростанням":
                self.table.sortItems(1, Qt.AscendingOrder)
            else:
                self.table.sortItems(1, Qt.DescendingOrder)

    
    def register_student(self):
        dialog = RegistrationDialog(self)
        dialog.exec_()





#📌 Вкладка2 CoursesTab для введення, редагування предметів
class CoursesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.filter_semester = None  # зберігає поточне значення фільтра
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.addSpacing(20)
        
        # Перший рядок кнопок: Додати, Редагувати, Видалити, Фільтр, Показати усі
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Додати")
        self.edit_btn = QPushButton("Редагувати")
        self.delete_btn = QPushButton("Видалити")
        self.filter_btn = QPushButton("Фільтр")
        self.show_all_btn = QPushButton("Показати усі")
        
        btn_size = (120, 30)
        style = "background-color: #4CAF50; color: white; border: none; border-radius: 5px; font-size: 16px"
        for btn in (self.add_btn, self.edit_btn, self.delete_btn, self.filter_btn, self.show_all_btn):
            btn.setFixedSize(*btn_size)
            btn.setStyleSheet(style)
            btn_layout.addWidget(btn)
        main_layout.addLayout(btn_layout)
        main_layout.addSpacing(20)
        
        # Другий рядок: випадаючі списки для сортування та кнопка "Сортувати"
        
        sort_layout = QHBoxLayout()
        self.sort_field_cb = QComboBox()
        fields = ["ID", "Назва", "Години", "Форма контролю", "Семестр"]
        self.sort_field_cb.addItems(fields)
        self.sort_order_cb = QComboBox()
        self.sort_order_cb.addItems(["За зростанням", "За спаданням"])
        self.sort_btn = QPushButton("Сортувати")
        self.sort_btn.setFixedSize(*btn_size)
        self.sort_btn.setStyleSheet(style)
        
        sort_layout.addWidget(QLabel("Поле:"))
        sort_layout.addWidget(self.sort_field_cb)
        sort_layout.addSpacing(40)
        sort_layout.addWidget(QLabel("Напрям:"))
        sort_layout.addWidget(self.sort_order_cb)
        sort_layout.addSpacing(40)
        sort_layout.addWidget(self.sort_btn)
        main_layout.addLayout(sort_layout)
        sort_layout.addStretch()
        main_layout.addSpacing(20)
        
        self.table = QTableWidget()
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)
        
        self.load_courses()
        self.add_btn.clicked.connect(self.add_course)
        self.edit_btn.clicked.connect(self.edit_course)
        self.delete_btn.clicked.connect(self.delete_course)
        self.filter_btn.clicked.connect(self.filter_courses)
        self.show_all_btn.clicked.connect(self.show_all_courses)
        self.sort_btn.clicked.connect(self.sort_courses)

    def load_courses(self):
        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()

        if self.filter_semester:
            cursor.execute("SELECT * FROM Course WHERE semester = ?", (self.filter_semester,))
        else:
            cursor.execute("SELECT * FROM Course")
        courses = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(courses))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Назва", "Години", "Форма контролю", "Семестр"])
        self.table.setColumnHidden(0, True)  # ховаємо ID

        for row, course in enumerate(courses):
            for col, data in enumerate(course):
                item = NumericItem(str(data)) if col == 2 else QTableWidgetItem(str(data))
                self.table.setItem(row, col, item)

        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 160)
        self.table.setColumnWidth(4, 100)

        self.table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #4CAF50; color: white; font-size: 16px; font-weight: bold; padding: 8px; }"
        )

    def add_course(self):
        dialog = CourseDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            try:
                conn = sqlite3.connect("Student.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Course (name, number_hours, form_control, semester)
                    VALUES (?, ?, ?, ?)
                """, (data['name'], data['number_hours'], data['form_control'], data['semester']))
                conn.commit()
                conn.close()
            except Exception as e:
                QMessageBox.warning(self, "Помилка", f"Не вдалося додати предмет:\n{e}")
            self.load_courses()


    def edit_course(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Попередження", "Оберіть запис для редагування")
            return

        row = selected[0].row()
        course_id = int(self.table.item(row, 0).text())
        name = self.table.item(row, 1).text()
        number_hours = int(self.table.item(row, 2).text())
        form_control = self.table.item(row, 3).text()
        semester = self.table.item(row, 4).text()

        current_course = (course_id, name, number_hours, form_control, semester)
        dialog = CourseDialog(self, course=current_course)

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            try:
                conn = sqlite3.connect("Student.db")
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Course
                    SET name = ?, number_hours = ?, form_control = ?, semester = ?
                    WHERE course_id = ?
                """, (data['name'], data['number_hours'], data['form_control'], data['semester'], course_id))
                conn.commit()
                conn.close()
            except Exception as e:
                QMessageBox.warning(self, "Помилка", f"Не вдалося оновити дані предмета:\n{e}")
            self.load_courses()


    def delete_course(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Попередження", "Оберіть запис для видалення")
            return

        row = selected[0].row()
        course_id = int(self.table.item(row, 0).text())

        reply = QMessageBox.question(self, "Підтвердження", "Ви впевнені, що хочете видалити запис?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect("Student.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Course WHERE course_id = ?", (course_id,))
                conn.commit()
                conn.close()
            except Exception as e:
                QMessageBox.warning(self, "Помилка", f"Не вдалося видалити предмет:\n{e}")
            self.load_courses()


    def filter_courses(self):
        semester, ok = QInputDialog.getText(self, "Фільтр", "Введіть семестр для фільтрації (залиште порожнім для скидання):")
        if ok:
            if semester.strip() == "":
                self.filter_semester = None
            else:
                self.filter_semester = semester.strip()
            self.load_courses()

    def show_all_courses(self):
        self.filter_semester = None
        self.load_courses()

    def sort_courses(self):
        # Отримання вибраного поля для сортування з combo box
        fields = ["ID", "Назва", "Години", "Форма контролю", "Семестр"]
        field = self.sort_field_cb.currentText()
        field_index = fields.index(field)
        # Отримання напрямку сортування
        direction = self.sort_order_cb.currentText()
        sort_order = Qt.AscendingOrder if direction == "За зростанням" else Qt.DescendingOrder
        self.table.sortItems(field_index, sort_order)


# 📌 Вкладка3 "Успішність по предмету"
class GradesByCourseTab(QWidget):
    def __init__(self, student_id=None):
        super().__init__()
        self.student_id = student_id
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Додаємо відступ перед групою віджетів
        layout.addSpacing(20)

        # Вибір предмета
        course_layout = QHBoxLayout()
        course_label = QLabel("Оберіть предмет:")
        self.course_dropdown = QComboBox()
        self.course_dropdown.setFixedWidth(300)
        self.course_dropdown.currentIndexChanged.connect(self.load_grades)

        course_layout.addWidget(course_label, 0, Qt.AlignLeft)
        course_layout.addSpacing(20)
        self.course_dropdown.setMinimumWidth(250)
        course_layout.addWidget(self.course_dropdown, 0, Qt.AlignLeft)
        course_layout.addStretch()
        layout.addLayout(course_layout)

        # Відступ між групами віджетів
        layout.addSpacing(20)

        # 🔐 Тільки для викладачів/секретарів: група + дата
        if not self.student_id:
            group_date_layout = QHBoxLayout()

            # Вибір групи
            group_label = QLabel("Оберіть групу:")
            self.group_dropdown = QComboBox()
            self.group_dropdown.setFixedWidth(150)
            self.group_dropdown.addItems(["КІ-21-01", "КІ-21-02"])
            self.group_dropdown.currentIndexChanged.connect(self.load_grades)

            # Поле вибору дати
            date_label = QLabel("Дата проведення контролю:")
            self.date_picker = QDateEdit()
            self.date_picker.setCalendarPopup(True)
            self.date_picker.setDate(QDate.currentDate())

            # Додаємо віджети з потрібними відступами
            group_date_layout.addWidget(group_label, 0, Qt.AlignLeft)
            group_date_layout.addSpacing(20)
            group_date_layout.addWidget(self.group_dropdown, 0, Qt.AlignLeft)
            group_date_layout.addSpacing(40)
            group_date_layout.addWidget(date_label, 0, Qt.AlignLeft)
            group_date_layout.addSpacing(20)
            group_date_layout.addWidget(self.date_picker, 0, Qt.AlignLeft)
            group_date_layout.addStretch()

            layout.addLayout(group_date_layout)

        # Додаємо відступ після групи віджетів
        layout.addSpacing(20)


        # # Таблиця з оцінками
        # self.table = QTableWidget()
        # self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)  # Дозволяє редагування
        # layout.addWidget(self.table)
        # layout.addSpacing(20)
        # # Кнопки "Зберегти оцінки" та "Експортувати відомість"
        # btn_layout = QHBoxLayout()
        # btn_layout.addSpacing(20)
        
        # self.save_grades_btn = QPushButton("Зберегти оцінки")
        # self.export_button = QPushButton("Відомість")
        

        # for btn in (self.save_grades_btn, self.export_button):
        #     btn.setFixedSize(150, 30)
        #     btn.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px; font-size: 16px")

        # btn_layout = QHBoxLayout()
        # btn_layout.addWidget(self.save_grades_btn)
        # # Додаємо фіксований проміжок 40 пікселів
        # btn_layout.addSpacing(40)
        

        # btn_layout.addStretch()  # Додаємо розтягування праворуч, щоб кнопки лишилися зліва
       
        # layout.addLayout(btn_layout)

        # self.setLayout(layout)
        # layout.addSpacing(20)

        # # Підключення подій
        # self.save_grades_btn.clicked.connect(self.save_grades)
        # self.export_button.clicked.connect(self.export_to_excel)

        # Додаємо таблицю
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        layout.addWidget(self.table)

        # Додаємо кнопки лише якщо не студент
        btn_layout = QHBoxLayout()

        if not self.student_id:
            self.save_grades_btn = QPushButton("Зберегти оцінки")
            self.export_button = QPushButton("Відомість")

            for btn in (self.save_grades_btn, self.export_button):
                btn.setFixedSize(150, 30)
                btn.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px; font-size: 16px")

            btn_layout.addWidget(self.save_grades_btn)
            btn_layout.addSpacing(40)
            btn_layout.addWidget(self.export_button)

            # Підключення сигналів
            self.save_grades_btn.clicked.connect(self.save_grades)
            self.export_button.clicked.connect(self.export_to_excel)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Встановлюємо layout вкінці
        self.setLayout(layout)

        self.load_courses()


    def load_grades(self):
        """Завантаження оцінок по вибраному предмету"""
        course_id = self.course_dropdown.currentData()

        # Отримати group_name тільки якщо це не студент
        group_name = self.group_dropdown.currentText() if hasattr(self, "group_dropdown") else None

        if course_id is None and not self.student_id:
            return  # Для викладачів потрібен вибраний предмет

        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()

        grades = []
        columns = []

        if self.student_id:
            if course_id is None:
                # 🔹 Всі оцінки по всіх предметах студента з номером семестру
                cursor.execute("""
                    SELECT C.semester, C.name, G.grade
                    FROM Grades G
                    JOIN Course C ON G.course_id = C.course_id
                    WHERE G.student_id = ?
                    ORDER BY C.semester ASC
                """, (self.student_id,))
                raw_data = cursor.fetchall()

                # Групування оцінок по семестрах
                from collections import defaultdict
                semester_data = defaultdict(list)
                for semester, name, grade in raw_data:
                    semester_data[semester].append((name, grade))

                # Формування списку оцінок із середніми
                for semester in sorted(semester_data.keys()):
                    subjects = semester_data[semester]
                    for name, grade in subjects:
                        grades.append((semester, name, grade))

                    # Додавання середнього балу
                    grades_in_semester = [g for _, g in subjects if isinstance(g, (int, float))]
                    if grades_in_semester:
                        avg = round(sum(grades_in_semester) / len(grades_in_semester), 2)
                        grades.append((semester, "Середній бал:", avg))
                    else:
                        grades.append((semester, "Середній бал:", "-"))

                columns = ["Семестр", "Предмет", "Оцінка"]
            else:
                # 🔹 Оцінки лише по вибраному предмету
                cursor.execute("""
                    SELECT S.last_name, S.first_name, S.middle_name, G.grade
                    FROM Grades G
                    JOIN Student_info S ON G.student_id = S.student_id
                    WHERE G.course_id = ? AND G.student_id = ?
                    ORDER BY S.last_name ASC
                """, (course_id, self.student_id))
                grades = cursor.fetchall()
                columns = ["Прізвище", "Ім'я", "По батькові", "Оцінка"]
        else:
            # 🔹 Для викладача/секретаря — оцінки по конкретному предмету і групі
            cursor.execute("""
                SELECT S.student_id, S.last_name, S.first_name, S.middle_name, COALESCE(G.grade, '') 
                FROM Student_info S
                LEFT JOIN Grades G ON S.student_id = G.student_id AND G.course_id = ?
                WHERE S.group_name = ?
                ORDER BY S.last_name ASC
            """, (course_id, group_name))
            grades = cursor.fetchall()
            columns = ["ID", "Прізвище", "Ім'я", "По батькові", "Оцінка"]

        conn.close()

        # Очистка таблиці та заповнення
        self.table.clear()
        self.table.setRowCount(len(grades))
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        for row, grade in enumerate(grades):
            for col, data in enumerate(grade):
                item = QTableWidgetItem(str(data))

                # 🔍 Виділення для "Середній бал:"
                if len(grade) >= 2 and str(grade[1]) == "Середній бал:":
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    item.setBackground(QColor("#D0F0C0"))

                # 🔒 Дозвіл редагування лише для викладачів
                if columns[col] == "Оцінка" and not self.student_id:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                self.table.setItem(row, col, item)

        # Налаштування режиму редагування
        if not self.student_id and "ID" in columns:
            self.table.setColumnHidden(0, True)
            self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        else:
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Налаштування ширини колонок
        for i, width in enumerate([120, 300, 300,300][:len(columns)]):
            self.table.setColumnWidth(i, width)

        self.table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #4CAF50; color: white; font-size: 16px; font-weight: bold; padding: 8px; }"
        )





    def save_grades(self):
        """Збереження внесених оцінок у базу даних (для викладача або секретаря)."""
        course_id = self.course_dropdown.currentData()
        if course_id is None:
            QMessageBox.warning(self, "Помилка", "Виберіть предмет перед збереженням оцінок!")
            return

        # Студенти не мають права редагувати, тому просто ігноруємо дію
        if hasattr(self, 'student_id') and self.student_id:
            QMessageBox.information(self, "Увага", "Студенти не мають права змінювати оцінки.")
            return

        try:
            with sqlite3.connect("Student.db") as conn:
                cursor = conn.cursor()

                for row in range(self.table.rowCount()):
                    student_id_item = self.table.item(row, 0)  # Прихований ID
                    grade_item = self.table.item(row, self.table.columnCount() - 1)  # Оцінка = останній стовпець

                    if not student_id_item or not grade_item:
                        print(f"⚠️ Пропущено рядок {row}: немає ID або оцінки.")
                        continue

                    student_id_text = student_id_item.text().strip()
                    grade_text = grade_item.text().strip()

                    if not student_id_text.isdigit():
                        print(f"⚠️ Некоректний ID у рядку {row}: {student_id_text}")
                        continue

                    if not grade_text.isdigit():
                        QMessageBox.warning(self, "Помилка", f"Некоректна оцінка у рядку {row + 1}: {grade_text}. "
                                                            f"Введіть число від 1 до 12.")
                        return

                    grade = int(grade_text)
                    if not (1 <= grade <= 12):
                        QMessageBox.warning(self, "Помилка", f"Оцінка у рядку {row + 1} ({grade}) виходить за межі 1-12!")
                        return

                    student_id = int(student_id_text)

                    # Запис або оновлення оцінки
                    cursor.execute("""
                        INSERT INTO Grades (student_id, course_id, grade) 
                        VALUES (?, ?, ?)
                        ON CONFLICT(student_id, course_id) DO UPDATE SET grade = excluded.grade
                    """, (student_id, course_id, grade))

                conn.commit()

        except sqlite3.OperationalError as e:
            QMessageBox.critical(self, "Помилка", f"Помилка бази даних:\n{e}")
            return

        QMessageBox.information(self, "Успіх", "Оцінки успішно збережено!")
        self.load_grades()



    def export_to_excel(self):
        """Експорт оцінок у файл 'vidomist.xlsx' для вибраної групи"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Відкрити відомість", "", "Excel Files (*.xlsx)")
        if not file_path:
            return

        # Отримуємо вибраний предмет та дату
        course_id = self.course_dropdown.currentData()
        selected_date = self.date_picker.date().toString("dd.MM.yyyy")
        group_name = self.group_dropdown.currentText()  # Вибрана група

        # Отримуємо дані про предмет із таблиці Course
        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, number_hours FROM Course WHERE course_id = ?", (course_id,))
        course_data = cursor.fetchone()
        conn.close()

        if not course_data:
            QMessageBox.warning(self, "Помилка", "Предмет не знайдено в базі даних!")
            return

        course_name, number_hours = course_data

        # Завантажуємо оцінки студентів для вибраної групи та предмета
        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Student_info.last_name, Student_info.first_name, Student_info.middle_name, Grades.grade 
            FROM Grades
            JOIN Student_info ON Grades.student_id = Student_info.student_id
            WHERE Grades.course_id = ? AND Student_info.group_name = ?
        """, (course_id, group_name))
        grades = cursor.fetchall()
        conn.close()

        # Сортуємо студентів за прізвищем у зростаючому порядку
        grades_sorted = sorted(grades, key=lambda x: x[0])

        # Завантажуємо Excel файл
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active

        # Записуємо дані в Excel
        sheet["B15"].value = course_name  # Назва предмета
        sheet["B13"].value = selected_date  # Дата контролю
        sheet["H20"].value = number_hours  # Кількість годин
        sheet["F8"].value = group_name  # Назва групи

        name_range = sheet["B26:B55"]
        grade_range = sheet["E26:E55"]

        for i, (last_name, first_name, middle_name, grade) in enumerate(grades_sorted):
            if i >= 30:
                break
            # Формуємо ініціали (прізвище та ініціали)
            initials = f"{last_name} {first_name[0]}.{middle_name[0]}."
            name_range[i][0].value = initials

            # Експортуємо оцінку як ціле число
            grade_range[i][0].value = int(grade) if grade is not None else ""

        # Якщо студентів менше, ніж 30, залишаємо порожні клітинки
        for i in range(len(grades_sorted), 30):
            name_range[i][0].value = ""
            grade_range[i][0].value = ""

        # Зберігаємо файл
        save_path, _ = QFileDialog.getSaveFileName(self, "Зберегти відомість", "vidomist.xlsx", "Excel Files (*.xlsx)")
        if save_path:
            wb.save(save_path)
            QMessageBox.information(self, "Успіх", f"Відомість успішно експортована!")


    def load_courses(self):
        """Завантаження предметів у випадаючий список (з опцією 'усі предмети')"""
        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()

        cursor.execute("SELECT course_id, name FROM Course ORDER BY name ASC")
        courses = cursor.fetchall()
        conn.close()

        self.course_dropdown.clear()
        self.course_dropdown.addItem("Усі предмети", None)  # <--- перший пункт

        for course_id, name in courses:
            self.course_dropdown.addItem(name, course_id)




# 📌 Вкладка4 "Рейтинг"
class RatingTab(QWidget):
    def __init__(self, readonly=False):
        super().__init__()
        self.readonly = readonly
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Верхній рядок: Вибір семестру + Вибір групи
        top_layout = QHBoxLayout()
        layout.addSpacing(20)  # Додає відступ у 20 пікселів зверху
        # Створення горизонтального макету для вибору семестра та групи
        top_layout = QHBoxLayout()

        # Лейбл і комбобокс для семестра
        semester_label = QLabel("Вибір семестра:")
        self.semester_cb = QComboBox()
        self.semester_cb.setFixedWidth(80)  
        self.semester_cb.addItem("Усі", None)
        for i in range(1, 9):
            self.semester_cb.addItem(str(i), i)

        # Лейбл і комбобокс для групи
        group_label = QLabel("Оберіть групу:")
        self.group_cb = QComboBox()
        self.group_cb.setFixedWidth(100)  
        self.group_cb.addItems(["усі", "КІ-21-01", "КІ-21-02"])

        # Додаємо віджети в макет
        top_layout.addWidget(semester_label, 0, Qt.AlignLeft)
        top_layout.addWidget(self.semester_cb, 0, Qt.AlignLeft)
        top_layout.addSpacing(40)  # Відстань 40px між групами елементів
        top_layout.addWidget(group_label, 0, Qt.AlignLeft)
        top_layout.addWidget(self.group_cb, 0, Qt.AlignLeft)

        # Додаємо розтягування праворуч, щоб залишити всі елементи вирівняними вліво
        top_layout.addStretch()

        layout.addLayout(top_layout)

        layout.addSpacing(20)

        filter_layout = QHBoxLayout()

        # Лейбл і поле для відсотка на стипендію
        scholarship_label = QLabel("Відсоток на стипендію:")
        self.scholarship_le = QLineEdit()
        self.scholarship_le.setFixedWidth(80)
        self.scholarship_le.setPlaceholderText("Напр. 30")

        # Кнопки
        self.list_btn = QPushButton("Список")
        self.show_all_btn = QPushButton("Показати усіх")

        btn_size = (120, 30)
        style = "background-color: #4CAF50; color: white; border: none; border-radius: 5px; font-size: 16px"
        for btn in (self.list_btn, self.show_all_btn):
            btn.setFixedSize(*btn_size)
            btn.setStyleSheet(style)

        # Додаємо віджети до макету з правильними відступами
        filter_layout.addWidget(scholarship_label, 0, Qt.AlignLeft)
        filter_layout.addWidget(self.scholarship_le, 0, Qt.AlignLeft)
        filter_layout.addSpacing(40)  # Відступ перед першою кнопкою
        filter_layout.addWidget(self.list_btn, 0, Qt.AlignLeft)
        filter_layout.addSpacing(40)  # Відступ перед другою кнопкою
        filter_layout.addWidget(self.show_all_btn, 0, Qt.AlignLeft)

        # Додаємо розтягування праворуч для вирівнювання по лівому краю
        filter_layout.addStretch()

        layout.addLayout(filter_layout)

        layout.addSpacing(20)

      

        # Таблиця рейтингу
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Студент", "Середній бал"])
        layout.addWidget(self.table)
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 80)

        # Контейнер для загального середнього балу та кнопки експорту
        bottom_layout = QHBoxLayout()
        
        self.avg_label = QLabel("Загальний середній бал: -")
        self.avg_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333; background-color: #f0f0f0; padding: 6px; border-radius: 5px;")
        self.avg_label.setAlignment(Qt.AlignCenter)
        bottom_layout.addWidget(self.avg_label, 2)

        self.export_btn = QPushButton("Експорт в Excel")
        self.export_btn.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; font-weight: bold; padding: 8px; border-radius: 5px;")
        self.export_btn.setFixedSize(130, 30)  # Встановлюємо фіксований розмір кнопки
        bottom_layout.addWidget(self.export_btn, 1)

        btn_size = (120, 30)
        
        layout.addLayout(bottom_layout)
        

        self.setLayout(layout)

        # Підключення сигналів
        self.semester_cb.currentIndexChanged.connect(self.load_ratings)
        self.group_cb.currentIndexChanged.connect(self.load_ratings)
        self.list_btn.clicked.connect(self.apply_percentage_filter)
        self.show_all_btn.clicked.connect(self.load_ratings)
        self.export_btn.clicked.connect(self.export_to_excel)

        self.load_ratings()

    def load_groups(self):
        """Завантажує список груп із БД та додає опцію 'усі'."""
        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT group_name FROM Student_info ORDER BY group_name")
        groups = cursor.fetchall()
        conn.close()

        self.group_cb.clear()
        self.group_cb.addItem("усі", "усі")  # Встановлюємо значення "усі"

        for group in groups:
            self.group_cb.addItem(group[0], group[0])  # Додаємо групи зі значенням group_name

    def load_ratings(self):
        """Завантаження рейтингу студентів для вибраного семестру та групи."""
        semester = self.semester_cb.currentData()  # Вибір семестру
        group = self.group_cb.currentText()  # Отримуємо текст вибраної групи (замість currentData)

        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()

        query = """
            SELECT S.last_name || ' ' || substr(S.first_name, 1, 1) || '.' 
                || CASE WHEN S.middle_name IS NOT NULL THEN substr(S.middle_name, 1, 1) || '.' ELSE '' END AS student_name,
                COALESCE(AVG(G.grade), 0) AS avg_grade
            FROM Student_info S
            LEFT JOIN Grades G ON S.student_id = G.student_id
            LEFT JOIN Course C ON G.course_id = C.course_id
        """
        conditions = []
        params = []

        if semester is not None:
            conditions.append("C.semester = ?")
            params.append(semester)

        if group and group != "усі":  # Якщо вибрана конкретна група
            conditions.append("S.group_name = ?")
            params.append(group)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY S.student_id ORDER BY avg_grade DESC"

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        self.rating_results = results
        self.populate_table(results)
        self.calculate_average(results)



    def populate_table(self, results):
        """Заповнення таблиці студентами та їхнім середнім балом."""
        self.table.setRowCount(len(results))
        for i, (student_name, avg_grade) in enumerate(results):
            self.table.setItem(i, 0, QTableWidgetItem(student_name))
            grade_text = "Немає оцінок" if avg_grade is None else f"{avg_grade:.2f}"
            self.table.setItem(i, 1, QTableWidgetItem(grade_text))

        # self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #4CAF50; color: white; font-size: 16px; font-weight: bold; padding: 8px; }"
        )
        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(1, 150)

    def calculate_average(self, results):
        """Обчислення загального середнього балу."""
        grades = [grade for _, grade in results if grade is not None]
        avg_score = sum(grades) / len(grades) if grades else None
        self.avg_label.setText(f"Загальний середній бал: {avg_score:.2f}" if avg_score else "Немає даних")

    def apply_percentage_filter(self):
        """Фільтрує рейтинг, показуючи тільки топ X% студентів."""
        try:
            percent = float(self.scholarship_le.text().strip())
            if not (0 <= percent <= 100):
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Помилка", "Введіть відсоток від 0 до 100!")
            return

        count = math.ceil(len(self.rating_results) * (percent / 100))
        filtered_results = self.rating_results[:count]
        self.populate_table(filtered_results)
        self.calculate_average(filtered_results)

    def export_to_excel(self):
        """Експортує рейтинг у файл Excel."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Зберегти як", "", "Excel Files (*.xlsx)")
        if not file_path:
            return

        data = [[self.table.item(row, 0).text(), self.table.item(row, 1).text()]
                for row in range(self.table.rowCount())]

        df = pd.DataFrame(data, columns=["Студент", "Середній бал"])
        df.to_excel(file_path, index=False)

        QMessageBox.information(self, "Експорт завершено", "Дані успішно експортовані в Excel!")




# 📌 Вкладка5 "Внесення оцінок"
class GradeEntryTab(QWidget):
    def __init__(self, student_id=None):
        super().__init__()
        self.student_id = student_id
        self.initUI()
        
    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Верхній блок: вибір студента
        main_layout.addSpacing(20)  # Додає відступ у 20 пікселів зверху
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Студент:"))
        top_layout.addSpacing(40)
        self.student_cb = QComboBox()
        top_layout.addWidget(self.student_cb)
        main_layout.addLayout(top_layout)
        main_layout.addSpacing(20)  # Додає відступ у 20 пікселів зверху
        top_layout.addStretch()
        
        # Таблиця предметів
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Предмет", "Семестр", "Оцінка"])
        self.table.setColumnHidden(0, True)

        # Встановлюємо фіксовану ширину колонок
        self.table.setColumnWidth(0, 50)   # ID
        self.table.setColumnWidth(1, 200)  # Предмет
        self.table.setColumnWidth(2, 100)  # Семестр
        self.table.setColumnWidth(2, 60)   # Оцінка

        main_layout.addWidget(self.table)


        self.table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #4CAF50; color: white; font-size: 16px; font-weight: bold; padding: 8px; }"
        )

        
        # Кнопка "Зберегти оцінки"
        main_layout.addSpacing(20)
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Зберегти оцінки")
        self.export_btn = QPushButton("Експорт в Excel")
        self.save_btn.setFixedSize(140, 30)
        self.export_btn.setFixedSize(140, 30)

        self.save_btn.setStyleSheet("background-color: #4CAF50; color: white; border: none; border-radius: 5px;font-size:16px")
        self.export_btn.setStyleSheet("background-color: #4CAF50; color: white; border: none; border-radius: 5px;font-size:16px")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addSpacing(40)  # Відступ перед першою кнопкою
        btn_layout.addWidget(self.export_btn)
        main_layout.addLayout(btn_layout)
        main_layout.addSpacing(20)
        
        self.setLayout(main_layout)
        btn_layout.addStretch()
        
        
        # Завантаження даних студентів і предметів
        self.load_students()
        self.student_cb.currentIndexChanged.connect(self.load_courses_for_student)
        self.save_btn.clicked.connect(self.save_grades)
        self.export_btn.clicked.connect(self.export_to_excel)
        
        # Завантажуємо предмети для поточного студента (якщо список не порожній)
        if self.student_cb.count() > 0:
            self.load_courses_for_student()
    
    def load_students(self):
        """Завантажуємо студентів у випадаючий список."""
        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT student_id, last_name, first_name 
            FROM Student_info 
            ORDER BY last_name ASC
        """)
        students = cursor.fetchall()
        conn.close()

        self.student_cb.clear()
        for s in students:
            # Формуємо рядок типу "Прізвище Ім'я"
            self.student_cb.addItem(f"{s[1]} {s[2]}", s[0])

        
        
    def load_courses_for_student(self):
        """Завантажуємо усі предмети в таблицю, відсортовані за семестром, з уже внесеними оцінками для обраного студента."""
        student_id = self.student_cb.currentData()
        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()

        # Запит повертає ID предмета, назву, оцінку, семестр і форму контролю, відсортовані за семестром
        cursor.execute("""
            SELECT Course.course_id, Course.name, 
                (SELECT grade FROM Grades WHERE student_id = ? AND course_id = Course.course_id LIMIT 1),
                Course.semester, Course.form_control
            FROM Course
            ORDER BY Course.semester, Course.course_id
        """, (student_id,))

        courses = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(courses))

        for row, course in enumerate(courses):
            course_id, course_name, grade, semester, form_control = course

            # ID предмета (не редагується)
            item_id = QTableWidgetItem(str(course_id))
            item_id.setFlags(item_id.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, item_id)

            # Назва предмета (не редагується, з підказкою)
            item_name = QTableWidgetItem(course_name)
            item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
            item_name.setToolTip(f"Семестр: {semester}\nФорма контролю: {form_control}")
            self.table.setItem(row, 1, item_name)

            # Семестр (не редагується)
            item_semester = QTableWidgetItem(str(semester))
            item_semester.setFlags(item_semester.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 2, item_semester)

            # Оцінка (користувач може вводити або редагувати значення)
            grade_val = "" if grade is None else str(grade)
            item_grade = QTableWidgetItem(grade_val)
            self.table.setItem(row, 3, item_grade)

        self.table.resizeColumnsToContents()




    def save_grades(self):
        """Зберігаємо введені оцінки, перевіряючи правильність введених даних."""
        student_id = self.student_cb.currentData()
        rows = self.table.rowCount()
        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()
        for row in range(rows):
            course_id = int(self.table.item(row, 0).text())
            grade_text = self.table.item(row, 2).text().strip()
            cursor.execute("DELETE FROM Grades WHERE student_id = ? AND course_id = ?", (student_id, course_id))
            if grade_text != "":
                try:
                    grade_val = int(grade_text)
                    if not (1 <= grade_val <= 12):
                        raise ValueError("Оцінка має бути в межах 1-12!")
                except ValueError:
                    QMessageBox.warning(self, "Помилка", f"Оцінка в рядку {row+1} має бути числом від 1 до 12!")
                    conn.rollback()
                    conn.close()
                    return
                cursor.execute("INSERT INTO Grades (student_id, course_id, grade) VALUES (?, ?, ?)",
                               (student_id, course_id, grade_val))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Успіх", "Оцінки збережено!")
        self.load_courses_for_student()
                
        
    def export_to_excel(self):
        """Експортує оцінки у файл Excel."""
        student_id = self.student_cb.currentData()
        student_name = self.student_cb.currentText()
        conn = sqlite3.connect("Student.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Course.name, Grades.grade 
            FROM Grades 
            JOIN Course ON Grades.course_id = Course.course_id 
            WHERE Grades.student_id = ?
        """, (student_id,))
        data = cursor.fetchall()
        conn.close()
        
        if not data:
            QMessageBox.warning(self, "Помилка", "Немає оцінок для експорту!")
            return
        
        df = pd.DataFrame(data, columns=["Предмет", "Оцінка"])
        filename = f"{student_name}_оцінки.xlsx"
        df.to_excel(filename, index=False)
        QMessageBox.information(self, "Успіх", f"Файл '{filename}' збережено!")



# 📌 Головне вікно програми
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget

class MainApp(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.position = user_data["position"]
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Система обліку успішності студентів")
        self.resize(1200, 800)

        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Додавання вкладок залежно від ролі
        if self.position in ("секретар", "заввідділенням"):
            self.tabs.addTab(StudentInfoTab(), "Інформація про студентів")
            self.tabs.addTab(CoursesTab(), "Предмети")
            self.tabs.addTab(GradesByCourseTab(), "Успішність по предмету")
            self.tabs.addTab(RatingTab(), "Рейтинг")
            self.tabs.addTab(GradeEntryTab(), "Внесення оцінок")
        elif self.position == "студент":
            self.tabs.addTab(GradesByCourseTab(student_id=self.user_data["id"]), "Мої оцінки")
            self.change_pwd_btn = QPushButton("Змінити пароль")
            self.change_pwd_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 6px; border-radius: 5px;")
            self.change_pwd_btn.clicked.connect(self.change_password)
            self.tabs.addTab(RatingTab(readonly=True), "Рейтинг")

            layout.addWidget(self.change_pwd_btn, alignment=Qt.AlignLeft)

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        # Оформлення вкладок
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                min-width: 190px;
                background: #CCCCCC;
            }
            QTabBar::tab:selected {
                background: #4CAF50;
                color: white;
            }
            QTabBar::tab:!selected {
                background: #CCCCCC;
                color: black;
            }
        """)

    def change_password(self):
        dialog = ChangePasswordDialog(self.user_data["id"], self.user_data["name"], self)
        dialog.exec_()




if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        user_data = login_dialog.user_data
        main_window = MainApp(user_data)
        main_window.show()
        sys.exit(app.exec_())

    
    