from console.console import *
from classes.geometric import *

if __name__ == "__main__":
    while True:

        a = check_side()
        color = check_color()

        pent = Pentagon(a, color)
        print("{:info}".format(pent))
        print("{:short}".format(pent))

        label = check_title()

        pent.draw(label)


        menu()
        choice = check_menu()
        if choice == 0:
            break
