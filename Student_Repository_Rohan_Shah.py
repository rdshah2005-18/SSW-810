""" Program to create a system for Universities to track records of their students, instructors and grades """
import os
import sys
from collections import defaultdict
from typing import Dict, List, DefaultDict, Set
from prettytable import PrettyTable
from HW08_Rohan_Shah import file_reader


class Student:
    """ Class to hold details of a student """

    # Hard-coding the column names
    cols: List[str] = ["CWID", "Name", "Major", "Completed Courses"]

    def __init__(self, cwid: str, name: str, major: str):
        """ Initialzing fields of Student """
        self.cwid: str = cwid
        self.name: str = name
        self.major: str = major
        self.courses: Dict[str, str] = dict()

    def fetch_student_records(self) -> List[str]:
        """ Function to fetch student records and sort the courses """
        return [self.cwid, self.name, self.major, sorted(self.courses.keys())]

    def class_taken(self, course_name: str, grade: str) -> None:
        """ Function to assign courses to students """
        self.courses[course_name] = grade


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


class University:
    """ Class to hold details of all students, instructors, and grades for a single Uni """

    def __init__(self, file_path: str) -> None:
        """ Initialing all fields of University """
        self.file_path: str = file_path
        self.all_students: Dict[str, Student] = dict()
        self.all_instructors: Dict[str, Instructor] = dict()
        self.fetch_students()
        self.fetch_instructors()
        self.fetch_grades()
        self.display_students()
        self.display_instructors()

    def fetch_students(self) -> None:
        """ Function to store all student records """
        try:
            for CWID, Name, Major in file_reader(os.path.join(self.file_path, "students.txt"), 3, sep='\t', header=False):
                if CWID in self.all_students:
                    # Check if a record has a CWID getting repeated
                    raise KeyError(
                        f"WARNING! A Student with the CWID {CWID} already exits")
                else:
                    # Else add the student
                    self.all_students[CWID] = Student(CWID, Name, Major)
        except FileNotFoundError:
            raise FileNotFoundError(f"ERROR! File not found")
        except ValueError:
            raise ValueError("ERROR! Some fields may be missing")

    def fetch_instructors(self) -> None:
        """ Function to store all instructor records """
        try:
            for CWID, Name, Dept in file_reader(os.path.join(self.file_path, "instructors.txt"), 3, sep='\t', header=False):
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
            for Student_CWID, Course, Letter_Grade, Instr_CWID in file_reader(os.path.join(self.file_path, "grades.txt"), 4, sep='\t', header=False):
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

    def display_students(self) -> None:
        """ Display student records """

        pretty: PrettyTable = PrettyTable()
        pretty.field_names = Student.cols
        for record in self.all_students.values():
            pretty.add_row(record.fetch_student_records())
        print(pretty)

    def display_instructors(self) -> None:
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


def main():
    SIT: University = University(
        "/Users/rdshah2005/Desktop/SSW810/Assignment9/SSW-810")


main()
