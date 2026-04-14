class Student():

    faculty = "Faculty of Music and Education"
    total_count = 0

    def __init__(self, name, instrument, score):
        self.name = name
        self.instrument = instrument
        self.score = score

        Student.total_count += 1

        self.id = Student.total_count