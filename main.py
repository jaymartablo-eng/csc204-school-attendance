from typing import Dict, List, Optional, Tuple

import auth
import services
import ui

THEME = ui.DEFAULT_THEME


def bootstrap_admin() -> None:
    if not auth.load_users():
        ui.print_banner("INITIAL ADMIN SETUP", "No user accounts found", THEME)
        while True:
            username = input(ui.style("  Create admin username: ", "accent", THEME)).strip()
            password = input(ui.style("  Create admin password: ", "accent", THEME)).strip()
            ok, msg = auth.create_user(username, password, "admin")
            ui.print_message(msg, "accent" if ok else "error", THEME)
            if ok:
                ui.pause(THEME)
                break


def login_screen() -> Optional[Dict[str, str]]:
    global THEME
    while True:
        ui.clear_screen()
        ui.print_banner("SCHOOL ATTENDANCE SYSTEM", "System Login", THEME)
        username = input(ui.style("  Username: ", "accent", THEME)).strip()
        password = input(ui.style("  Password: ", "accent", THEME)).strip()

        user = auth.authenticate_user(username, password)
        if user:
            ui.print_message(f"Welcome, {user['username']}!", "accent", THEME)
            ui.pause(THEME)
            return user

        ui.print_message("Invalid username or password.", "error", THEME)
        ui.pause(THEME)


def get_record_counts() -> Dict[str, int]:
    return {
        "students": len(services.list_students()),
        "subjects": len(services.list_subjects()),
        "attendance": len(services.list_attendance()),
    }


def handle_add_student() -> None:
    sid = input(ui.style("  Student ID   : ", "accent", THEME))
    name = input(ui.style("  Full Name    : ", "accent", THEME))
    course = input(ui.style("  Course & Year: ", "accent", THEME))
    ok, msg = services.add_student(sid, name, course)
    ui.print_message(msg, "accent" if ok else "error", THEME)


def handle_search_students() -> None:
    query = input(ui.style("  Search ID or Name: ", "accent", THEME))
    results = services.search_students(query)
    rows = [[s["student_id"], s["full_name"], s["course_year"]] for s in results]
    ui.print_table(["Student ID", "Full Name", "Course & Year"], rows, THEME)


def handle_add_subject() -> None:
    code = input(ui.style("  Subject Code  : ", "accent", THEME))
    name = input(ui.style("  Subject Name  : ", "accent", THEME))
    inst = input(ui.style("  Instructor    : ", "accent", THEME))
    ok, msg = services.add_subject(code, name, inst)
    ui.print_message(msg, "accent" if ok else "error", THEME)


def handle_record_attendance() -> None:
    date_str = input(ui.style("  Date (YYYY-MM-DD): ", "accent", THEME))
    code = input(ui.style("  Subject Code     : ", "accent", THEME))
    sid = input(ui.style("  Student ID       : ", "accent", THEME))
    status = input(ui.style("  Status (Present/Absent/Late/Excused): ", "accent", THEME))
    ok, msg = services.record_attendance(date_str, code, sid, status)
    ui.print_message(msg, "accent" if ok else "error", THEME)


def handle_view_attendance() -> None:
    records = services.list_attendance()
    rows = [[r["date"], r["subject_code"], r["student_id"], r["status"]] for r in records]
    ui.print_table(["Date", "Subject", "Student ID", "Status"], rows, THEME)


def handle_reports() -> None:
    ui.print_banner("ATTENDANCE REPORTS", "Student & Subject Summaries", THEME)
    st_rows = [
        [
            str(s["student_id"]),
            str(s["full_name"]),
            str(s["total"]),
            str(s["present"]),
            str(s["late"]),
            str(s["absent"]),
            str(s["excused"]),
            f"{s['rate']}%",
        ]
        for s in services.student_attendance_summary()
    ]
    ui.print_message("Student Summary", "accent", THEME)
    ui.print_table(
        ["ID", "Name", "Total", "Present", "Late", "Absent", "Excused", "Rate"],
        st_rows,
        THEME,
    )

    print()
    sub_rows = [
        [
            str(sub["subject_code"]),
            str(sub["subject_name"]),
            str(sub["total"]),
            str(sub["present"]),
            str(sub["absent"]),
        ]
        for sub in services.subject_attendance_summary()
    ]
    ui.print_message("Subject Summary", "accent", THEME)
    ui.print_table(
        ["Code", "Subject", "Total", "Present", "Absent"],
        sub_rows,
        THEME,
    )


def handle_create_user() -> None:
    username = input(ui.style("  New Username : ", "accent", THEME))
    password = input(ui.style("  New Password : ", "accent", THEME))
    role = input(ui.style("  Role (admin/instructor): ", "accent", THEME))
    ok, msg = auth.create_user(username, password, role)
    ui.print_message(msg, "accent" if ok else "error", THEME)


def handle_settings(user: Dict[str, str]) -> None:
    global THEME
    while True:
        ui.print_dashboard(user, get_record_counts(), THEME)
        ui.print_message("System Settings", "accent", THEME)
        ui.print_menu(
            [
                ("1", "Change Terminal Theme"),
                ("2", "Update Password"),
                ("0", "Back to Main Menu"),
            ],
            THEME,
        )
        choice = input(ui.style("  Select option: ", "accent", THEME)).strip()

        if choice == "1":
            themes = ui.available_themes()
            ui.print_message(f"Available themes: {', '.join(themes)}", "text", THEME)
            selected = input(ui.style("  Enter theme name: ", "accent", THEME)).strip().lower()
            if selected in themes:
                THEME = selected
                ui.print_message(f"Theme switched to '{THEME}'.", "accent", THEME)
            else:
                ui.print_message("Unknown theme name.", "error", THEME)
            ui.pause(THEME)
        elif choice == "2":
            old_pw = input(ui.style("  Current Password: ", "accent", THEME)).strip()
            new_pw = input(ui.style("  New Password    : ", "accent", THEME)).strip()
            ok, msg = auth.update_password(user["username"], old_pw, new_pw)
            ui.print_message(msg, "accent" if ok else "error", THEME)
            ui.pause(THEME)
        elif choice == "0":
            return
        else:
            ui.print_message("Invalid choice.", "error", THEME)
            ui.pause(THEME)


def build_menu(user: Dict[str, str]) -> Tuple[List[Tuple[str, str]], Dict[str, callable]]:
    if auth.is_admin(user):
        options = [
            ("1", "Add Student"),
            ("2", "View / Search Students"),
            ("3", "Add Subject"),
            ("4", "Record Attendance"),
            ("5", "View Attendance Records"),
            ("6", "Reports & Summaries"),
            ("7", "Create User Account"),
            ("8", "System Settings"),
            ("9", "Logout"),
            ("0", "Exit"),
        ]
        actions = {
            "1": handle_add_student,
            "2": handle_search_students,
            "3": handle_add_subject,
            "4": handle_record_attendance,
            "5": handle_view_attendance,
            "6": handle_reports,
            "7": handle_create_user,
            "8": lambda: handle_settings(user),
        }
        return options, actions

    options = [
        ("1", "View / Search Students"),
        ("2", "Record Attendance"),
        ("3", "View Attendance Records"),
        ("4", "Reports & Summaries"),
        ("5", "System Settings"),
        ("6", "Logout"),
        ("0", "Exit"),
    ]
    actions = {
        "1": handle_search_students,
        "2": handle_record_attendance,
        "3": handle_view_attendance,
        "4": handle_reports,
        "5": lambda: handle_settings(user),
    }
    return options, actions


def run() -> None:
    try:
        bootstrap_admin()
        while True:
            user = login_screen()
            if not user:
                continue

            while True:
                ui.print_dashboard(user, get_record_counts(), THEME)
                options, actions = build_menu(user)
                ui.print_menu(options, THEME)
                choice = input(ui.style("  Enter choice: ", "accent", THEME)).strip()

                logout_key = "9" if auth.is_admin(user) else "6"
                if choice == logout_key:
                    break
                if choice == "0":
                    ui.print_message("Goodbye!", "accent", THEME)
                    return
                if choice in actions:
                    actions[choice]()
                    ui.pause(THEME)
                else:
                    ui.print_message("Invalid menu choice.", "error", THEME)
                    ui.pause(THEME)
    except KeyboardInterrupt:
        print("\nExited cleanly.")
    except Exception as exc:
        print(f"\nUnexpected error: {exc}")


if __name__ == "__main__":
    run()