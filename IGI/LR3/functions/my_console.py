from prettytable import PrettyTable
import random
def input_float_x() ->float:

    """
    Checking the input parameter x.
    Must be in range from -1 to 1
    
    Returns:
        float: value of x
    """

    while True:
        try:
            x = float(input("Input float x (-1; 1): "))
            if x > -1 and x < 1:
                break
        except ValueError:
            print("Not correct inputting!")
    print("")
    return x
def input_float_eps() ->float:

    """
    Checking the input parameter eps.
    Must be positive
    
    Returns:
        float: value of eps
    """

    while True:
        try:
            x = float(input("Input positive float eps: "))
            if x >= 0:
                break
        except ValueError:
            print("Not correct inputting!")
    print("")
    return x

def input_int_n() ->int:

    """
    Checking the input parameter n.
    Must be in range from 1 to 500
    
    Returns:
        int: value of n
    """

    while True:
        try:
            x = int(input("Input number of iterations (1, 500): "))
            if (x > 0 and x <= 500) :
                break
        except ValueError:
            print("Input int value from 1 to 500")
    print("")
    return x
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

    x = round(random.uniform(-0.99, 0.99), 3)
    n = random.randint(1, 500)
    eps = random.choice([0.1, 0.01, 0.001, 0.0001, 0.00001])
    return x, n, eps

def menu():

    """
    Menu for choosing an action by tasks
    
    Returns:
        char: value of choice
    """
    while True:
        print("==== MENU ====")
        print("Choose one of the options:")
        print("0. Exit.")
        print("1. Calculate a value of ln(x+1)")
        print("2.")
        print("3.")
        print("4.")
        print("5.")
        return input("Your choice (1-5): ")
        
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

