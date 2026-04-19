from classes.text_analizer import *
from my_console.console import *
import os

while True:
    filename = check_filename()
    textAnalizer = TextAnalizer(filename)

    result = []
    result_filename = "result.txt"

    print("Text from file:")
    print(textAnalizer.text)

    print(f"Count of sentences: {textAnalizer.count_sentences()}")
    print(f"Count of narrative sentences: {textAnalizer.count_narrative()}")
    print(f"Count of questiion sentences: {textAnalizer.count_question()}")
    print(f"Count of incentive sentences: {textAnalizer.count_incentive()}")
    print(f"Average length of word in sentences: {textAnalizer.average_length_word_sentences()}")
    print(f"Count of emoji: {textAnalizer.count_emoji()}")
    print(f"Average length of word in text: {textAnalizer.average_length_word_text()}")

    result.append(f"Count of sentences: {textAnalizer.count_sentences()}")
    result.append(f"Count of narrative sentences: {textAnalizer.count_narrative()}")
    result.append(f"Count of questiion sentences: {textAnalizer.count_question()}")
    result.append(f"Count of incentive sentences: {textAnalizer.count_incentive()}")
    result.append(f"Average length of word in sentences: {textAnalizer.average_length_word_sentences()}")
    result.append(f"Count of emoji: {textAnalizer.count_emoji()}")
    result.append(f"Average length of word in text: {textAnalizer.average_length_word_text()}")

    while True:
        menu_my()
        choice_my = menu_choice_my()

        if choice_my == 0:
            break
        elif choice_my == 1:
            string = f"List of words, length which is less then 5: {', '.join(textAnalizer.list_words_length_less_five())}"
            print(string)
            result.append(string)

        elif choice_my == 2:
            print(textAnalizer.text)
            count_line = check_count_line()
            chosen_line = textAnalizer.find_a_specific_line(count_line)
            if not chosen_line:
                break
            textAnalizer.output_line(chosen_line)
            chosen_line = textAnalizer.find_aA(chosen_line)
            textAnalizer.join_replace_line(count_line, chosen_line)

            string = f"Change _?_aA_?_:\n"+textAnalizer.text
            print(string)
            result.append(string)
        elif choice_my == 3:
            print(textAnalizer.text)
            count_line = check_count_line()
            chosen_line = textAnalizer.find_a_specific_line(count_line)
            if not chosen_line:
                break
            textAnalizer.output_line(chosen_line)
            count, words = textAnalizer.count_words_chosen_line_even(chosen_line)

            string = f"Count words : {count}, output words length which is % 2 = 0 : {', '.join(words)}"
            print(string)
            result.append(string)
            
        elif choice_my == 4:
            print(textAnalizer.text)
            count_line = check_count_line()
            chosen_line = textAnalizer.find_a_specific_line(count_line)
            if not chosen_line:
                break
            textAnalizer.output_line(chosen_line)

            string = f"Min length of word started with 'a' : {textAnalizer.find_word_min_len_a(chosen_line)}"
            print(string)
            result.append(string)
        elif choice_my == 5:
            print(textAnalizer.text)
            count_line = check_count_line()
            chosen_line = textAnalizer.find_a_specific_line(count_line)
            if not chosen_line:
                break
            textAnalizer.output_line(chosen_line)

            string = f"Duplicates: {', '.join(textAnalizer.find_duplicates(chosen_line))}"
            print(string)
            result.append(string)


