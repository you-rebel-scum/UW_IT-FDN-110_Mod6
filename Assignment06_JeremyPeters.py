# -------------------------------------------------------------------------- #
# Title: Assignment05
# Desc: This assignment demonstrates using functions with
# structured error handling
# Change Log: (Who, When, What)
#   Jeremy Peters, 11/12/2024, Initial file creation
#   Jeremy Peters, 11/16/2024, Continuing class & function dev
#   Jeremy Peters, 11/17/2024, Fixes applied to functions and main exec
#   Jeremy Peters, 11/18/2024, Fix spacing and other final touches
# -------------------------------------------------------------------------- #
import os
import json
from colorama import Fore, Style

# Define the Data Constants
FILE_NAME: str = "Enrollments.json"
MENU: str = """
---- Course Registration Program --------
  Select from the following menu:  
    1. Register a Student for a Course
    2. Show current data  
    3. Save data to a file
    4. Exit the program
----------------------------------------- 
"""

# Define the Data Variables
menu_choice: str = str()
students: list = list()

class CustomMessage:
    """
    Class for storing reusable messages
    """
    menu_prompt: str = (Fore.LIGHTYELLOW_EX + f"What would you like to do: " +
         Style.RESET_ALL)
    file_exists: str = (Fore.LIGHTYELLOW_EX + f"File {FILE_NAME} already \
exists. Skipping file creation." + Style.RESET_ALL)
    no_file_create_it: str = (Fore.LIGHTYELLOW_EX + f"No existing file \
{FILE_NAME} found. File will be created." + Style.RESET_ALL)
    prompt_firstname: str = (Fore.LIGHTYELLOW_EX + f"Please enter the \
student's first name: " + Style.RESET_ALL)
    prompt_lastname: str = (Fore.LIGHTYELLOW_EX + f"Please enter the \
student's last name: " + Style.RESET_ALL)
    prompt_coursename: str = (Fore.LIGHTYELLOW_EX + f"Please enter the course\
 name: " + Style.RESET_ALL)
    no_data: str = (Fore.LIGHTCYAN_EX + f"You have not entered any data.\n\
Try starting with starting option 1." + Style.RESET_ALL)
    alpha_only: str = (Fore.LIGHTCYAN_EX + f"Student name should only contain\
 alphabetic characters." + Style.RESET_ALL)
    ascii_only: str = (Fore.LIGHTCYAN_EX + f"Course name should only contain \
ascii characters." + Style.RESET_ALL)
    valid_choices: str = (Fore.LIGHTCYAN_EX + f"Invalid choice. Please try \
again." + Style.RESET_ALL)
    registered_students: str = (Fore.MAGENTA + f"The following students are \
registered:" + Style.RESET_ALL)
    read_file_error: str = (Fore.RED + f"Error reading contents of \
{FILE_NAME}." + Style.RESET_ALL)


class FileProcessor:
    """
    A collection of functions for processing files
    """

    @staticmethod
    def file_check():
        """
        Checks that the file exists and if not, creates an empty file.
        """

        try:
            print(Fore.MAGENTA + f"Checking for existing file {FILE_NAME}..."
                  + Style.RESET_ALL)
            if (not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME)
                    == 0):
                print(CustomMessage.no_file_create_it)
                with open(FILE_NAME, "w") as file:
                    file.write("[]")
            else:
                print(CustomMessage.file_exists)
        finally:
            pass

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        A function to read data from a file

        :param file_name: name of the file
        :param student_data: list of students
        """
        try:
            with open(file_name, "r") as file:
                student_data = json.load(file)
                if isinstance(student_data, list):
                    students.extend(student_data)
        except Exception as e:
            IO.output_error_messages(
                message=CustomMessage.read_file_error, error=e)
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """
        A function to write data to a file

        :param file_name: The name of the file
        :param student_data: The list of students
        """
        try:
            with open(file_name, "w") as file:
                json.dump(student_data, file)
                print(Fore.LIGHTYELLOW_EX + f"The following was saved to \
file:" + Style.RESET_ALL)
                IO.output_student_courses(student_data=students)
                if student_data == str():
                    raise ValueError(CustomMessage.no_data)
        except ValueError as e:
            IO.output_error_messages(e.__str__())
        except Exception as e:
            IO.output_error_messages(e.__str__())

class IO:
    """
    A collection of functions for receiving and storing user data
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        A function that handles error messages

        :param message: message data passed to the function
        :param error: Exception data passed to the function
        """
        print(message)
        if error is not None:
            print(Fore.LIGHTRED_EX + "-- Error Message -- ")
            print(error, error.__doc__, type(error), sep="\n" +
                                                         Style.RESET_ALL)
        elif error == ValueError:
            print(Fore.RED + f"-- Error -- " + Style.RESET_ALL)
            print(Fore.RED + error.__str__() + Style.RESET_ALL)

    @staticmethod
    def output_menu(menu: str):
        """
        A function that presents the menu to the user
        """

        print(Fore.MAGENTA + menu + Style.RESET_ALL)

    @staticmethod
    def input_menu_choice():
        """
        A function that handles the user menu input
        """
        try:
            choice = input(CustomMessage.menu_prompt)
            if choice not in ("1", "2", "3", "4"):
                raise Exception(CustomMessage.valid_choices)
            return choice
        except Exception as e:
            IO.output_error_messages(e.__str__())
            return None

    @staticmethod
    def input_student_data(student_data: list):
        """
        A function that handles the user input

        :param student_data: Stores the students list data
        """

        try:
            while True:
                try:
                    student_first_name = input(CustomMessage.prompt_firstname)
                    if not student_first_name.isalpha():
                        raise ValueError(CustomMessage.alpha_only)
                    student_first_name = student_first_name.title().strip()
                    break
                except ValueError as e:
                    IO.output_error_messages(e.__str__())

            while True:
                try:
                    student_last_name = input(CustomMessage.prompt_lastname)
                    if not student_last_name.isalpha():
                        raise ValueError(CustomMessage.alpha_only)
                    student_last_name = student_last_name.title().strip()
                    break
                except ValueError as e:
                    IO.output_error_messages(e.__str__())

            while True:
                try:
                    course_name = input(CustomMessage.prompt_coursename)
                    if not course_name.isascii():
                        raise ValueError(CustomMessage.ascii_only)
                    course_name = course_name.title().strip()
                    break
                except ValueError as e:
                    IO.output_error_messages(e.__str__())

            student = {"FirstName": student_first_name,
                            "LastName": student_last_name,
                            "CourseName": course_name}
            students.append(student)
            print(Fore.MAGENTA + f"You have added {student_first_name} \
{student_last_name} for course {course_name} to the registration list." \
+ Style.RESET_ALL)
        except Exception as e:
            IO.output_error_messages(message=Fore.RED + f"There was a \
non-specific error!\n" + Style.RESET_ALL, error=e)

    @staticmethod
    def output_student_courses(student_data: list):
        """
        A function that prints the student's courses

        :param student_data: Stores the students list data
        """
        try:
            if not student_data:
                raise ValueError(CustomMessage.no_data)
            for student in students:
                print(Fore.MAGENTA + f"{student['FirstName']}"
                      f" {student['LastName']} is enrolled in "
                      f"{student['CourseName']}" + Style.RESET_ALL)
        except ValueError as e:
            IO.output_error_messages(e.__str__())

# Check if file exists and if not, create empty file
FileProcessor.file_check()

# Load the students variable with data from JSON, if present
FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

while (True):
    # Present menu to user
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":
        IO.input_student_data(students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_courses(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME,
                                         student_data=students)

    # Stop the loop and exit the program
    elif menu_choice == "4":
        print("Program closed successfully")
        exit()
