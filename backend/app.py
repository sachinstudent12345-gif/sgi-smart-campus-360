import os

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from database import get_db, init_db


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
ASSETS_DIR = os.path.join(BASE_DIR, "..", "frontend", "assets")


# ==========================================
# FLASK APP
# ==========================================

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR
)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://sachinstudent12345-gif.github.io"
        ]
    }
})
init_db()

# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# ==========================================
# ASSETS
# SGI CAMPUS PHOTO + DEVELOPER PHOTOS
# ==========================================

@app.route("/assets/<path:filename>")
def serve_assets(filename):

    return send_from_directory(
        ASSETS_DIR,
        filename
    )


# ==========================================
# FRONTEND FILES
# ==========================================

@app.route("/<path:path>")
def frontend_files(path):

    return send_from_directory(
        FRONTEND_DIR,
        path
    )

# ==========================================
# ADMIN LOGIN
# ==========================================

@app.route("/api/admin/login", methods=["POST"])
def admin_login():

    data = request.get_json()

    admin_id = data.get("admin_id")
    password = data.get("password")

    if not admin_id or not password:
        return jsonify({
            "success": False,
            "message": "Admin ID and password are required."
        })

    # Demo Admin Credentials
    if admin_id == "admin" and password == "admin123":

        return jsonify({
            "success": True,
            "message": "Admin login successful.",
            "admin": {
                "admin_id": "admin",
                "name": "SGI Administrator"
            }
        })

    return jsonify({
        "success": False,
        "message": "Invalid Admin ID or Password."
    })

# ==========================================
# STUDENT LOGIN
# ==========================================

@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    campus_id = data.get("campus_id")
    password = data.get("password")

    if not campus_id or not password:

        return jsonify({
            "success": False,
            "message": "Campus ID and password are required."
        })

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, campus_id, name, branch, semester, attendance
        FROM students
        WHERE campus_id = ? AND password = ?
    """, (campus_id, password))

    student = cursor.fetchone()

    conn.close()

    if student:

        return jsonify({
            "success": True,
            "student": dict(student)
        })

    return jsonify({
        "success": False,
        "message": "Invalid Campus ID or Password."
    })


# ==========================================
# STUDENT REGISTRATION
# ==========================================

@app.route("/api/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    campus_id = data.get("campus_id")
    branch = data.get("branch")
    semester = data.get("semester")
    password = data.get("password")

    if not name or not campus_id or not branch or not semester or not password:

        return jsonify({
            "success": False,
            "message": "All fields are required."
        })

    conn = get_db()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO students
            (campus_id, name, password, branch, semester, attendance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            campus_id,
            name,
            password,
            branch,
            int(semester),
            0
        ))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Account created successfully."
        })

    except Exception as error:

        if "UNIQUE constraint failed" in str(error):

            return jsonify({
                "success": False,
                "message": "Campus ID already exists."
            })

        return jsonify({
            "success": False,
            "message": "Registration failed."
        })

    finally:

        conn.close()


# ==========================================
# SMART COMPLAINTS
# ==========================================

@app.route("/api/complaints", methods=["POST"])
def create_complaint():

    data = request.get_json()

    campus_id = data.get("campus_id")
    category = data.get("category")
    description = data.get("description")
    location = data.get("location", "")
    priority = data.get("priority", "Normal")

    if not campus_id or not category or not description:

        return jsonify({
            "success": False,
            "message": "Campus ID, category and description are required."
        })

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints
        (campus_id, category, description, location, priority)
        VALUES (?, ?, ?, ?, ?)
    """, (
        campus_id,
        category,
        description,
        location,
        priority
    ))

    complaint_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Complaint submitted successfully.",
        "complaint_id": complaint_id
    })


# ==========================================
# GET STUDENT COMPLAINTS
# ==========================================

@app.route("/api/complaints/<campus_id>", methods=["GET"])
def get_complaints(campus_id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            category,
            description,
            location,
            priority,
            status,
            created_at
        FROM complaints
        WHERE campus_id = ?
        ORDER BY id DESC
    """, (campus_id,))

    complaints = cursor.fetchall()

    conn.close()

    return jsonify({
        "success": True,
        "complaints": [dict(row) for row in complaints]
    })


# ==========================================
# ADMIN - GET ALL COMPLAINTS
# CAMPUS + HOSTEL + LAB
# ==========================================

@app.route("/api/admin/complaints", methods=["GET"])
def get_all_complaints():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            campus_id,
            category,
            description,
            location,
            priority,
            status,
            created_at,
            'Campus' AS complaint_type
        FROM complaints

        UNION ALL

        SELECT
            id,
            campus_id,
            'Hostel - ' || category AS category,
            description,
            'Room ' || room_no AS location,
            'Normal' AS priority,
            status,
            created_at,
            'Hostel' AS complaint_type
        FROM hostel_complaints

        UNION ALL

        SELECT
            id,
            campus_id,
            'Lab - ' || lab_name AS category,
            issue AS description,
            'Computer ' || computer_id AS location,
            'Normal' AS priority,
            status,
            created_at,
            'Lab' AS complaint_type
        FROM lab_reports

        ORDER BY id DESC
    """)

    complaints = cursor.fetchall()

    conn.close()

    return jsonify({
        "success": True,
        "complaints": [dict(row) for row in complaints]
    })


# ==========================================
# ADMIN - UPDATE COMPLAINT STATUS
# ==========================================

@app.route(
    "/api/admin/complaints/<int:complaint_id>",
    methods=["PUT"]
)
def update_complaint_status(complaint_id):

    data = request.get_json()

    status = data.get("status")

    allowed_statuses = [
        "Pending",
        "In Progress",
        "Resolved"
    ]

    if status not in allowed_statuses:

        return jsonify({
            "success": False,
            "message": "Invalid complaint status."
        })

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE complaints
        SET status = ?
        WHERE id = ?
    """, (
        status,
        complaint_id
    ))

    if cursor.rowcount == 0:

        conn.close()

        return jsonify({
            "success": False,
            "message": "Complaint not found."
        })

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Complaint status updated successfully."
    })


# ==========================================
# SMART LAB - SUBMIT REPORT
# ==========================================

@app.route("/api/lab-reports", methods=["POST"])
def create_lab_report():

    data = request.get_json()

    campus_id = data.get("campus_id")
    lab_name = data.get("lab_name")
    computer_id = data.get("computer_id")
    issue = data.get("issue")

    if not campus_id or not lab_name or not computer_id or not issue:

        return jsonify({
            "success": False,
            "message": "Campus ID, lab name, computer ID and issue are required."
        })

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO lab_reports
        (campus_id, lab_name, computer_id, issue)
        VALUES (?, ?, ?, ?)
    """, (
        campus_id,
        lab_name,
        computer_id,
        issue
    ))

    report_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Lab issue reported successfully.",
        "report_id": report_id
    })


# ==========================================
# SMART LAB - GET STUDENT REPORTS
# ==========================================

@app.route("/api/lab-reports/<campus_id>", methods=["GET"])
def get_lab_reports(campus_id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            lab_name,
            computer_id,
            issue,
            status,
            created_at
        FROM lab_reports
        WHERE campus_id = ?
        ORDER BY id DESC
    """, (campus_id,))

    reports = cursor.fetchall()

    conn.close()

    return jsonify({
        "success": True,
        "reports": [dict(row) for row in reports]
    })


# ==========================================
# ADMIN - UPDATE LAB REPORT STATUS
# ==========================================

@app.route(
    "/api/admin/lab-reports/<int:report_id>",
    methods=["PUT"]
)
def update_lab_report_status(report_id):

    data = request.get_json()

    status = data.get("status")

    allowed_statuses = [
        "Pending",
        "In Progress",
        "Resolved"
    ]

    if status not in allowed_statuses:

        return jsonify({
            "success": False,
            "message": "Invalid lab report status."
        })

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE lab_reports
        SET status = ?
        WHERE id = ?
    """, (
        status,
        report_id
    ))

    if cursor.rowcount == 0:

        conn.close()

        return jsonify({
            "success": False,
            "message": "Lab report not found."
        })

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Lab report status updated successfully."
    })


# ==========================================
# ADMIN - UPDATE HOSTEL COMPLAINT STATUS
# ==========================================

@app.route(
    "/api/admin/hostel-complaints/<int:complaint_id>",
    methods=["PUT"]
)
def update_hostel_complaint_status(complaint_id):

    data = request.get_json()

    status = data.get("status")

    allowed_statuses = [
        "Pending",
        "In Progress",
        "Resolved"
    ]

    if status not in allowed_statuses:

        return jsonify({
            "success": False,
            "message": "Invalid complaint status."
        })

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE hostel_complaints
        SET status = ?
        WHERE id = ?
    """, (
        status,
        complaint_id
    ))

    if cursor.rowcount == 0:

        conn.close()

        return jsonify({
            "success": False,
            "message": "Hostel complaint not found."
        })

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Hostel complaint status updated successfully."
    })


# ==========================================
# HOSTEL - SUBMIT COMPLAINT
# ==========================================

@app.route("/api/hostel-complaints", methods=["POST"])
def create_hostel_complaint():

    data = request.get_json()

    campus_id = data.get("campus_id")
    category = data.get("category")
    description = data.get("description")
    room_no = data.get("room_no")

    if not campus_id or not category or not description or not room_no:

        return jsonify({
            "success": False,
            "message": "Campus ID, category, description and room number are required."
        })

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO hostel_complaints
        (campus_id, category, description, room_no)
        VALUES (?, ?, ?, ?)
    """, (
        campus_id,
        category,
        description,
        room_no
    ))

    complaint_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Hostel complaint submitted successfully.",
        "complaint_id": complaint_id
    })


# ==========================================
# HOSTEL - GET STUDENT COMPLAINTS
# ==========================================

@app.route(
    "/api/hostel-complaints/<campus_id>",
    methods=["GET"]
)
def get_hostel_complaints(campus_id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            category,
            description,
            room_no,
            status,
            created_at
        FROM hostel_complaints
        WHERE campus_id = ?
        ORDER BY id DESC
    """, (campus_id,))

    complaints = cursor.fetchall()

    conn.close()

    return jsonify({
        "success": True,
        "complaints": [dict(row) for row in complaints]
    })


# ==========================================
# CAMPUS NOTICES - GET ALL NOTICES
# ==========================================

@app.route("/api/notices", methods=["GET"])
def get_notices():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            message,
            created_at
        FROM notices
        ORDER BY id DESC
    """)

    notices = cursor.fetchall()

    conn.close()

    return jsonify({
        "success": True,
        "notices": [dict(row) for row in notices]
    })


# ==========================================
# ADMIN - ADD CAMPUS NOTICE
# ==========================================

@app.route("/api/admin/notices", methods=["POST"])
def create_notice():

    data = request.get_json()

    title = data.get("title")
    message = data.get("message")

    if not title or not message:

        return jsonify({
            "success": False,
            "message": "Notice title and message are required."
        })

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notices
        (title, message)
        VALUES (?, ?)
    """, (
        title,
        message
    ))

    notice_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Notice published successfully.",
        "notice_id": notice_id
    })


# ==========================================
# ADMIN - MARK STUDENT ATTENDANCE
# ==========================================

@app.route("/api/admin/attendance", methods=["POST"])
def mark_attendance():

    data = request.get_json()

    campus_id = data.get("campus_id")
    attendance_date = data.get("attendance_date")
    status = data.get("status")

    if not campus_id or not attendance_date or not status:

        return jsonify({
            "success": False,
            "message": "Campus ID, date and attendance status are required."
        })

    if status not in [
        "Present",
        "Absent"
    ]:

        return jsonify({
            "success": False,
            "message": "Invalid attendance status."
        })

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO attendance_records
        (campus_id, attendance_date, status)
        VALUES (?, ?, ?)
    """, (
        campus_id,
        attendance_date,
        status
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Attendance marked successfully."
    })

# ==========================================
# ADMIN - GET ALL STUDENTS
# ==========================================

@app.route("/api/admin/students", methods=["GET"])
def get_all_students():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
       SELECT
    id,
    campus_id,
    name,
    password,
    branch,
    semester,
    attendance
FROM students
        ORDER BY id DESC
    """)

    students = cursor.fetchall()
    conn.close()

    return jsonify({
        "success": True,
        "students": [dict(row) for row in students],
        "total_students": len(students)
    })
# ==========================================
# ADMIN - DELETE STUDENT
# ==========================================

@app.route("/api/admin/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM students
        WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    if not student:
        conn.close()

        return jsonify({
            "success": False,
            "message": "Student not found."
        })

    cursor.execute("""
        DELETE FROM students
        WHERE id = ?
    """, (student_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Student deleted successfully."
    })
# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True
    )