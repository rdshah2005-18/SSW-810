""" Program to create a system for Universities to track records of their students, instructors and grades """
import os
import sys
from collections import defaultdict
from typing import Dict, List, DefaultDict, Set
from prettytable import PrettyTable
from HW08_Rohan_Shah import file_reader
import sqlite3


class Student:
    """ Class to hold details of a student """

    # Hard-coding the column names
    cols: List[str] = ["CWID", "Name", "Major", "Completed Courses",
                       "Remaining Required", "Remaining Elective", "GPA"]

    def __init__(self, cwid: str, name: str, major: str, required: List[str], electives: List[str]) -> None:
        """ Initialzing fields of Student """
        self.cwid: str = cwid
        self.name: str = name
        self.major: str = major
        self.courses: Dict[str, str] = dict()
        self.remaining_req: List[str] = required
        self.remaining_elec: List[str] = electives
        self.grade_map: Dict[str, float] = {"A": 4.0, "A-": 3.75, "B+": 3.25, "B": 3.0,
                                            "B-": 2.75, "C+": 2.25, "C": 2.0, "C-": 0.0, "D+": 0.0, "D": 0.0, "D-": 0.0, "F": 0.0}

    def fetch_student_records(self) -> List[str]:
        """ Function to fetch student records and sort the courses """
        return [self.cwid, self.name, self.major, sorted(self.courses.keys()), sorted(self.remaining_req), sorted(self.remaining_elec), self.calculate_gpa()]

    def class_taken(self, course_name: str, grade: str) -> None:
        """ Function to assign courses to students """
        self.courses[course_name] = grade

    def calculate_gpa(self) -> float:
        """ Function to calculate GPA of the student """
        cumulative_gpa: float = 0.00
        total_sub: int = 0
        for grade in self.courses.values():
            if grade in self.grade_map:
                cumulative_gpa += self.grade_map[grade]
                total_sub += 1
            else:
                print("Invalid Grade")

        gpa: float = cumulative_gpa / total_sub
        return format(gpa, '.2f')


class Instructor:
    """ Class to hold details of an instructor """
    # Hard-coding the column names
    cols: List[str] = ["CWID", "Name", "Dept", "Course", "Students"]

    def __init__(self, cwid: str, name: str, dept: str):
        """ Initialzing fields of Student """
        self.cwid: str = cwid
        self.name: str = name
        self.dept: str = dept
        self.courses_taught: Set = set()
        self.courses_students: DefaultDict[str, int] = defaultdict(int)

    def fetch_instructor_records(self) -> List[str]:
        """ Function to fetch instructor records"""
        return [self.cwid, self.name, self.dept]

    def add_course_and_student(self, course: str) -> None:
        """ Function to add course and student """
        self.courses_taught.add(course)
        self.courses_students[course] += 1


class Major:
    """ Class to hold details about Majors of students """
    cols: List[str] = ["Major", "Required Courses", "Electives"]

    def __init__(self, major: str):
        """ Function to initalize all values """
        self.major = major
        self.req_courses: List[str] = list()
        self.electives: List[str] = list()

    def course_classification(self, course_type: str, course: str) -> None:
        """ Function to classify courses as Electives or Required """
        if course_type == "E":
            self.electives.append(course)
        elif course_type == "R":
            self.req_courses.append(course)
        else:
            print("Invalid Value")
            pass

    def fetch_req_courses(self) -> None:
        """ Function to fetch all required courses """
        return list(self.req_courses)

    def fetch_electives(self) -> None:
        """ Function to fetch all electives """
        return list(self.electives)

    def fetch_major_records(self) -> List[str]:
        """ Function to fetch major records """
        return [self.major, sorted(self.req_courses), sorted(self.electives)]


class University:
    """ Class to hold details of all students, instructors, and grades for a single Uni """

    def __init__(self, file_path: str, db_path: str) -> None:
        """ Initialing all fields of University """
        self.file_path: str = file_path
        self.db_path: str = db_path
        self.all_students: Dict[str, Student] = dict()
        self.all_instructors: Dict[str, Instructor] = dict()
        self.all_majors: Dict[str, Major] = dict()
        self.grade_summary: List[str] = []
        self.fetch_majors()
        self.fetch_students()
        self.fetch_instructors()
        self.fetch_grades()
        self.display_majors()
        self.display_students()
        self.display_instructors()
        self.display_grades(db_path)

    def fetch_majors(self) -> None:
        """ Function to store all majors """
        try:
            for major, course_type, course in file_reader(os.path.join(self.file_path, "majors.txt"), 3, sep='\t', header=True):
                if major not in self.all_majors:
                    self.all_majors[major] = Major(major)
                self.all_majors[major].course_classification(
                    course_type, course)
        except FileNotFoundError:
            print(f"ERROR! File not found at {self.file_path}")

    def fetch_students(self) -> None:
        """ Function to store all student records """
        try:
            for CWID, Name, Major in file_reader(os.path.join(self.file_path, "students.txt"), 3, sep='\t', header=True):
                if CWID in self.all_students:
                    # Check if a record has a CWID getting repeated
                    raise KeyError(
                        f"WARNING! A Student with the CWID {CWID} already exits")
                # Else add the student
                req: List[str] = self.all_majors[Major].fetch_req_courses()
                electives: List[str] = self.all_majors[Major].fetch_electives()
                self.all_students[CWID] = Student(
                    CWID, Name, Major, req, electives)
        except FileNotFoundError:
            raise FileNotFoundError(f"ERROR! File not found")
        except ValueError:
            raise ValueError("ERROR! Some fields may be missing")

    def fetch_instructors(self) -> None:
        """ Function to store all instructor records """
        try:
            for CWID, Name, Dept in file_reader(os.path.join(self.file_path, "instructors.txt"), 3, sep='\t', header=True):
                if CWID in self.all_instructors:
                    # Check if a record has a CWID getting repeated
                    raise KeyError(
                        f"WARNING! An Instructor with the CWID {CWID} already exits")
                else:
                    # Else add the instructor
                    self.all_instructors[CWID] = Instructor(CWID, Name, Dept)
        except FileNotFoundError:
            raise FileNotFoundError(f"ERROR! File not found")
        except ValueError:
            raise ValueError("ERROR! Some fields may be missing")

    def fetch_grades(self) -> None:
        """ Function to store all grade records """
        try:
            for Student_CWID, Course, Letter_Grade, Instr_CWID in file_reader(os.path.join(self.file_path, "grades.txt"), 4, sep='\t', header=True):
                # Check if student exists
                if Student_CWID in self.all_students:
                    add_grade_Student: Student = self.all_students[Student_CWID]
                else:
                    raise KeyError(
                        f"ERROR! No student with the CWID: {Student_CWID}")
                # Check if instructor exists
                if Instr_CWID in self.all_instructors:
                    add_course_Instr: Instructor = self.all_instructors[Instr_CWID]
                else:
                    raise KeyError(
                        f"ERROR! No instructor with the CWID: {Instr_CWID}")

                # Add course and grade to student record
                add_grade_Student.class_taken(Course, Letter_Grade)

                # Add course to instructor record
                add_course_Instr.add_course_and_student(Course)
        except FileNotFoundError:
            raise FileNotFoundError(f"ERROR! File not found")
        except ValueError:
            raise ValueError("ERROR! Some inputs or data may be incorrect ")

    def display_students(self) -> PrettyTable:
        """ Display student records """

        pretty: PrettyTable = PrettyTable()
        pretty.field_names = Student.cols
        for record in self.all_students.values():
            pretty.add_row(record.fetch_student_records())
        print(pretty)

    def display_instructors(self) -> PrettyTable:
        """ Display instructors records """
        pretty: PrettyTable = PrettyTable()
        pretty.field_names = Instructor.cols
        for record in self.all_instructors.values():
            for course in record.courses_taught:
                course_stud: List[str] = [
                    course, record.courses_students[course]]
                instr_record: List[str] = record.fetch_instructor_records()
                instr_record.extend(course_stud)
                pretty.add_row(instr_record)

        print(pretty)
        return pretty

    def display_majors(self) -> PrettyTable:
        """ Display major records """
        pretty: PrettyTable = PrettyTable()
        pretty.field_names = Major.cols
        for majors in self.all_majors.values():
            pretty.add_row(majors.fetch_major_records())

        print(pretty)
        return pretty

    def display_grades(self, db_path) -> PrettyTable:
        """
        Printing the query into a pretty table
        """
        pretty: PrettyTable = PrettyTable()
        pretty.field_names = ["Name", "CWID", "Course", "Grade", "Instructor"]
        try:
            db: sqlite3.Connection = sqlite3.connect(db_path)
        except sqlite3.OperationalError as e:
            print(e)
        else:
            try:
                for row in db.execute("select  s.Name, s.CWID, g.course, g.grade, i.Name as Instructor from students s  join grades g  join instructors i where s.CWID = g.StudentCWID and  g.InstructorCWID = i.CWID order by s.Name"):
                    pretty.add_row(row)
                    self.grade_summary.append(row)
            except sqlite3.Error as e:
                print(e)
        print(pretty)
        return pretty


def main():
    SIT: University = University(
        "/Users/rdshah2005/Desktop/SSW810/Assignment9/SSW-810", "/Users/rdshah2005/Desktop/SSW810/Assignment9/SSW-810/Hw11.db")


main()
