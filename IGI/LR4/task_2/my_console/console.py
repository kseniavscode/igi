from my_console.decorator import *
import os

def menu():
    print()
    print("MENU:")
    print("0. Close.")
    print("1. Continue")
    print()

def menu_my():
    print()
    print("MENU:")
    print("0. Continue.")
    print("1. List of words, length which is less then 5")
    print("2. Change _?_aA_?_")
    print("3. Count words, output words length which is % 2 = 0")
    print("4. Min length of word started with 'a'")
    print("5. Duplicates")
    print()

@checking(int, "Not correct input! Integer from 0 or 1", condition=lambda x: x in (0,1))
def menu_choice():
    """Method for checking choice (0,1)"""
    return "Input your choice (0,1): " 

@checking(int, "Not correct input! Integer from 0 to 5", condition=lambda x: x >= 0 and x <= 5)
def menu_choice_my():
    """Method for checking choice (0,5)"""
    return "Input your choice (0-5): "    

@checking(str, "Not correct input! Enter the name of file .txt", regEx=r"^\w+\.txt$", condition=lambda x: os.path.exists(x))
def check_filename():
    """Method for checking filename"""
    return "Input name of file: "

@checking(str, "Not correct input! Enter the name of zipfile .zip", regEx=r"^\w+\.zip$")
def check_zipname():
    """Method for checking zipname"""
    return "Input name of zipfile: "

@checking(int, "Not correct input! Integer", condition=lambda x: x > 0)
def check_count_line():
    """Method for checking count of line"""
    return "Choose number of line: " 