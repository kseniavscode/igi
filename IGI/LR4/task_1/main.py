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
        try:
            saving_format()
            choice = check_saving_format()

            if choice == 1:
                load_csv(dictionary)
            elif choice == 2:
                load_pickle(dictionary)
                pass
        except Exception as e:
            print(f"Bad bad bad! {e}")
        else:
            output("Information is successfully added!")
    elif choice == 4: 
        if not dictionary:
            output("Dictionary is empty...")
        try:
            saving_format()
            choice = check_saving_format()

            if choice == 1:
                save_csv(dictionary)
            elif choice == 2:
                save_pickle(dictionary)
        except Exception as e:
            print(f"Bad bad bad! {e}")
        else:
            output("Information is successfully added into file!")
    elif choice == 5:
        if not dictionary:
            output("Dictionary is empty...") 
        name = check_name()
        for d in dictionary.values():
            if d.name == name:
                print(d)

    elif choice == 6:
        if not dictionary:
            output("Dictionary is empty...")
        instr = check_instrument()
        list_instr = [x for x in dictionary.values() if x.instrument == instr]
        sorted_list = sorted(list_instr, key = lambda x: x.score)

        for x in sorted_list:
            print(x)
