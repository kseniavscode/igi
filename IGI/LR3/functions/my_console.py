from prettytable import PrettyTable
import random

from utilits import decorator
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
def input_int() ->int:

    """
    Checking the input parameter.
    
    Returns:
        int: value
    """

    while True:
        try:
            x = int(input("Input int number, if you wanna stop loop, enter number 1: "))
            return x
        except ValueError:
            print("Input int value!")

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
        print("2. Find a min element in our inputing list")
        print("3. Find count of all elements of string(inputting) in low and all number")
        print("4. Have a text, find words with an odd number of letters, find the shortest word starting with i, output repeated words")
        print("5. Enter size and list of float elem, found max, found sum of only positive part of elements of list")
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

def input_list_without_one():

    """
    Input loop for list, when we input 1, loop will be stopped
    
    Returns:
        list: elements without 1
    """

    my_list = []
    while True:
        x = input_int()
        if x == 1:
            return my_list
        my_list.append(x)




@decorator
def output_min(x, values: list):
    """
    Output information about a min element in list
    
    Args: 
        x(int): min
        values(list): list of elements
    """
    print(f"Min elements in list {values} is {x}" )

def input_string():
    """
    Input not empty string
    
    Returns: str x: string
    """
    while True:
        x = input("Input string: ")
        if x:
            return x
        print("Our string does not have to be empty...") 
def output_count_lower(x):
    """
    Output information about count of chars in lower case
    
    Args: 
        x(int): count
    """
    print(f"Count of chars in lower case is {x}" )

def output_count_num(x):
    """
    Output information about count of chars which are digits
    
    Args: 
        x(int): count
    """
    print(f"Count of chars which are digits is {x}" )

def output_words_count(l:list):

    """
    Output information about count of words with an odd number of letters and words
    
    Args: 
        x(int): count
        list: words with an odd number of letters
    """

    print("All of words in this text with an odd number of letters")
    for i in l[:-1]:
        print(i)
    print(f"Count of words is {l[-1]}")

def output_word_with_i(x):
    """
    Output information about a word started with i
    
    Args: 
        x(str): n, if not found, a word, if found
    """
    if x == 'n':
        print(f"Not found a word started with i...")
    else:
        print(f"Found the shortest word started with i: {x}")

def output_repeated_words(d:dict):

    """
    Output dictionary with repeated words and their counts
    
    Args: 
        d(dict): dictionary where key = word
    """

    print('')
    print("Repeated words and their counts in text:")
    found = False
    for word, count in d.items():
        if count > 1:
            print(f"{word} :: {count}")
            found = True
    if not found:
        print("In this text not found repeated words at all")

def input_size_list() ->int:

    """
    Input size of future list
    
    Returns: int x: size > 0
    """

    while True:
        try:
            x = int(input("Enter the size of future list: "))
            if x > 0:
                return x
        except ValueError:
            print("Size of list MUST be positive int number")

def input_list(size:int) ->list:

    """
    Input not empty string
    
    Args: size(int): size of list

    Returns: list l: list of float numbers
    """

    l = []
    while size != 0:
        try:
           x = float(input("Enter the float element for list: ")) 
           l.append(x)
           size -= 1
        except ValueError:
            print("List contains only float number without restrictions")
    return l

def input_list_generation(size:int):

    """
    Generator Expression for list of elements counts which is size
    
    Args: size(int): size of list

    Returns: list l: list of float numbers
    """

    return [round(random.uniform(-50, 500), 2) for _ in range(size)]

def output_list(l:list):

    """
    Output list
    
    Args: l(list): list
    """

    print(f"List of inputting elements: {l}")

def output_max(max:float):

    """
    Output max abs element of list
    
    Args: 
        max(float): element of list
    """

    print(f"Max abs element of list: |{max}|")

def output_sum_list(sum:float):

    """
    Output sum element of list
    
    Args: 
        sum(float): sum element of list
    """

    print(f"Sum of positive elements: {sum}")

def output_empty_list():

    """
    Output that list is empty
    """

    print(f"Sorry, but list is turned out empty...")