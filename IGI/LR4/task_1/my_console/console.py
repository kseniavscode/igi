from my_console.decoration import *

def output(x):
    """Just outputting for messagesses"""
    print(x)

    
def menu():
    """
    Menu for choosing an option
    """
    print("MENU:")
    print("0. Close program")
    print("1. Enter the data")
    print("2. List of students")
    print("3. Read the data from file")
    print("4. Save the data into file")
    print("5. Find a student")
    print("6. Sort by music instrument")
    print()

def saving_format():
    """
    Menu for choosing a format for saving
    """
    print("CHOOSE A FORMAT FOR SAVING")
    print("1. CSV")
    print("2. PICKEL")
    print()

@checking(int, "Choose right number of list", lambda x: x >= 0 and x <= 6)
def check_value_of_menu():
    """
    Checking of number of choosing in a menu
    """
    return "Enter a number of choosing "

@checking(int, "You can choose only 1 or 2", lambda x: x == 1 or x == 2)
def check_saving_format():
    """
    Checking entering number of format saving
    """
    return ""


@checking(str, "Enter right name of student consisting of only letters", lambda x: x.isalpha())
def check_name():
    """
    Checking name of a student
    """
    return "Enter a name of student consisting of only letters "

@checking(str, "Enter a name of instrument consisting of only letters", lambda x: x.isalpha())
def check_instrument():
    """
    Checking a name of instrument
    """
    return "Enter a name of instrument consisting of only letters "

@checking(int, "Not correct inputting an exam score", lambda x: x > 0 and x <= 10)
def check_score():
    """
    Checking of valid entering mark 
    """
    return "Enter an exam score of this student "


