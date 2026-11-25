"""
Student Record Management System
--------------------------------
A simple menu-driven program to add, view, search, update and delete
student records. Records are saved permanently in a JSON file.
"""

import json
import os

FILE_NAME = "students.json"   # file where all records are stored


# ---------------------------------------------------------------
# FILE HANDLING
# ---------------------------------------------------------------
def load_students():
    """Read records from the JSON file. Return an empty list if the
    file does not exist yet or is damaged."""
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read the data file. Starting with no records.")
        return [] 


def save_students(students):
    """Write the full list of records to the JSON file."""
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)


# ---------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------
def calculate_grade(marks):
    """Return a grade letter for the given marks (out of 100)."""
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    elif marks >= 40:
        return "E"
    else:
        return "F"


def find_by_id(students, student_id):
    """Return the student dictionary with this ID, or None."""
    for student in students:
        if student["id"].lower() == student_id.lower():
            return student
    return None


def get_text(prompt):
    """Keep asking until the user types something non-empty."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  Input cannot be empty. Try again.")


def get_number(prompt, minimum, maximum, as_float=False):
    """Keep asking until the user enters a valid number in range."""
    while True:
        try:
            value = float(input(prompt)) if as_float else int(input(prompt))
            if minimum <= value <= maximum:
                return value
            print(f"  Enter a value between {minimum} and {maximum}.")
        except ValueError:
            print("  Invalid input. Please enter a number.")


def get_contact(prompt):
    """Contact number must be exactly 10 digits."""
    while True:
        value = input(prompt).strip()
        if value.isdigit() and len(value) == 10:
            return value
        print("  Contact number must be exactly 10 digits.")


def get_email(prompt):
    """Very simple email check: must contain '@' and a '.' after it."""
    while True:
        value = input(prompt).strip()
        if "@" in value and "." in value.split("@")[-1]:
            return value
        print("  Enter a valid email address (e.g. name@example.com).")


def get_gender(prompt):
    """Accept only M, F or O."""
    while True:
        value = input(prompt).strip().upper()
        if value in ("M", "F", "O"):
            return value
        print("  Enter M (Male), F (Female) or O (Other).")


def print_table(students):
    """Display a list of students as a formatted table."""
    if not students:
        print("\nNo records to display.")
        return
    header = (f"{'ID':<8}{'Name':<22}{'Age':<5}{'Gen':<5}{'Course':<12}"
              f"{'Sem':<5}{'Contact':<13}{'Email':<26}{'Marks':<8}{'Grade':<6}")
    print("\n" + header)
    print("-" * len(header))
    for s in students:
        print(f"{s['id']:<8}{s['name']:<22}{s['age']:<5}{s['gender']:<5}"
              f"{s['course']:<12}{s['semester']:<5}{s['contact']:<13}"
              f"{s['email']:<26}{s['marks']:<8}{calculate_grade(s['marks']):<6}")


# ---------------------------------------------------------------
# MAIN OPERATIONS
# ---------------------------------------------------------------
def add_student(students):
    """Option 1: take details from the user and store a new record."""
    print("\n--- Add New Student ---")
    student_id = get_text("Student ID: ")
    if find_by_id(students, student_id):      # prevent duplicate IDs
        print("A student with this ID already exists.")
        return

    student = {
        "id": student_id,
        "name": get_text("Full Name: "),
        "age": get_number("Age (15-60): ", 15, 60),
        "gender": get_gender("Gender (M/F/O): "),
        "course": get_text("Course: "),
        "semester": get_number("Semester (1-8): ", 1, 8),
        "contact": get_contact("Contact Number (10 digits): "),
        "email": get_email("Email Address: "),
        "marks": get_number("Marks (0-100): ", 0, 100, as_float=True),
    }
    students.append(student)
    save_students(students)
    print("Student added successfully!")


def view_students(students):
    """Option 2: show all records."""
    print("\n--- All Student Records ---")
    print_table(students)


def search_student(students):
    """Option 3: search by ID (exact) or Name (partial match)."""
    print("\n--- Search Student ---")
    keyword = get_text("Enter Student ID or Name: ").lower()
    results = [s for s in students
               if keyword == s["id"].lower() or keyword in s["name"].lower()]
    if results:
        print(f"{len(results)} record(s) found.")
        print_table(results)
    else:
        print("No matching student found.")


def update_student(students):
    """Option 4: change one or more fields of an existing student."""
    print("\n--- Update Student ---")
    student = find_by_id(students, get_text("Enter Student ID to update: "))
    if student is None:
        print("Student not found.")
        return

    print("Leave a field blank and press Enter to keep the old value.")
    # Name
    new = input(f"Name [{student['name']}]: ").strip()
    if new:
        student["name"] = new
    # Age
    new = input(f"Age [{student['age']}]: ").strip()
    if new:
        try:
            if 15 <= int(new) <= 60:
                student["age"] = int(new)
            else:
                print("  Age out of range. Old value kept.")
        except ValueError:
            print("  Invalid age. Old value kept.")
    # Course
    new = input(f"Course [{student['course']}]: ").strip()
    if new:
        student["course"] = new
    # Semester
    new = input(f"Semester [{student['semester']}]: ").strip()
    if new:
        try:
            if 1 <= int(new) <= 8:
                student["semester"] = int(new)
            else:
                print("  Semester out of range. Old value kept.")
        except ValueError:
            print("  Invalid semester. Old value kept.")
    # Contact
    new = input(f"Contact [{student['contact']}]: ").strip()
    if new:
        if new.isdigit() and len(new) == 10:
            student["contact"] = new
        else:
            print("  Invalid contact number. Old value kept.")
    # Email
    new = input(f"Email [{student['email']}]: ").strip()
    if new:
        if "@" in new and "." in new.split("@")[-1]:
            student["email"] = new
        else:
            print("  Invalid email. Old value kept.")
    # Marks
    new = input(f"Marks [{student['marks']}]: ").strip()
    if new:
        try:
            if 0 <= float(new) <= 100:
                student["marks"] = float(new)
            else:
                print("  Marks out of range. Old value kept.")
        except ValueError:
            print("  Invalid marks. Old value kept.")

    save_students(students)
    print("Student record updated successfully!")


def delete_student(students):
    """Option 5: remove a student after confirmation."""
    print("\n--- Delete Student ---")
    student = find_by_id(students, get_text("Enter Student ID to delete: "))
    if student is None:
        print("Student not found.")
        return
    confirm = input(f"Delete {student['name']}? (y/n): ").strip().lower()
    if confirm == "y":
        students.remove(student)
        save_students(students)
        print("Student deleted successfully!")
    else:
        print("Deletion cancelled.")


def show_grade(students):
    """Option 6: show the grade of one student."""
    print("\n--- Calculate Grade ---")
    student = find_by_id(students, get_text("Enter Student ID: "))
    if student is None:
        print("Student not found.")
        return
    print(f"Name  : {student['name']}")
    print(f"Marks : {student['marks']}")
    print(f"Grade : {calculate_grade(student['marks'])}")


# ---------------------------------------------------------------
# MENU
# ---------------------------------------------------------------
def show_menu():
    print("\n===== STUDENT RECORD MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Calculate Grade")
    print("7. Exit")


def main():
    students = load_students()           # load saved data at start
    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ").strip()
        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            show_grade(students)
        elif choice == "7":
            save_students(students)
            print("Data saved. Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()