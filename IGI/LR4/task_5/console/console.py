from console.decorator import *
import pandas


def menu():
    """Menu for continue or not"""
    print()
    print("MENU")
    print("0. Close")
    print("1. Continue")
    print()

@checking(int, 'Not correct input! Choose 0 or 1', condition=lambda x: x in (0,1))
def check_menu():
    "Check input integer 0 or 1"
    return "Enter your choice: "

def choose_matrix():
    """Method for choosing matrix initialization"""

    print()
    print("CHOOSE METHOD FOR INITIALIZATION MATRIX")
    print("1. Random")
    print("2. Array")
    print("3. Pandas")
    print()


@checking(int, 'Not correct input! Choose 1/2/3', condition=lambda x: x in (1,2,3))
def check_choose_matrix():
    "Check input integer 1/2/3"
    return "Enter your choice: "
   



@checking(int, 'Not correct input!', condition=lambda x: x > 0 and x <= 100)
def size_matrix():
    "Check input integer for size"
    return ""

@checking(int, 'Not correct input!', condition=lambda x: x >= -100 and x <= 100)
def range_random():
    "Check input integer for size"
    return ""

def check_start_end(start, end):
    """Method for changing places start and end if anything"""
    if end < start:
        return end, start
    return start, end


def array_matrix_input(n, m):
    """Method for initialization array which will be matrix in future"""
    array_matrix = []
    for r in range(n):
        while True:
            string_m = input(f"Enter {m} elements for {r+1} row: \n")
            string_m = re.sub(r"^\s+|\s+$", "", string_m)

            try:
                row = [int(x) for x in string_m.split()]

                if len(row) != m:
                    raise ValueError
                else:
                    array_matrix.append(row)
                    break
            except ValueError:
                print(f"Not correct input in row {r+1}")
    return array_matrix

def pandas_df():
    """Creation pandas"""
    print("\nCreating a test Pandas DataFrame...")
    df = pandas.DataFrame({
        'Column1': [10, 20, 30, 40, 50],
        'Column2': [5, 4, 3, 2, 1]
    })
    print("Available DataFrame:")
    print(df)

    return df
def colum_pandas():
    """Entering name of colum of pandas"""
    return input("\nEnter column name to extract ('Column1' or 'Column2'): ").strip()
