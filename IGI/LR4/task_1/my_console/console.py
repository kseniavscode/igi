from my_console.decoration import *

def output(x):
    print(x)

    
def menu():
    """
    Menu for choosing an option
    """
    print("MENU:")
    print("0. Close program")
    print("1. Enter the data")
    print("2. Read the data")
    print("3. Find a student")
    print("4. Sort by music instrument")

@checking(int, "Choose right number of list", lambda x: x >= 0 and x <= 6)
def check_value_of_menu():
    """
    Checking of number of choosing in a menu
    """
    return "Enter a number of choosing"

@checking(str, "Enter right name of student consisting of only letters", lambda x: x.isalpha())
def check_name():
    """
    Checking name of a student
    """
    return "Enter a name of student consisting of only letters"

@checking(str, "Enter a name of instrument consisting of only letters", lambda x: x.isalpha())
def check_instrument():
    """
    Checking a name of instrument
    """
    return "Enter a name of instrument consisting of only letters"

@checking(int, "Not correct inputting an exam score", lambda x: x > 0 and x <= 10)
def check_score():
    """
    Checking of valid entering mark 
    """
    return "Enter an exam score of this student"