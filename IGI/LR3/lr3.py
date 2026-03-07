import math

from functions import sum_F, output_max, sum_list, output_empty_list, input_list, output_sum_list, found_max_in_list, list_with_positive, output_list, count_odd_num_of_letters, split_string, counts_repeated_words, output_repeated_words, input_float_x, input_float_eps, input_int_n, create_table, generate_random_data, menu, menu_input_data, min_in_list, input_list_without_one, output_min, input_string, count_chars_in_low, count_numbers, output_count_lower, output_count_num, output_words_count, shortest_started_i, output_word_with_i, input_size_list

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
    elif choice == '4':
        string = ''' So she was considering in her own mind, as well as she could, for the hot day made her feel 
        very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble 
        of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by 
        her.'''
        my_list = split_string(string)
        odd_words = count_odd_num_of_letters(my_list)
        output_words_count(odd_words)
        word_i = shortest_started_i(my_list)
        output_word_with_i(word_i)
        my_dict = counts_repeated_words(my_list)
        output_repeated_words(my_dict)
    elif choice == '5':
        size = input_size_list()
        my_list = input_list(size)
        output_list(my_list)
        max = found_max_in_list(my_list)
        output_max(max)

        positive_list = list_with_positive(my_list)
        if len(positive_list) == 0:
            output_empty_list()
        else:
            sum = sum_list(positive_list)
            output_sum_list(sum)
        
    else:
        print("Mistake! Not correct input! Choose from 1 to 5")


    







