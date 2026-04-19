from classes.text_analizer import *
from classes.file_result import *
from my_console.console import *

while True:
    filename = check_filename()
    textAnalizer = TextAnalizer(filename)

    result = []
    fileResult = FileResults("result.txt")

    print("Text from file:")
    print(textAnalizer.text)

    smth = f"Count of sentences: {textAnalizer.count_sentences()}"
    print(smth)
    result.append(smth)
    
    smth = f"Count of narrative sentences: {textAnalizer.count_narrative()}"
    print(smth)
    result.append(smth)

    smth = f"Count of questiion sentences: {textAnalizer.count_question()}"
    print(smth)
    result.append(smth)

    smth = f"Count of incentive sentences: {textAnalizer.count_incentive()}"
    print(smth)
    result.append(smth)

    smth = f"Average length of word in sentences: {textAnalizer.average_length_word_sentences()}"
    print(smth)
    result.append(smth)

    smth = f"Count of emoji: {textAnalizer.count_emoji()}"
    print(smth)
    result.append(smth)

    smth = f"Average length of word in text: {textAnalizer.average_length_word_text()}"
    print(smth)
    result.append(smth)
    

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

    result = list(dict.fromkeys(result))
    fileResult.save_into_file("\n".join(result), fileResult.result_filename)
    fileResult.archive(fileResult.result_filename)
    info = fileResult.get_info_zip()

    menu()
    choice = menu_choice()

    if choice == 0:
        break


