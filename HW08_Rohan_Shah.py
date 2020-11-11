""" Program to work on dates, files and OS operations"""

from typing import Tuple, Iterator, List, IO
from datetime import datetime, date, timedelta
from prettytable import PrettyTable
import os


def date_arithmetic() -> Tuple[datetime, datetime, int]:
    """ This function uses Python's datetime module to answer a few questions"""
    three_days_after_02272020: datetime = datetime.strptime(
        "02/27/2020", "%m/%d/%Y") + timedelta(days=3)
    three_days_after_02272019: datetime = datetime.strptime(
        "02/27/2019", "%m/%d/%Y") + timedelta(days=3)
    days_passed_02012019_09302019: int = (datetime.strptime(
        "09/30/2019", "%m/%d/%Y")-datetime.strptime("02/01/2019", "%m/%d/%Y")).days

    return three_days_after_02272020, three_days_after_02272019, days_passed_02012019_09302019


def file_reader(path, fields, sep=',', header=False) -> Iterator[Tuple[str]]:
    """This function reads field-separated text files and yields a tuple with all of the values from a single line in the file"""
    try:
        file_path: IO = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(
            f"ERROR! The file could not be found at {path}. Please check if the path is correct.")
    else:
        no_of_lines: int = 0
        for each_line in file_path:
            # Split the file into one line each
            row: List[str] = each_line.strip().split(sep)
            # Increment line counter by 1
            no_of_lines += 1

            if len(row) != fields or KeyError is True:
                file_path.close()
                error_msg = f'ERROR! {os.path.basename(file_path)} has {len(row)} fields on line {no_of_lines} but expected {fields}'
                raise ValueError(error_msg)
            else:
                if header == True and no_of_lines == 1:
                    # If header is true, so no of lines has to be 1 atleast
                    continue
                elif header == True and no_of_lines > 1:
                    # If header is true, and there are more lines, yield them
                    yield tuple(row)
                else:
                    yield tuple(row)
    file_path.close()


class FileAnalyzer:
    """ Class that given a directory name, searches that directory for Python files and provides some summary about it"""

    def __init__(self, directory: str) -> None:
        """ Function to initialize all class variables"""
        self.directory: str = directory  # NOT mandatory!
        self.files_summary: Dict[str, Dict[str, int]] = dict()

        self.analyze_files()  # summerize the python files data

    def analyze_files(self) -> None:
        """ Function to analyze and summarize the data"""
        all_files: List[str] = os.listdir(self.directory)

        for file_ in all_files:
            # Check if its a Python file
            if(file_.endswith(".py")):
                try:
                    # Check for file
                    python_file: IO = open(
                        os.path.join(self.directory, file_), 'r')
                except FileNotFoundError:
                    raise FileNotFoundError(
                        f"ERROR! File {file_} not found. Please check your directory once again")
                else:
                    class_count = 0
                    function_count = 0
                    line_count = 0
                    char_count = 0

                    for line in python_file:
                        # Increase line count by 1
                        line_count += 1
                        # Split file into lines
                        lines: List[str] = line.strip().split('\n')
                        # Traverse each line
                        for word in lines:
                            # Increase the character count
                            char_count += len(word)
                            if word.startswith('def'):
                                # Check for functions
                                function_count += 1
                            elif word.startswith('class'):
                                # Check for classes
                                class_count += 1
                python_file.close()

                self.files_summary[file_] = {
                    "classes": class_count, "functions": function_count, "lines": line_count, "characters": char_count}

    def pretty_print(self) -> None:
        """ Function to display the summary in a tabular format """
        table_output = PrettyTable()
        table_output.field_names = ["File Name", "Classes",
                                    "Functions", "Lines", "Characters"]
        for i, j in self.files_summary.items():
            table_output.add_row([i, j["classes"], j["functions"],
                                  j["lines"], j["characters"]])
        return table_output


# x = FileAnalyzer(r"/Users/rdshah2005/Desktop/SSW810/Assn8Test")
# print(x.pretty_print())
