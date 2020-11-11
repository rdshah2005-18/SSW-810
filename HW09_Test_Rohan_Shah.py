import unittest
from typing import List, Dict
from HW09_Rohan_Shah import Student, Instructor,  University


class System_Repo_Test(unittest.TestCase):
    """ Class to test the system """

    def test_fetch_student_records(self) -> None:
        """ Test function to check if student records have been stored correctly """
        SIT: University = University(
            "/Users/rdshah2005/Desktop/SSW810/Assignment9")
        expected_result: List[str] = [['10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']], ['10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']], ['10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567']], ['10175', 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687']], [
            '10183', 'Chapman, O', 'SFEN', ['SSW 689']], ['11399', 'Cordova, I', 'SYEN', ['SSW 540']], ['11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800']], ['11658', 'Kelly, P', 'SYEN', ['SSW 540']], ['11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645']], ['11788', 'Fuller, E', 'SYEN', ['SSW 540']]]
        computed_results: List[str] = list()

        for record in SIT.all_students.values():
            computed_results.append(record.fetch_student_records())

        self.assertEqual(expected_result, computed_results)

    def test_fetch_instructors_records(self) -> None:
        """ Test function to check if instructor records have been stored correctly """
        SIT: University = University(
            "/Users/rdshah2005/Desktop/SSW810/Assignment9")
        expected_result: List[str] = [['98765', 'Einstein, A', 'SFEN'], ['98764', 'Feynman, R', 'SFEN'], [
            '98763', 'Newton, I', 'SFEN'], ['98762', 'Hawking, S', 'SYEN'], ['98761', 'Edison, A', 'SYEN'], ['98760', 'Darwin, C', 'SYEN']]
        computed_results: List[str] = list()

        for record in SIT.all_instructors.values():
            computed_results.append(record.fetch_instructor_records())

        self.assertEqual(expected_result, computed_results)

    def test_fields(self) -> None:
        """ Test function to check if program raises error when no of fields are incorrect """
        file_path: str = "/Users/rdshah2005/Desktop/SSW810/Assignment9/Test_files"
        with self.assertRaises(TypeError):
            University(file_path)

    def test_duplicates(self) -> None:
        """ Test function to check if program raises error when there are duplicate CWIDs """
        file_path: str = "/Users/rdshah2005/Desktop/SSW810/Assignment9/Test_files_2"
        with self.assertRaises(KeyError):
            University(file_path)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
