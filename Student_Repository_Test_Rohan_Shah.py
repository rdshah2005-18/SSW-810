import unittest
from typing import List, Dict
from Student_Repository_Rohan_Shah import Student, Instructor,  University, Major


class System_Repo_Test(unittest.TestCase):
    """ Class to test the system """

    def test_fetch_student_records(self) -> None:
        """ Test function to check if student records have been stored correctly """
        SIT: University = University(
            "/Users/rdshah2005/Desktop/SSW810/Assignment9/SSW-810")
        expected_result: List[str] = [['10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545'], '3.44'], [
            '10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545'], '3.81']]
        computed_results: List[str] = list()

        count: int = 2
        for record in SIT.all_students.values():
            if count > 0:
                computed_results.append(record.fetch_student_records())
                count = count - 1

        self.assertEqual(expected_result, computed_results)

    def test_fetch_instructors_records(self) -> None:
        """ Test function to check if instructor records have been stored correctly """
        SIT: University = University(
            "/Users/rdshah2005/Desktop/SSW810/Assignment9/SSW-810")
        expected_result: List[str] = [['98765', 'Einstein, A', 'SFEN'], ['98764', 'Feynman, R', 'SFEN'], [
            '98763', 'Newton, I', 'SFEN'], ['98762', 'Hawking, S', 'SYEN'], ['98761', 'Edison, A', 'SYEN'], ['98760', 'Darwin, C', 'SYEN']]
        computed_results: List[str] = list()

        for record in SIT.all_instructors.values():
            computed_results.append(record.fetch_instructor_records())

        self.assertEqual(expected_result, computed_results)

    def test_fetch_majors_records(self) -> None:
        """ Test function to check if major records have been stored correctly """
        SIT: University = University(
            "/Users/rdshah2005/Desktop/SSW810/Assignment9/SSW-810/")
        expected_result: List[str] = [['SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']], [
            'SYEN', ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810']]]
        computed_results: List[str] = list()

        for record in SIT.all_majors.values():
            computed_results.append(record.fetch_major_records())

        self.assertEqual(expected_result, computed_results)

    def test_fields(self) -> None:
        """ Test function to check if program raises error when no of fields are incorrect """
        file_path: str = "/Users/rdshah2005/Desktop/SSW810/Assignment9/SSW-810/Test_files"
        with self.assertRaises(KeyError):
            University(file_path)

    def test_duplicates(self) -> None:
        """ Test function to check if program raises error when there are duplicate CWIDs """
        file_path: str = "/Users/rdshah2005/Desktop/SSW810/Assignment9/SSW-810/Test_files_2"
        with self.assertRaises(KeyError):
            University(file_path)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
