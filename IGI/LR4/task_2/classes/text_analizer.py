import re
from classes.mixins import *

class TextAnalizer():

    def __init__(self, filename):
        """
        Initialiser for reading text from file
        """
        with open(filename, 'r', encoding='UTF-8') as f:
            self.text = f.read()

    @property
    def text(self):
        """ Getter for getting text """
        return self._text
    @text.setter
    def text(self, value):
        """ Setter for setting text """
        self._text = value

    def count_sentences(self):
        """ 
        Find all sentences
        Returns: count of sentences
        """
        return len(re.findall(r"[\.\!\?]+", self.text))
    
    def count_narrative(self):
        """ 
        Find all narratine sentences (., ...)
        Returns: count of narrative sentences
        """
        return len(re.findall(r"[\.]+", self.text))
    def count_question(self):
        """ 
        Find all question sentences (?)
        Returns: count of question sentenses
        """
        return len(re.findall(r"[\?]+", self.text))
    def count_incentive(self):
        """ 
        Find all incentive sentences (!)
        Returns: count of incentive sentences
        """
        return len(re.findall(r"[\!]+", self.text))
    

    def all_words(self):
        """All words in text Returns: list of words"""
        return re.findall(r"\b[A-ZА-ЯЁa-zа-яё]+(?:\-[A-ZА-ЯЁa-zа-яё]+)*\b",self.text)
    

    def average_length_word_sentences(self):
        """
        Average count symbols(only words) in all sentences
        Returns: count
        """
        count_sent = self.count_sentences()

        if count_sent == 0:
            print("Not words in this text")
            return 0
        
        return sum(len(word) for word in self.all_words()) / count_sent

    def average_length_word_text(self):
        """Average length of word in text Returns: count"""

        words = self.all_words()
        count_words = len(words)

        if count_words == 0:
            print("No words in this text")
            return 0
        
        return sum(len(word) for word in words) / count_words

    def count_emoji(self):
        """All emoji in text Returns: count of emoji in text"""
        return len(re.findall(r"[;:](?:\-)*(\(+|\)+|\[+|\]+)", self.text))
    
    def list_words_length_less_five(self):
        """Method for find all words which have length less then 5  Returns: list of words"""
        words = []
        for x in self.all_words():
            if len(x) < 5:
                words.append(x)
        return words
    

    def find_a_specific_line(self, index_line):
        """Method for finding a specific line by index Returns: this line like str"""

        lines = self.text.splitlines()
        if index_line > len(lines) or index_line < 1:
            print("Do not have this index number! Try again :)")
            return None
        return lines[index_line - 1]
    
    def join_replace_line(self, index_line, line):
        """Mothod for joining changed line in your place"""
        lines = self.text.splitlines()
        if index_line > len(lines) or index_line < 1:
            print("Do not have this index number! Try again :)")
            return None
        lines[index_line - 1] = line
        self.text = "\n".join(lines)


    def find_aA(self, line:str):
        """Find two symbols, when lower case and then upper case """
        return re.sub(r"([a-zа-яё][A-ZА-ЯЁ])", r"_?_\1_?_",line)
    
    def output_line(self, line:str):
        """Output chosen line"""
        print(line)

    def count_words_chosen_line_even(self, line:str):
        """Find all words in line which has even"""
        words = re.findall(r"\b[A-Za-zА-ЯЁа-яё]+(?:\-[A-Za-zА-ЯЁа-яё]+)*\b", line)
        print(f"Count of words in chosen line: {len(words)}")
        print("Words where length is even:")
        print(*(x for x in words if len(x) % 2 == 0))


    def find_word_min_len_a(self, line:str):
        """Method for finding word started with a, and have min length of word in this line"""
        words = re.findall(r"\b[aAаА][a-zа-яё]*(?:\-[A-Za-zА-ЯЁа-яё]+)*\b", line)

        if not words:
            print("No words started with 'a' in this line")
            return

        print(f"Word started with 'a' and have min length in this line: {min(words, key=len)}")
        
    def find_duplicates(self, line:str):
        """Find duplicates in line"""

        words = re.findall(r"\b[a-zа-яё]+(?:\-[a-zа-яё]+)*\b", line.lower())

        words_dict = {}
        duplicates = []
        for word in words:
            if word in words_dict:
                words_dict[word] += 1
            else:
                words_dict[word] = 1
        for x, count in words_dict.items():
            if count > 1:
                duplicates.append(x)

        if not duplicates:
            print("No duplicates in this line")
            return
        print("Duplicates in chosen line:")
        print(*(duplicates))
        