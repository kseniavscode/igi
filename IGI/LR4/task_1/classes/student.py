import re
from classes.mixin import *

class Student(ColorOutputMixin):

    total_count = 0
    def __init__(self, name):
        Student.total_count += 1
        self._id = Student.total_count
        self.name = name
        
    @property   
    def name(self):
        """
        Getter of name, when writed obj.name, this method will be done.
        """
        return self._name
    
    @name.setter
    def name(self, value):
        """
        Setter of name, when writed obj.name = value, this method will be done.
        """
        x = re.sub(r"^\s+|\s+$", "", value)
        if not re.fullmatch(r"^[A-ZА-Я][a-zа-яё]{2,}(\-[A-ZА-Я][a-zа-яё]{2,})?$",x):
            raise ValueError("Not correct entering name of Student") 

        self._name = x

    

class MusicStudent(Student):

    faculty = "Faculty of Music and Education"
    
    def __init__(self, name, instrument, score):
        super().__init__(name)
        self.instrument = instrument
        self.score = score
    
    @property
    def instrument(self):
        """
        Getter of instrument, when writed obj.instrument, this method will be done.
        """
        return self._instrument
    
    @instrument.setter
    def instrument(self, value):
        """
        Setter of instrument, when writed obj.instrument = value, this method will be done.
        """
        x = re.sub(r"^\s+|\s+$", "", value)
        if not re.fullmatch(r"^[a-zа-яё]{4,}$",x):
            raise ValueError("Not correct an entering name of instrument") 

        self._instrument = x


    @property
    def score(self):
        """
        Getter of exam score, when writed obj.score, this method will be done.
        """
        return self._score
    
    @score.setter
    def score(self, value):
        """
        Setter of exam score, when writed obj.score = value, this method will be done.
        """
        if type(value) is not int:
            raise TypeError("Not correct entering exam score, must be integer") 
        if value <= 0 or value > 100:
            raise ValueError("Not correct entering exam score, must be from 0 to 100") 

        self._score = value


        
        