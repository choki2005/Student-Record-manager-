# Student Record Manager

## Project Overview
The Student Record Manager is a desktop application developed using Python and PyQt6. It allows users to manage student information, including student ID, name, age, gender, class and marks.

The application uses SQLite to store student records and Matplotlib to display student data through charts.

## Technologies Used
- Python 3.13
- PyQt6
- SQLite
- Matplotlib

## Features
- Home page and dashboard
- Add new student records
- View and manage student information
- Update existing student records
- Delete student records
- Search and view student records
- Validate student ID entries
- Display student statistics and charts

## Installation Instructions

1. Install Python 3.13.
2. Open the project folder in VS Code.
3. Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

4. Install the required packages:

```powershell
pip install -r requirements.txt
```

5. Run the application:

```powershell
python main.py
```

## Database
The application uses SQLite. The database file is named `students.db`. It stores student information locally.

## Developer
Name: Sonam Choki

Student ID: 08230194