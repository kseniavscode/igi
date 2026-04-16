import pickle
import csv
from classes.student import *
def save_csv(data:dict, filename = "students.csv"):

    """
    Metod for saving data students in csv.

    Args: data: a dictionary with all students information, filename: string where we save this information
    """

    with open(filename, 'w', newline='', encoding="UTF-8") as f:
        writen = csv.writer(f)
        writen.writerow(["Name", "Exam Score", "Instrument"])

        for x in data.values():
            writen.writerow([x.name, x.score, x.instrument])

def load_csv(data:dict, filename = "students.csv"):
    """
    Metod for loading data students from csv.

    Args: data: a dictionary with all students information, filename: string where stored information about students
    """

    new_dic = {}
    try:
        with open(filename, 'r', encoding="UTF-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                obj = MusicStudent(name=r["Name"], instrument=r["Instrument"], score= int(r["Exam Score"]))
                new_dic[obj._id] = obj
        data.clear()
        data.update(new_dic)
    except FileNotFoundError:
        print("File not found...")

def save_pickle(data, filename = "students.dat"):
    """
    Metod for saving data students in pickle .dat.

    Args: data: a dictionary with all students information, filename: string where we save this information
    """
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
    print("Data is complitely saved!")

def load_pickle(data:dict, filename = "students.dat"):
    """
    Metod for loading data students from pickle .dat.

    Args: data: a dictionary with all students information, filename: string where stored information about students
    """
    new_dict = {}
    try:
        with open(filename, 'rb') as f:
            new_dict = pickle.load(f)
        data.clear()
        data.update(new_dict)
    except FileNotFoundError:
        print("File not found...")