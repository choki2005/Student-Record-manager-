
from contextlib import closing
import sqlite3
from pathlib import Path

DB_NAME = Path(__file__).resolve().parent / "students.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                class_name TEXT NOT NULL,
                marks REAL NOT NULL
            )
        """)

        conn.commit()


def add_student(student_id, name, age, gender, class_name, marks):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students
            (student_id, name, age, gender, class_name, marks)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, name, age, gender, class_name, marks))

        conn.commit()


def get_students():
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students")

        return cursor.fetchall()


def update_student(student_id, name, age, gender, class_name, marks):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE students
            SET name = ?, age = ?, gender = ?, class_name = ?, marks = ?
            WHERE student_id = ?
        """, (name, age, gender, class_name, marks, student_id))

        conn.commit()

        return cursor.rowcount > 0


def delete_student(student_id):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,)
        )

        conn.commit()

        return cursor.rowcount > 0


def search_students(keyword):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        search_term = f"%{keyword}%"

        cursor.execute("""
            SELECT * FROM students
            WHERE student_id LIKE ?
            OR name LIKE ?
            OR class_name LIKE ?
        """, (search_term, search_term, search_term))

        return cursor.fetchall()
