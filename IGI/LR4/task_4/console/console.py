from console.decorator import *
import matplotlib.colors as colors

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

@checking(float, 'Not correct input! Side must be positive', condition=lambda x: x > 0 and x < 100)
def check_side():
    "Check input side of figure"
    return "Enter side of pentagone : "

@checking(str, 'I don`t know this color... Try again', condition=lambda x: colors.is_color_like(x))
def check_color():
    "Check input color"
    return "Enter color of pentagone (eng): "

@checking(str, 'Enter normal title!...', regex=r"[A-Za-z\s\-]+")
def check_title():
    "Check title for figure"
    return 'Enter the title for figure : '


