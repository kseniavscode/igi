import math

from functions import sum_F, input_float_x, input_float_eps, input_int_n, create_table, generate_random_data, menu, menu_input_data, min_in_list, input_list_without_one, output_min, input_string, count_chars_in_low, count_numbers, output_count_lower, output_count_num

'''
LAB 3
YAROSHEVICH KSENIA, group 453504
started 06.03.2026 8:13
python 3.14.3

task 1
need to calculate the sum of the series ln(x+1)
'''

while True:
    choice = menu()
    if choice == '0':
        print("GOOOD BYYYEEEEE!")
        break
    elif choice == '1':
        ch_data = menu_input_data()
        while ch_data != '1' and ch_data != '2':
            print("Mistake! Not correct input! Choose 1 or 2")
            ch_data = menu_input_data()
        if ch_data == '1':
            x = input_float_x()
            n = input_int_n()
            eps = input_float_eps()
        elif ch_data == '2':
            x, n, eps = generate_random_data()
        
        F = sum_F(x, n, eps)
        F_math = math.log(x + 1)
        create_table(["x", "n", "F(x)", "Math", "eps"], [x, n, F, F_math, eps])
    elif choice == '2':
        my_list = input_list_without_one()
        min = min_in_list(my_list)
        output_min(min, my_list)
    elif choice == '3':
        string = input_string()
        count_low = count_chars_in_low(string)
        output_count_lower(count_low)
        count_n = count_numbers(string)
        output_count_num(count_n)
    # elif choice == '4':
    # elif choice == '5':
    else:
        print("Mistake! Not correct input! Choose from 1 to 5")


    







