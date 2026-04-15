from classes.student import *
from my_console.console import *

dictionary = dict()
while True:
    menu()
    choice = check_value_of_menu()

    if choice == 0:
        break
    elif choice == 1:
        try:
            name = check_name()
            instrument = check_instrument()
            mark = check_score()

            new_student = MusicStudent(name, instrument, mark)

            dictionary[new_student._id] = new_student
        except Exception as e:
            print("Bad bad bad! {e}")
        else:
            output("Student is successfully added!")

    # elif choice == 2: 

    # elif choice == 3: 

    # elif choice == 4: 

