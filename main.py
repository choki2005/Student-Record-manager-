
import sys
import sqlite3

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout,
    QComboBox, QSpinBox, QDoubleSpinBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QGroupBox, QMessageBox,
    QFrame, QScrollArea, QSizePolicy, QStackedWidget
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from database import (
    DB_NAME, init_db, add_student, get_students,
    delete_student, search_students
)


class StudentManager(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Student Record Manager | Sonam Choki | 08230194"
        )
        self.setMinimumSize(1000, 700)
        self.resize(1250, 850)

        self.selected_student_id = None

        init_db()
        self.create_menu()
        self.create_interface()
        self.apply_styles()
        self.load_students()

    # ================= MENU =================

    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_about(self):
        QMessageBox.about(
            self,
            "About Student Record Manager",
            "Student Record Manager\n\n"
            "Developed by: Sonam Choki\n"
            "Student ID: 08230194\n"
            "Framework: PyQt6\n"
            "Database: SQLite\n"
            "Chart: Matplotlib"
        )

    # ================= SCROLL AREA =================

    def create_scroll_area(self, content_widget):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        scroll.setWidget(content_widget)
        return scroll

    # ================= MAIN INTERFACE =================

    def create_interface(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # LEFT SIDEBAR
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 25, 15, 20)
        sidebar_layout.setSpacing(12)

        logo = QLabel("S R M")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(logo)

        logo_subtitle = QLabel("STUDENT RECORD MANAGER")
        logo_subtitle.setObjectName("logoSubtitle")
        logo_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(logo_subtitle)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setObjectName("sidebarLine")
        sidebar_layout.addWidget(separator)

        sidebar_layout.addSpacing(15)

        self.nav_buttons = []

        navigation = [
            ("⌂    Home", 0),
            ("▦    Dashboard", 1),
            ("＋    Manage Students", 2),
            ("▤    Student Records", 3)
        ]

        for label, index in navigation:
            button = QPushButton(label)
            button.setObjectName("navButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setCheckable(True)
            button.clicked.connect(
                lambda checked=False, i=index: self.navigate(i)
            )
            sidebar_layout.addWidget(button)
            self.nav_buttons.append(button)

        sidebar_layout.addStretch()

        developer = QLabel(
            "DEVELOPED BY\nSonam Choki\n\nSTUDENT ID\n08230194"
        )
        developer.setObjectName("developerInfo")
        developer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(developer)

        main_layout.addWidget(self.sidebar)

        # RIGHT CONTENT AREA
        right_area = QWidget()
        right_area.setObjectName("rightArea")

        right_layout = QVBoxLayout(right_area)
        right_layout.setContentsMargins(25, 20, 25, 15)
        right_layout.setSpacing(12)

        self.page_heading = QLabel("Welcome")
        self.page_heading.setObjectName("heading")

        self.page_subtitle = QLabel(
            "Manage student information in one place."
        )
        self.page_subtitle.setObjectName("subtitle")

        right_layout.addWidget(self.page_heading)
        right_layout.addWidget(self.page_subtitle)

        # STACKED PAGES
        self.pages = QStackedWidget()

        self.home_tab = QWidget()
        self.dashboard_tab = QWidget()
        self.manage_tab = QWidget()
        self.records_tab = QWidget()

        self.create_home_tab()
        self.create_dashboard_tab()
        self.create_manage_tab()
        self.create_records_tab()

        self.home_scroll = self.create_scroll_area(self.home_tab)
        self.dashboard_scroll = self.create_scroll_area(
            self.dashboard_tab
        )
        self.manage_scroll = self.create_scroll_area(
            self.manage_tab
        )
        self.records_scroll = self.create_scroll_area(
            self.records_tab
        )

        self.pages.addWidget(self.home_scroll)
        self.pages.addWidget(self.dashboard_scroll)
        self.pages.addWidget(self.manage_scroll)
        self.pages.addWidget(self.records_scroll)

        right_layout.addWidget(self.pages, 1)

        footer = QLabel(
            "Student Record Manager | Developed using PyQt6 and SQLite"
        )
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        right_layout.addWidget(footer)

        main_layout.addWidget(right_area, 1)

        self.navigate(0)

    # ================= NAVIGATION =================

    def navigate(self, index):

        self.pages.setCurrentIndex(index)

        headings = [
            ("Welcome", "Manage student information in one place."),
            ("Dashboard Overview",
             "Monitor student statistics and academic performance."),
            ("Manage Students",
             "Register, update and manage student information."),
            ("Student Records",
             "View, search and select student records.")
        ]

        self.page_heading.setText(headings[index][0])
        self.page_subtitle.setText(headings[index][1])

        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == index)

        if index == 1:
            self.update_summary()
            self.update_chart()

    # ================= HOMEPAGE =================

    def create_home_tab(self):

        layout = QVBoxLayout(self.home_tab)
        layout.setContentsMargins(20, 20, 20, 25)
        layout.setSpacing(22)

        banner = QFrame()
        banner.setObjectName("welcomeBanner")
        banner.setMinimumHeight(190)

        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(30, 25, 30, 25)
        banner_layout.setSpacing(12)

        welcome = QLabel("Welcome to Student Record Manager")
        welcome.setObjectName("welcomeTitle")
        welcome.setWordWrap(True)

        description = QLabel(
            "A simple and efficient desktop application for organising "
            "student information and monitoring academic performance."
        )
        description.setObjectName("welcomeDescription")
        description.setWordWrap(True)

        student_details = QLabel(
            "DEVELOPED BY   Sonam Choki     |     STUDENT ID   08230194"
        )
        student_details.setObjectName("studentDetails")
        student_details.setWordWrap(True)

        banner_layout.addWidget(welcome)
        banner_layout.addWidget(description)
        banner_layout.addStretch()
        banner_layout.addWidget(student_details)

        layout.addWidget(banner)

        section_title = QLabel("Explore the system")
        section_title.setObjectName("sectionTitle")
        layout.addWidget(section_title)

        section_description = QLabel(
            "Choose a section below to manage records or view student performance."
        )
        section_description.setObjectName("subtitle")
        section_description.setWordWrap(True)
        layout.addWidget(section_description)

        cards_layout = QGridLayout()
        cards_layout.setSpacing(15)

        cards_layout.addWidget(
            self.create_home_card(
                "01  |  DASHBOARD",
                "View student statistics, average marks and performance charts.",
                "Open Dashboard",
                lambda: self.navigate(1)
            ), 0, 0
        )

        cards_layout.addWidget(
            self.create_home_card(
                "02  |  MANAGE STUDENTS",
                "Register new students and update or remove existing information.",
                "Manage Students",
                lambda: self.navigate(2)
            ), 0, 1
        )

        cards_layout.addWidget(
            self.create_home_card(
                "03  |  STUDENT RECORDS",
                "Browse the student table and search for a particular record.",
                "View Records",
                lambda: self.navigate(3)
            ), 1, 0, 1, 2
        )

        layout.addLayout(cards_layout)

        note = QLabel(
            "TIP: Use the navigation menu on the left to move between "
            "sections. Your student records are stored in the SQLite database."
        )
        note.setObjectName("instruction")
        note.setWordWrap(True)

        layout.addWidget(note)
        layout.addStretch()

    def create_home_card(self, heading, description, button_text, action):

        card = QFrame()
        card.setObjectName("homeCard")
        card.setMinimumHeight(175)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 18, 20, 18)
        card_layout.setSpacing(10)

        title = QLabel(heading)
        title.setObjectName("homeCardTitle")
        title.setWordWrap(True)

        detail = QLabel(description)
        detail.setObjectName("homeCardDescription")
        detail.setWordWrap(True)

        button = QPushButton(button_text)
        button.setObjectName("homeButton")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(action)

        card_layout.addWidget(title)
        card_layout.addWidget(detail)
        card_layout.addStretch()
        card_layout.addWidget(button)

        return card

    # ================= DASHBOARD =================

    def create_dashboard_tab(self):

        layout = QVBoxLayout(self.dashboard_tab)
        layout.setContentsMargins(20, 25, 20, 25)
        layout.setSpacing(20)

        title = QLabel("Student Performance Summary")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        description = QLabel(
            "An overview of student numbers and academic performance."
        )
        description.setObjectName("subtitle")
        layout.addWidget(description)

        stats_layout = QGridLayout()
        stats_layout.setSpacing(15)

        self.total_label = QLabel("0")
        self.average_label = QLabel("0%")
        self.highest_label = QLabel("0%")
        self.topper_label = QLabel("None")

        stats_layout.addWidget(
            self.create_stat_card(
                "TOTAL STUDENTS", self.total_label, "#681F3D"
            ), 0, 0
        )
        stats_layout.addWidget(
            self.create_stat_card(
                "AVERAGE MARKS", self.average_label, "#A66B32"
            ), 0, 1
        )
        stats_layout.addWidget(
            self.create_stat_card(
                "HIGHEST MARKS", self.highest_label, "#7A5367"
            ), 1, 0
        )
        stats_layout.addWidget(
            self.create_stat_card(
                "TOP PERFORMER", self.topper_label, "#526D60"
            ), 1, 1
        )

        layout.addLayout(stats_layout)

        chart_group = QGroupBox("Student Performance Distribution")
        chart_layout = QVBoxLayout(chart_group)

        self.figure = Figure(figsize=(8, 4))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setMinimumHeight(320)
        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        chart_layout.addWidget(self.canvas)
        layout.addWidget(chart_group)

        refresh_button = QPushButton("Refresh Dashboard")
        refresh_button.setObjectName("refreshButton")
        refresh_button.clicked.connect(self.refresh_dashboard)

        layout.addWidget(
            refresh_button,
            alignment=Qt.AlignmentFlag.AlignLeft
        )
        layout.addStretch()

    def create_stat_card(self, heading, value_label, color):

        card = QFrame()
        card.setObjectName("statCard")
        card.setStyleSheet(f"""
            QFrame#statCard {{
                background-color: {color};
                border-radius: 12px;
                min-height: 115px;
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 15, 18, 15)

        heading_label = QLabel(heading)
        heading_label.setStyleSheet(
            "color: white; font-size: 12px; font-weight: bold;"
        )

        value_label.setStyleSheet(
            "color: white; font-size: 23px; font-weight: bold;"
        )
        value_label.setWordWrap(True)

        card_layout.addWidget(heading_label)
        card_layout.addWidget(value_label)

        return card

    # ================= MANAGE STUDENTS =================

    def create_manage_tab(self):

        layout = QVBoxLayout(self.manage_tab)
        layout.setContentsMargins(20, 25, 20, 25)
        layout.setSpacing(20)

        title = QLabel("Student Registration Form")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        description = QLabel(
            "Enter the required details to register or update a student."
        )
        description.setObjectName("subtitle")
        layout.addWidget(description)

        form_group = QGroupBox("Student Information")
        form_layout = QGridLayout(form_group)
        form_layout.setContentsMargins(20, 25, 20, 25)
        form_layout.setHorizontalSpacing(18)
        form_layout.setVerticalSpacing(20)

        form_layout.addWidget(QLabel("Student ID:"), 0, 0)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter numeric student ID")
        form_layout.addWidget(self.id_input, 0, 1)

        form_layout.addWidget(QLabel("Full Name:"), 0, 2)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter full name")
        form_layout.addWidget(self.name_input, 0, 3)

        form_layout.addWidget(QLabel("Age:"), 1, 0)

        self.age_input = QSpinBox()
        self.age_input.setRange(5, 100)
        self.age_input.setValue(15)
        form_layout.addWidget(self.age_input, 1, 1)

        form_layout.addWidget(QLabel("Gender:"), 1, 2)

        self.gender_input = QComboBox()
        self.gender_input.addItems(
            ["Select Gender", "Male", "Female", "Other"]
        )
        form_layout.addWidget(self.gender_input, 1, 3)

        form_layout.addWidget(QLabel("Class:"), 2, 0)

        self.class_input = QComboBox()
        self.class_input.addItems(
            ["Select Class", "VII", "VIII", "IX", "X", "XI", "XII"]
        )
        form_layout.addWidget(self.class_input, 2, 1)

        form_layout.addWidget(QLabel("Marks (%):"), 2, 2)

        self.marks_input = QDoubleSpinBox()
        self.marks_input.setRange(0, 100)
        self.marks_input.setDecimals(2)
        self.marks_input.setSuffix(" %")
        form_layout.addWidget(self.marks_input, 2, 3)

        layout.addWidget(form_group)

        instruction = QLabel(
            "To update or delete a student, select the student's record "
            "from the Student Records section first. You can also change "
            "the Student ID when updating a record."
        )
        instruction.setObjectName("instruction")
        instruction.setWordWrap(True)
        layout.addWidget(instruction)

        button_group = QGroupBox("Student Record Actions")
        button_layout = QGridLayout(button_group)
        button_layout.setSpacing(15)

        self.add_button = QPushButton("Add Student")
        self.update_button = QPushButton("Update Student")
        self.delete_button = QPushButton("Delete Student")
        self.clear_button = QPushButton("Clear Form")

        self.add_button.setObjectName("addButton")
        self.update_button.setObjectName("updateButton")
        self.delete_button.setObjectName("deleteButton")

        button_layout.addWidget(self.add_button, 0, 0)
        button_layout.addWidget(self.update_button, 0, 1)
        button_layout.addWidget(self.delete_button, 1, 0)
        button_layout.addWidget(self.clear_button, 1, 1)

        layout.addWidget(button_group)
        layout.addStretch()

        self.add_button.clicked.connect(self.add_record)
        self.update_button.clicked.connect(self.update_record)
        self.delete_button.clicked.connect(self.delete_record)
        self.clear_button.clicked.connect(self.clear_form)

    # ================= STUDENT RECORDS =================

    def create_records_tab(self):

        layout = QVBoxLayout(self.records_tab)
        layout.setContentsMargins(20, 25, 20, 25)
        layout.setSpacing(18)

        title = QLabel("Student Records")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        description = QLabel(
            "View, search and select registered student information."
        )
        description.setObjectName("subtitle")
        layout.addWidget(description)

        search_group = QGroupBox("Search Student Records")
        search_layout = QVBoxLayout(search_group)
        search_layout.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Enter student ID, name or class..."
        )

        search_buttons = QHBoxLayout()

        self.search_button = QPushButton("Search")
        self.show_all_button = QPushButton("Show All")

        search_buttons.addWidget(self.search_button)
        search_buttons.addWidget(self.show_all_button)

        search_layout.addWidget(self.search_input)
        search_layout.addLayout(search_buttons)
        layout.addWidget(search_group)

        table_group = QGroupBox("Registered Students")
        table_layout = QVBoxLayout(table_group)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Student ID", "Full Name", "Age",
            "Gender", "Class", "Marks (%)"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(400)

        table_layout.addWidget(self.table)
        layout.addWidget(table_group)

        self.selection_label = QLabel(
            "Select a student row to update or delete a record."
        )
        self.selection_label.setObjectName("instruction")
        self.selection_label.setWordWrap(True)
        layout.addWidget(self.selection_label)

        layout.addStretch()

        self.search_button.clicked.connect(self.search_record)
        self.show_all_button.clicked.connect(self.show_all_records)
        self.search_input.returnPressed.connect(self.search_record)
        self.table.cellClicked.connect(self.select_student)

    # ================= VALIDATION =================

    def validate_inputs(self):

        student_id = self.id_input.text().strip()
        name = self.name_input.text().strip()

        if not student_id or not name:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter both Student ID and Full Name."
            )
            return False

        # Student ID must contain numbers only.
        # isdigit() allows IDs such as 08230194 to retain their leading zero.
        if not student_id.isdigit():
            QMessageBox.warning(
                self,
                "Invalid Student ID",
                "Student ID must contain numbers only."
            )
            return False

        if self.gender_input.currentIndex() == 0:
            QMessageBox.warning(
                self, "Invalid Input", "Please select a gender."
            )
            return False

        if self.class_input.currentIndex() == 0:
            QMessageBox.warning(
                self, "Invalid Input", "Please select a class."
            )
            return False

        if not any(char.isalpha() for char in name):
            QMessageBox.warning(
                self, "Invalid Name",
                "Please enter a valid student name."
            )
            return False

        if not all(
            char.isalpha() or char.isspace() or char in "-'."
            for char in name
        ):
            QMessageBox.warning(
                self, "Invalid Name",
                "Name should contain letters only."
            )
            return False

        return True

    # ================= ADD STUDENT =================

    def add_record(self):

        if not self.validate_inputs():
            return

        try:
            add_student(
                self.id_input.text().strip(),
                self.name_input.text().strip(),
                self.age_input.value(),
                self.gender_input.currentText(),
                self.class_input.currentText(),
                self.marks_input.value()
            )

            QMessageBox.information(
                self, "Success",
                "Student record added successfully!"
            )

            self.load_students()
            self.clear_form()
            self.search_input.clear()
            self.navigate(3)

        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self, "Duplicate ID",
                "This Student ID already exists. Please use a different ID."
            )

        except sqlite3.Error as error:
            QMessageBox.critical(
                self, "Database Error", str(error)
            )

    # ================= LOAD AND DISPLAY =================

    def load_students(self):

        try:
            records = get_students()
            self.display_records(records)
            self.update_summary()
            self.update_chart()

        except sqlite3.Error as error:
            QMessageBox.critical(
                self, "Database Error", str(error)
            )

    def display_records(self, records):

        self.table.setRowCount(len(records))

        for row_index, record in enumerate(records):
            for column_index, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )
                self.table.setItem(row_index, column_index, item)

        self.table.clearSelection()

    def show_all_records(self):

        self.selected_student_id = None
        self.selection_label.setText(
            "Select a student row to update or delete a record."
        )
        self.search_input.clear()
        self.load_students()

    # ================= DASHBOARD STATISTICS =================

    def update_summary(self):

        records = get_students()

        if not records:
            self.total_label.setText("0")
            self.average_label.setText("0%")
            self.highest_label.setText("0%")
            self.topper_label.setText("None")
            return

        marks = [float(record[5]) for record in records]
        average = sum(marks) / len(marks)

        highest = max(
            records, key=lambda record: float(record[5])
        )

        self.total_label.setText(str(len(records)))
        self.average_label.setText(f"{average:.2f}%")
        self.highest_label.setText(f"{max(marks):.2f}%")
        self.topper_label.setText(str(highest[1]))

    # ================= PERFORMANCE CHART =================

    def update_chart(self):

        records = get_students()
        marks = [float(record[5]) for record in records]

        categories = [
            "0–49", "50–59", "60–69",
            "70–79", "80–89", "90–100"
        ]

        counts = [
            sum(1 for mark in marks if 0 <= mark < 50),
            sum(1 for mark in marks if 50 <= mark < 60),
            sum(1 for mark in marks if 60 <= mark < 70),
            sum(1 for mark in marks if 70 <= mark < 80),
            sum(1 for mark in marks if 80 <= mark < 90),
            sum(1 for mark in marks if 90 <= mark <= 100)
        ]

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        bars = ax.bar(
            categories,
            counts,
            color="#8B3A56",
            width=0.55
        )

        ax.set_ylabel("Number of Students")
        ax.set_xlabel("Marks Range (%)")
        ax.set_title(
            "Student Performance Distribution",
            color="#681F3D",
            fontsize=12,
            fontweight="bold"
        )

        ax.set_ylim(0, max(counts, default=0) + 1.5)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.set_axisbelow(True)

        for bar, count in zip(bars, counts):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.1,
                str(count),
                ha="center",
                va="bottom",
                fontweight="bold"
            )

        self.figure.tight_layout()
        self.canvas.draw()

    def refresh_dashboard(self):

        try:
            self.update_summary()
            self.update_chart()

            QMessageBox.information(
                self, "Dashboard Refreshed",
                "Dashboard updated successfully."
            )

        except sqlite3.Error as error:
            QMessageBox.critical(
                self, "Database Error", str(error)
            )

    # ================= SELECT STUDENT =================

    def select_student(self, row, column):

        item = self.table.item(row, 0)

        if item is None:
            return

        # Keep the original ID so the correct database row is updated.
        self.selected_student_id = item.text()

        # Allow the user to edit the Student ID.
        self.id_input.setText(item.text())
        self.id_input.setReadOnly(False)

        self.name_input.setText(
            self.table.item(row, 1).text()
        )
        self.age_input.setValue(
            int(self.table.item(row, 2).text())
        )
        self.gender_input.setCurrentText(
            self.table.item(row, 3).text()
        )
        self.class_input.setCurrentText(
            self.table.item(row, 4).text()
        )
        self.marks_input.setValue(
            float(self.table.item(row, 5).text())
        )

        self.selection_label.setText(
            f"Selected Student: {self.selected_student_id}"
        )

        self.navigate(2)

    # ================= UPDATE STUDENT =================

    def update_record(self):

        if not self.selected_student_id:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a student from the Student Records section first."
            )
            return

        if not self.validate_inputs():
            return

        new_student_id = self.id_input.text().strip()

        try:
            # Use the original ID in WHERE and the new ID in SET.
            # DB_NAME is imported from database.py, so the correct
            # existing database file is always used.
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    UPDATE students
                    SET student_id = ?,
                        name = ?,
                        age = ?,
                        gender = ?,
                        class_name = ?,
                        marks = ?
                    WHERE student_id = ?
                """, (
                    new_student_id,
                    self.name_input.text().strip(),
                    self.age_input.value(),
                    self.gender_input.currentText(),
                    self.class_input.currentText(),
                    self.marks_input.value(),
                    self.selected_student_id
                ))

                updated = cursor.rowcount > 0

            if updated:
                QMessageBox.information(
                    self,
                    "Success",
                    "Student record updated successfully!"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Not Found",
                    "Student record could not be found."
                )
                return

            self.load_students()
            self.clear_form()
            self.navigate(3)

        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self,
                "Duplicate Student ID",
                "This Student ID already belongs to another student. "
                "Please use a different ID."
            )

        except sqlite3.Error as error:
            QMessageBox.critical(
                self, "Database Error", str(error)
            )

    # ================= DELETE STUDENT =================

    def delete_record(self):

        if not self.selected_student_id:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a student from the Student Records section first."
            )
            return

        answer = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete {self.selected_student_id}?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:

            try:
                success = delete_student(self.selected_student_id)

                if success:
                    QMessageBox.information(
                        self, "Deleted",
                        "Student record deleted successfully!"
                    )
                else:
                    QMessageBox.warning(
                        self, "Not Found",
                        "Student record could not be found."
                    )

                self.load_students()
                self.clear_form()
                self.navigate(3)

            except sqlite3.Error as error:
                QMessageBox.critical(
                    self, "Database Error", str(error)
                )

    # ================= SEARCH STUDENT =================

    def search_record(self):

        keyword = self.search_input.text().strip()

        if not keyword:
            QMessageBox.warning(
                self, "Search Required",
                "Please enter a student ID, name or class."
            )
            return

        try:
            records = search_students(keyword)
            self.display_records(records)

            self.selected_student_id = None
            self.id_input.setReadOnly(False)

            self.selection_label.setText(
                "Select a student row to update or delete a record."
            )

            if not records:
                QMessageBox.information(
                    self, "No Results",
                    "No matching student records found."
                )

        except sqlite3.Error as error:
            QMessageBox.critical(
                self, "Database Error", str(error)
            )

    # ================= CLEAR FORM =================

    def clear_form(self):

        self.id_input.clear()
        self.id_input.setReadOnly(False)

        self.name_input.clear()
        self.age_input.setValue(15)
        self.gender_input.setCurrentIndex(0)
        self.class_input.setCurrentIndex(0)
        self.marks_input.setValue(0)

        self.selected_student_id = None
        self.table.clearSelection()

        self.selection_label.setText(
            "Select a student row to update or delete a record."
        )

    # ================= STYLING =================

    def apply_styles(self):

        self.setStyleSheet("""

            QMainWindow {
                background-color: #F7F0E8;
            }

            QWidget {
                color: #402431;
                font-size: 13px;
            }

            QFrame#sidebar {
                background-color: #681F3D;
                border: none;
            }

            QLabel#logo {
                color: #FFFFFF;
                font-size: 29px;
                font-weight: bold;
                padding: 8px;
            }

            QLabel#logoSubtitle {
                color: #EAD5DD;
                font-size: 9px;
                font-weight: bold;
            }

            QFrame#sidebarLine {
                color: #A66B7F;
                background-color: #A66B7F;
                max-height: 1px;
            }

            QPushButton#navButton {
                background-color: transparent;
                color: #F7EAF0;
                border: none;
                border-radius: 8px;
                text-align: left;
                padding: 15px 12px;
                font-size: 13px;
                font-weight: bold;
                min-height: 24px;
            }

            QPushButton#navButton:hover {
                background-color: #843652;
            }

            QPushButton#navButton:checked {
                background-color: #F7F0E8;
                color: #681F3D;
            }

            QLabel#developerInfo {
                color: #F3DDE5;
                background-color: #542039;
                border-radius: 8px;
                padding: 12px;
                font-size: 11px;
            }

            QWidget#rightArea {
                background-color: #F7F0E8;
            }

            QLabel#heading {
                font-size: 26px;
                font-weight: bold;
                color: #681F3D;
            }

            QLabel#subtitle {
                color: #806875;
                font-size: 13px;
            }

            QLabel#footer {
                color: #806875;
                font-size: 11px;
                padding: 5px;
            }

            QLabel#sectionTitle {
                font-size: 21px;
                font-weight: bold;
                color: #681F3D;
            }

            QLabel#instruction {
                color: #806875;
                background-color: #F3E7EC;
                padding: 12px;
                border-radius: 6px;
            }

            QStackedWidget {
                background-color: #FBF8F4;
                border: 1px solid #E4CFD6;
                border-radius: 10px;
            }

            QScrollArea {
                background-color: #FBF8F4;
                border: none;
                border-radius: 10px;
            }

            QScrollArea > QWidget > QWidget {
                background-color: #FBF8F4;
            }

            QScrollBar:vertical {
                background-color: #F0E5E8;
                width: 12px;
                margin: 2px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background-color: #8B3A56;
                min-height: 35px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #681F3D;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }

            QFrame#welcomeBanner {
                background-color: #681F3D;
                border-radius: 15px;
            }

            QLabel#welcomeTitle {
                color: white;
                font-size: 27px;
                font-weight: bold;
            }

            QLabel#welcomeDescription {
                color: #F7EAF0;
                font-size: 13px;
            }

            QLabel#studentDetails {
                color: #FFE0A8;
                font-size: 12px;
                font-weight: bold;
            }

            QFrame#homeCard {
                background-color: white;
                border: 1px solid #E4CFD6;
                border-radius: 12px;
            }

            QLabel#homeCardTitle {
                color: #681F3D;
                font-size: 14px;
                font-weight: bold;
            }

            QLabel#homeCardDescription {
                color: #66515A;
                font-size: 12px;
            }

            QPushButton#homeButton {
                background-color: #681F3D;
                color: white;
                padding: 10px;
                border-radius: 7px;
                font-weight: bold;
            }

            QPushButton#homeButton:hover {
                background-color: #843652;
            }

            QGroupBox {
                background-color: white;
                border: 1px solid #E4CFD6;
                border-radius: 10px;
                margin-top: 14px;
                padding: 18px;
                font-weight: bold;
                color: #681F3D;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 6px;
            }

            QLineEdit, QComboBox,
            QSpinBox, QDoubleSpinBox {
                background-color: #FFFDFC;
                border: 1px solid #D8C3CC;
                border-radius: 6px;
                padding: 10px;
                min-height: 22px;
                color: #402431;
            }

            QLineEdit:focus,
            QComboBox:focus,
            QSpinBox:focus,
            QDoubleSpinBox:focus {
                border: 2px solid #A66B32;
            }

            QPushButton {
                background-color: #E9DCE1;
                color: #681F3D;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                min-height: 22px;
            }

            QPushButton:hover {
                background-color: #DCC3CE;
            }

            QPushButton#addButton {
                background-color: #681F3D;
                color: white;
            }

            QPushButton#addButton:hover {
                background-color: #843652;
            }

            QPushButton#updateButton {
                background-color: #A66B32;
                color: white;
            }

            QPushButton#updateButton:hover {
                background-color: #895525;
            }

            QPushButton#deleteButton {
                background-color: #A33E48;
                color: white;
            }

            QPushButton#deleteButton:hover {
                background-color: #862F39;
            }

            QPushButton#refreshButton {
                background-color: #681F3D;
                color: white;
                max-width: 220px;
            }

            QTableWidget {
                background-color: white;
                alternate-background-color: #F8F0F3;
                border: 1px solid #E4CFD6;
                border-radius: 8px;
                gridline-color: #EADDE2;
                selection-background-color: #DCC3CE;
                selection-color: #402431;
            }

            QHeaderView::section {
                background-color: #681F3D;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
            }

            QMenuBar {
                background-color: #681F3D;
                color: white;
                padding: 5px;
            }

            QMenuBar::item:selected {
                background-color: #843652;
            }

            QMenu {
                background-color: white;
                color: #681F3D;
            }

            QMenu::item:selected {
                background-color: #E9DCE1;
            }

        """)


# ================= RUN APPLICATION =================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = StudentManager()
    window.show()

    sys.exit(app.exec())
