from prettytable import PrettyTable
import random
from myconsole.decorator import *

def menu():
    """Menu"""
    print()
    print("0. Close")
    print("1. Continue")
    print()

@valid_input(int, "Not correct input!", lambda x: x in (0,1))
def check_menu():
    """Checking menu choice"""
    return "Choose one option: "
def menu_input_data():

    """
    Menu for choosing variant of getting data
    
    Returns:
        char: value of choice
    """

    print("==== MENU OF INPUTTING DATA ====")
    print("Choose one of the options:")
    print("1. Keyboard input")
    print("2. Random data")
    return input("Your choice 1 or 2: ")

#TASK 1
@valid_input(float, "Not correct inputting!", lambda x: x > -1 and x < 1)
def input_float_x() ->str:

    """
    Checking the input parameter x.
    Must be in range from -1 to 1
    
    Returns:
        float: value of x
    """
    return "Input float x (-1; 1): "

@valid_input(float, "Not correct inputting!", lambda x: x >= 0)
def input_float_eps() ->str:

    """
    Checking the input parameter eps.
    Must be positive
    
    Returns:
        float: value of eps
    """
    return "Input positive float eps: "

@valid_input(int, "Input int value from 1 to 500", lambda x: x > 0 and x <= 500)
def input_int_n() ->str:

    """
    Checking the input parameter n.
    Must be in range from 1 to 500
    
    Returns:
        int: value of n
    """
    return "Input number of iterations (1, 500): "

@valid_input(int, "Input int value!", lambda x: x > 0 and x <= 500)
def input_int() ->int:

    """
    Checking the input parameter.
    
    Returns:
        int: value
    """
    return "Input int number, if you wanna stop loop, enter number 1: "

def create_table(col_names: list, values: list):
    
    """
    Create table using PrettyTable
    
    Args: list of names of colums and list of values for the next row
    """

    table = PrettyTable()
    table.field_names = col_names
    table.add_row(values)
    print(table)

def generate_random_data():
    
    """
    Generate random data for variables: x, n, eps
    
    Returns:
        float x: argument in range (-1, 1)
        int n: argument in range [1, 500]
        float eps: argument in range [0.1, 0.01, 0.001, 0.0001, 0.00001]
    """

    yield round(random.uniform(-0.99, 0.99), 3)
    yield random.randint(1, 500)
    yield random.choice([0.001, 0.0001, 0.00001])
