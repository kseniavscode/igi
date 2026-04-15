class Student():

    total_count = 0
    def __init__(self, name):
        self._name = name
        Student.total_count += 1
        self._id = Student.total_count

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

        if not value.strip().isalpha():
            raise ValueError("Not correct entering name of Student") 

        self._name = value.strip().lower().capitalize()

    

class MusicStudent(Student):

    faculty = "Faculty of Music and Education"
    
    def __init__(self, name, instrument, score):
        super().__init__(name)
        self._instrument = instrument
        self._score = score

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

        if not value.strip().isalpha():
            raise ValueError("Not correct entering name of Student") 

        self._instrument = value.strip().lower()


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
            raise TypeError("Not correct entering name of Student, must be integer") 
        if value <= 0 or value > 100 or not isinstance(value, int):
            raise ValueError("Not correct entering name of Student, must be from 0 to 100") 

        self._score = value


        
        