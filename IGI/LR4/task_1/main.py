from classes.student import *
from my_console.console import *
from functions.func_of_file import *


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
            print(f"Bad bad bad! {e}")
        else:
            output("Student is successfully added!")

    elif choice == 2: 
        if not dictionary:
            output("Dictionary is empty...")
        for s in dictionary.values():
            print(s)
    elif choice == 3:
        pass
    elif choice == 4: 
        if not dictionary:
            output("Dictionary is empty...")
        try:
            saving_format()
            choice = check_saving_format()

            if choice == 1:
                #CSV
                pass
            elif choice == 2:
                #pickel
                pass
        except Exception as e:
            print(f"Bad bad bad! {e}")
        else:
            output("Information is successfully added!")
    elif choice == 5:
        if not dictionary:
            output("Dictionary is empty...") 

    elif choice == 6:
        if not dictionary:
            output("Dictionary is empty...")
        instr = check_instrument()
        list_instr = [x for x in dictionary.values() if x._instrument == instr]
        sorted_list = sorted(list_instr, key = lambda x: x._score)

        for x in sorted_list:
            print(x)
