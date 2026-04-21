from console.decorator import *

def menu():
    """Menu"""
    print()
    print("0. Close")
    print("1. Continue")
    print()

@checking(int, "Not correct input!", condition=lambda x: x in (0,1))
def check_menu():
    """Checking menu choice"""
    return "Choose one option: "