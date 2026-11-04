PASSING_GRADE = 75
PROGRAM = "Bachelor of Science in Information Technology"

# ------------------------------------------------------------------
# SUBJECTS (BSIT)
# ------------------------------------------------------------------
MAJOR_SUBJECTS = ["ITE 366", "ITE 260"]
MINOR_SUBJECTS = ["NSTP 021", "PED 030", "MAT 152", "GEN 006", "GEN 002", "GEN 001"]
ALL_SUBJECTS = MAJOR_SUBJECTS + MINOR_SUBJECTS


def subject_type(subject):
    return "Major" if subject in MAJOR_SUBJECTS else "Minor"


# ------------------------------------------------------------------
# DATA
# ------------------------------------------------------------------
# Each instructor has their own login and the subjects they handle.
instructors = {
    "instone": {"name": "Instructor One", "password": "1234", "subjects": ["ITE 366", "ITE 260"]},
    "insttwo": {"name": "Instructor Two", "password": "1234", "subjects": ["NSTP 021", "PED 030", "MAT 152"]},
    "instthree": {"name": "Instructor Three", "password": "1234", "subjects": ["GEN 006", "GEN 002", "GEN 001"]},
}

# Class sections (instructors can add more from the menu).
sections = []
        

# student_id -> {"name": str, "password": str, "section": str, "grades": {subject: grade}}
students = {}


# ------------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------------
def remark(grade):
    return "PASSED" if grade >= PASSING_GRADE else "FAILED"


def get_average(grades):
    return sum(grades.values()) / len(grades)


def ask_grade():
    """Keep asking until a valid grade (0-100) is entered."""
    while True:
        try:
            grade = float(input("Enter Grade (0-100): "))
            if 0 <= grade <= 100:
                return grade
            print("Grade must be between 0 and 100.")
        except ValueError:
            print("Please enter a number.")


def choose_subject(title, subjects):
    """Show numbered subject choices and return the selected one (or None to go back)."""
    print(f"\n{title}")
    for i, subject in enumerate(subjects, start=1):
        print(f"{i}. {subject:<10} ({subject_type(subject)})")
    print("0. Back")

    while True:
        choice = input("Enter your choice: ")
        if choice == "0":
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(subjects):
            return subjects[int(choice) - 1]
        print("Invalid choice!")


def print_grade_table(student_id):
    """Table of all BSIT subjects with grade and pass/fail, plus average and overall status."""
    student = students[student_id]
    grades = student["grades"]

    print("\nProgram   :", PROGRAM)
    print("Student ID:", student_id)
    print("Name      :", student["name"])
    print("Section   :", student["section"])
    print("-" * 52)
    print(f"{'SUBJECT':<14}{'TYPE':<10}{'GRADE':>10}{'REMARKS':>16}")
    print("-" * 52)

    for subject in ALL_SUBJECTS:
        if subject in grades:
            grade = grades[subject]
            print(f"{subject:<14}{subject_type(subject):<10}{grade:>10.2f}{remark(grade):>16}")
        else:
            print(f"{subject:<14}{subject_type(subject):<10}{'--':>10}{'NO GRADE YET':>16}")

    print("-" * 52)

    if not grades:
        print("No grades entered yet.")
        return

    average = get_average(grades)
    print(f"{'AVERAGE':<24}{average:>10.2f}{remark(average):>16}")
    print("-" * 52)


# ------------------------------------------------------------------
# LOGIN / REGISTRATION
# ------------------------------------------------------------------
def student_login():
    print("\n--- STUDENT LOGIN (type 0 as Student ID to go back) ---")
    while True:
        student_id = input("Student ID: ")
        if student_id == "0":
            return
        password = input("Password: ")

        if student_id in students and students[student_id]["password"] == password:
            print(f"\nWelcome, {students[student_id]['name']}!")
            student_menu(student_id)
            return
        print("Incorrect Student ID or password! Please try again.\n")


def instructor_login():
    print("\n--- INSTRUCTOR LOGIN (type 0 as Username to go back) ---")
    while True:
        username = input("Instructor Username: ")
        if username == "0":
            return
        password = input("Password: ")

        if username in instructors and instructors[username]["password"] == password:
            print(f"\nWelcome, {instructors[username]['name']}!")
            instructor_menu(username)
            return
        print("Incorrect username or password! Please try again.\n")


def register_instructor():
    while True:
        username = input("Choose a Username (letters only, type 0 to cancel): ").strip()
        if username == "0":
            return
        if not username.isalpha() or not username.isascii():
            print("Username must contain letters only (no numbers, spaces or symbols)!")
        elif username in instructors:
            print("Username already exists!")
        else:
            break

    name = input("Enter Instructor Name: ")
    password = input("Choose a Password: ")

    print("\nAVAILABLE SUBJECTS")
    for i, subject in enumerate(ALL_SUBJECTS, start=1):
        print(f"{i}. {subject:<10} ({subject_type(subject)})")

    raw = input("Enter the numbers of the subjects you handle (separate with commas): ")
    chosen = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit() and 1 <= int(part) <= len(ALL_SUBJECTS):
            subject = ALL_SUBJECTS[int(part) - 1]
            if subject not in chosen:
                chosen.append(subject)

    if not chosen:
        print("You must choose at least one valid subject.")
        return

    instructors[username] = {"name": name, "password": password, "subjects": chosen}
    print("Instructor account created successfully!")
    print("Subjects assigned:", ", ".join(chosen))


# ------------------------------------------------------------------
# INSTRUCTOR FUNCTIONS
# ------------------------------------------------------------------
def change_password(account):
    """Change the password of an account (works for both instructors and students)."""
    current = input("Enter current password: ")
    if current != account["password"]:
        print("Incorrect current password!")
        return

    new_password = input("Enter new password: ")
    if new_password == "":
        print("Password cannot be empty.")
        return
    if new_password == current:
        print("New password must be different from the current password.")
        return

    confirm = input("Confirm new password: ")
    if new_password != confirm:
        print("Passwords do not match!")
        return

    account["password"] = new_password
    print("Password changed successfully!")


def students_in(section):
    """List of (student_id, student) belonging to a section."""
    return [(sid, st) for sid, st in students.items() if st["section"] == section]


def choose_section(title):
    """Show numbered sections and return the selected one (or None to go back)."""
    print(f"\n{title}")
    for i, section in enumerate(sections, start=1):
        count = len(students_in(section))
        print(f"{i}. {section:<12} ({count} student{'s' if count != 1 else ''})")
    print("0. Back")

    while True:
        choice = input("Enter your choice: ")
        if choice == "0":
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(sections):
            return sections[int(choice) - 1]
        print("Invalid choice!")


def add_section():
    name = input("Enter new section name (e.g. BSIT 2A): ").strip().upper()

    if name == "":
        print("Section name cannot be empty.")
        return
    if name in [sec.upper() for sec in sections]:
        print("Section already exists!")
        return

    sections.append(name)
    print(f"Section {name} added successfully!")


def add_student():
    while True:
        student_id = input("Enter Student ID (numbers only, press Enter to cancel): ").strip()
        if student_id == "":
            return
        if not (student_id.isascii() and student_id.isdigit()):
            print("Student ID must contain numbers only!")
        elif student_id in students:
            print("Student ID already exists!")
        else:
            break

    while True:
        name = input("Enter Student Name (letters only, press Enter to cancel): ").strip()
        if name == "":
            return
        if not name.replace(" ", "").isalpha():
            print("Student name must contain letters only (no numbers or symbols)!")
        else:
            break

    password = input("Set a Password for the student: ")

    section = choose_section("SELECT THE STUDENT'S SECTION")
    if section is None:
        print("Student not added (no section selected).")
        return

    students[student_id] = {"name": name, "password": password, "section": section, "grades": {}}
    print(f"Student added successfully! (Program: {PROGRAM} | Section: {section})")


def print_subject_table(subject, section):
    """Table of the students in one section for one subject: ID, name, grade, remarks."""
    print(f"\nSUBJECT: {subject} ({subject_type(subject)})   SECTION: {section}")
    print("-" * 60)
    print(f"{'NO.':<5}{'STUDENT ID':<14}{'NAME':<22}{'GRADE':>8}{'REMARKS':>11}")
    print("-" * 60)

    class_list = students_in(section)
    if not class_list:
        print("No students in this section yet.")
    for i, (student_id, student) in enumerate(class_list, start=1):
        grade = student["grades"].get(subject)
        if grade is None:
            print(f"{i:<5}{student_id:<14}{student['name']:<22}{'--':>8}{'NO GRADE':>11}")
        else:
            print(f"{i:<5}{student_id:<14}{student['name']:<22}{grade:>8.2f}{remark(grade):>11}")
    print("-" * 60)


def enter_grades_for_all(subject, section):
    """Go through every student in the section and enter their grade for the subject."""
    print(f"\nEntering grades for {subject} - {section}.")
    print("Type a grade (0-100) for each student, or just press Enter to skip.")

    for student_id, student in students_in(section):
        current = student["grades"].get(subject)
        shown = "none" if current is None else f"{current:.2f}"

        while True:
            raw = input(f"{student_id} - {student['name']} (current: {shown}): ").strip()
            if raw == "":
                break
            try:
                grade = float(raw)
                if 0 <= grade <= 100:
                    student["grades"][subject] = grade
                    break
                print("Grade must be between 0 and 100.")
            except ValueError:
                print("Please enter a number.")

    print("\nGrades saved successfully!")


def enter_grade_for_one(subject, section):
    """Enter or edit the grade of a single student in the section."""
    student_id = input("Enter Student ID: ")
    if student_id not in students or students[student_id]["section"] != section:
        print(f"Student not found in {section}!")
        return

    print(f"Student: {students[student_id]['name']}  |  Subject: {subject}  |  Section: {section}")
    grade = ask_grade()
    students[student_id]["grades"][subject] = grade

    print("\nGrade saved successfully!")
    print(f"{subject} grade: {grade:.2f} ({remark(grade)})")

    average = get_average(students[student_id]["grades"])
    print(f"Current Average: {average:.2f}")
    print("Overall Status :", remark(average))


def record_grade(username):
    """Choose subject -> choose section -> see the table -> enter grades."""
    my_subjects = instructors[username]["subjects"]

    subject = choose_subject("SELECT SUBJECT", my_subjects)
    if subject is None:
        return

    section = choose_section("SELECT SECTION")
    if section is None:
        return

    while True:
        print_subject_table(subject, section)
        print(f"\n--- {subject} | {section} ---")
        print("1. Enter grades for all students in this section")
        print("2. Enter/edit grade of one student")
        print("0. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            if not students_in(section):
                print("No students in this section yet.")
            else:
                enter_grades_for_all(subject, section)
        elif choice == "2":
            if not students_in(section):
                print("No students in this section yet.")
            else:
                enter_grade_for_one(subject, section)
        elif choice == "0":
            break
        else:
            print("Invalid choice!")


def view_class_table(username):
    """View the grade table of one of the instructor's subjects for a section."""
    my_subjects = instructors[username]["subjects"]

    subject = choose_subject("SELECT SUBJECT TO VIEW", my_subjects)
    if subject is None:
        return

    section = choose_section("SELECT SECTION TO VIEW")
    if section is None:
        return

    print_subject_table(subject, section)


def instructor_menu(username):
    while True:
        print("\n==============================")
        print("      INSTRUCTOR MENU")
        print("==============================")
        print("1. Add Student")
        print("2. Add Section")
        print("3. Enter Grades (choose subject and section)")
        print("4. View Class Grades (by subject and section)")
        print("5. Change Password")
        print("6. Logout")
        print("==============================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            add_section()
        elif choice == "3":
            record_grade(username)
        elif choice == "4":
            view_class_table(username)
        elif choice == "5":
            change_password(instructors[username])
        elif choice == "6":
            print("Logged out.")
            break
        else:
            print("Invalid choice!")


# ------------------------------------------------------------------
# STUDENT FUNCTIONS (view only)
# ------------------------------------------------------------------
def student_menu(student_id):
    while True:
        print("\n==============================")
        print("        STUDENT MENU")
        print("==============================")
        print("1. View My Subjects, Grades and Pass/Fail")
        print("2. Change Password")
        print("3. Logout")
        print("==============================")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\n--- MY GRADES ---")
            print_grade_table(student_id)
        elif choice == "2":
            change_password(students[student_id])
        elif choice == "3":
            print("Logged out.")
            break
        else:
            print("Invalid choice!")


# ------------------------------------------------------------------
# MAIN MENU
# ------------------------------------------------------------------
while True:
    print("\n==============================")
    print("     GRADE MONITORING SYSTEM")
    print("  Bachelor of Science in")
    print("  Information Technology (BSIT)")
    print("==============================")
    print("1. Student Login")
    print("2. Instructor Login")
    print("3. Register as Instructor")
    print("4. Exit")
    print("==============================")

    choice = input("Enter your choice: ")

    if choice == "1":
        student_login()
    elif choice == "2":
        instructor_login()
    elif choice == "3":
        register_instructor()
    elif choice == "4":
        print("Thank you for using the Grade Monitoring System!")
        break
    else:
        print("Invalid choice!")
