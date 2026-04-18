import re

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
        return re.findall(r"[A-ZА-ЯЁa-zа-яё]+(?:\-[A-ZА-ЯЁa-zа-яё]+)*",self.text)
    

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
        return re.sub(r"([a-zа-яё][A-ZА-ЯЁ])","_?_\1_?_",line)


