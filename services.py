from typing import Dict, List, Tuple

from storage import append_record, load_records, save_records

STUDENTS_FILE = "data/students.txt"
SUBJECTS_FILE = "data/subjects.txt"
ATTENDANCE_FILE = "data/attendance.txt"
VALID_STATUSES = {"Present", "Absent", "Late", "Excused"}


def _parse_rows(filepath: str, expected_cols: int) -> List[List[str]]:
    rows: List[List[str]] = []
    try:
        raw_lines = load_records(filepath)
    except Exception:
        return rows

    for line in raw_lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) == expected_cols and all(parts):
            rows.append(parts)
    return rows


def list_students() -> List[Dict[str, str]]:
    return [
        {"student_id": sid, "full_name": name, "course_year": cy}
        for sid, name, cy in _parse_rows(STUDENTS_FILE, 3)
    ]


def add_student(student_id: str, full_name: str, course_year: str) -> Tuple[bool, str]:
    student_id = student_id.strip()
    full_name = full_name.strip()
    course_year = course_year.strip()

    if not all([student_id, full_name, course_year]):
        return False, "All student fields are required."

    if any(s["student_id"].lower() == student_id.lower() for s in list_students()):
        return False, f"Student ID '{student_id}' already exists."

    append_record(STUDENTS_FILE, f"{student_id} | {full_name} | {course_year}")
    return True, f"Student '{full_name}' added."


def search_students(query: str) -> List[Dict[str, str]]:
    q = query.strip().lower()
    if not q:
        return list_students()
    return [
        s
        for s in list_students()
        if q in s["student_id"].lower() or q in s["full_name"].lower()
    ]


def list_subjects() -> List[Dict[str, str]]:
    return [
        {"subject_code": code, "subject_name": name, "instructor": inst}
        for code, name, inst in _parse_rows(SUBJECTS_FILE, 3)
    ]


def add_subject(subject_code: str, subject_name: str, instructor: str) -> Tuple[bool, str]:
    subject_code = subject_code.strip().upper()
    subject_name = subject_name.strip()
    instructor = instructor.strip()

    if not all([subject_code, subject_name, instructor]):
        return False, "All subject fields are required."

    if any(sub["subject_code"] == subject_code for sub in list_subjects()):
        return False, f"Subject '{subject_code}' already exists."

    append_record(SUBJECTS_FILE, f"{subject_code} | {subject_name} | {instructor}")
    return True, f"Subject '{subject_code}' added."


def list_attendance() -> List[Dict[str, str]]:
    return [
        {
            "date": dt,
            "subject_code": code,
            "student_id": sid,
            "status": status,
        }
        for dt, code, sid, status in _parse_rows(ATTENDANCE_FILE, 4)
    ]


def record_attendance(
    date_str: str, subject_code: str, student_id: str, status: str
) -> Tuple[bool, str]:
    date_str = date_str.strip()
    subject_code = subject_code.strip().upper()
    student_id = student_id.strip()
    status = status.strip().capitalize()

    if not all([date_str, subject_code, student_id, status]):
        return False, "All attendance fields are required."
    if status not in VALID_STATUSES:
        return False, f"Status must be one of: {', '.join(sorted(VALID_STATUSES))}."

    if not any(s["student_id"] == student_id for s in list_students()):
        return False, f"Student ID '{student_id}' not found."
    if not any(sub["subject_code"] == subject_code for sub in list_subjects()):
        return False, f"Subject '{subject_code}' not found."

    records = list_attendance()
    updated = False
    new_lines: List[str] = []

    for rec in records:
        if (
            rec["date"] == date_str
            and rec["subject_code"] == subject_code
            and rec["student_id"] == student_id
        ):
            new_lines.append(f"{date_str} | {subject_code} | {student_id} | {status}")
            updated = True
        else:
            new_lines.append(
                f"{rec['date']} | {rec['subject_code']} | {rec['student_id']} | {rec['status']}"
            )

    if updated:
        save_records(ATTENDANCE_FILE, new_lines)
        return True, "Existing attendance record updated."

    append_record(ATTENDANCE_FILE, f"{date_str} | {subject_code} | {student_id} | {status}")
    return True, "Attendance recorded."


def student_attendance_summary() -> List[Dict[str, object]]:
    students = list_students()
    records = list_attendance()
    summary: List[Dict[str, object]] = []

    for st in students:
        sid = st["student_id"]
        st_recs = [r for r in records if r["student_id"] == sid]
        total = len(st_recs)
        present = sum(1 for r in st_recs if r["status"] == "Present")
        late = sum(1 for r in st_recs if r["status"] == "Late")
        absent = sum(1 for r in st_recs if r["status"] == "Absent")
        excused = sum(1 for r in st_recs if r["status"] == "Excused")
        rate = round((present / total) * 100, 1) if total > 0 else 0.0

        summary.append(
            {
                "student_id": sid,
                "full_name": st["full_name"],
                "total": total,
                "present": present,
                "late": late,
                "absent": absent,
                "excused": excused,
                "rate": rate,
            }
        )
    return summary


def subject_attendance_summary() -> List[Dict[str, object]]:
    subjects = list_subjects()
    records = list_attendance()
    summary: List[Dict[str, object]] = []

    for sub in subjects:
        code = sub["subject_code"]
        sub_recs = [r for r in records if r["subject_code"] == code]
        summary.append(
            {
                "subject_code": code,
                "subject_name": sub["subject_name"],
                "total": len(sub_recs),
                "present": sum(1 for r in sub_recs if r["status"] == "Present"),
                "absent": sum(1 for r in sub_recs if r["status"] == "Absent"),
            }
        )
    return summary