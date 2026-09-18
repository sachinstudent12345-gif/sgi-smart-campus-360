import sqlite3

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "sgi_campus.db")

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()
    cursor = conn.cursor()

    # STUDENTS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campus_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            branch TEXT,
            semester INTEGER,
            attendance INTEGER DEFAULT 0
        )
    """)

    # COMPLAINTS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campus_id TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT,
            priority TEXT DEFAULT 'Normal',
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campus_id TEXT NOT NULL,
            attendance_date TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(campus_id, attendance_date)
        )
    """)
    # NOTICES TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # LAB REPORTS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lab_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campus_id TEXT NOT NULL,
            lab_name TEXT NOT NULL,
            computer_id TEXT NOT NULL,
            issue TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # HOSTEL COMPLAINTS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hostel_complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campus_id TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            room_no TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # DEMO STUDENT
    cursor.execute("""
        INSERT OR IGNORE INTO students
        (campus_id, name, password, branch, semester, attendance)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "SGI001",
        "Sachin Kumar",
        "1234",
        "CSE",
        3,
        82
    ))

    conn.commit()
    conn.close()

    print("✅ SGI Smart Campus 360 Database Ready!")


if __name__ == "__main__":
    init_db()