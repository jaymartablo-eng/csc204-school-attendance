# School Attendance System (CSC 204-A)

A modular, terminal-based School Attendance System built in Python for **CSC 204-A (Programming Languages)**. It supports role-based access control, salted password hashing, structured plain-text persistence, customizable terminal themes, and student/subject attendance reporting.

---

## Features

- **Role-Based Access Control (`admin` & `instructor`)**
  - **Admins** can manage students, subjects, attendance records, reports, user accounts, and system settings.
  - **Instructors** can search students, record and view attendance, generate reports, and manage their own account settings.
- **Authentication & Security**
  - Initial admin bootstrap setup when no accounts exist.
  - Salted **PBKDF2-HMAC-SHA256** password hashing with constant-time digest verification.
  - Self-service password updates inside System Settings.
- **Persistent Text-File Storage**
  - Pipe-delimited (`|`) `.txt` storage for users, students, subjects, and attendance logs without external database dependencies.
- **Reporting & Summaries**
  - **Student Summary:** Total sessions, Present, Late, Absent, Excused counts, and attendance rate (`%`).
  - **Subject Summary:** Per-subject session totals, Present counts, and Absent counts.
- **Customizable Terminal UI**
  - Formatted ASCII tables, dashboard record counters, and switchable color themes (`classic`, `ocean`).

---

## Project Structure

```text
csc204-school-attendance/
├── main.py          # CLI entry point, login flow, role-based menus, and user prompts
├── auth.py          # Password hashing, user loading, authentication, and role checks
├── services.py      # Business logic for students, subjects, attendance, and summaries
├── storage.py       # Pipe-delimited file I/O helpers (load, append, save)
├── ui.py            # Terminal banners, tables, menus, and theme styling
├── data/            # Persistent pipe-delimited .txt data files
└── README.md        # Project documentation