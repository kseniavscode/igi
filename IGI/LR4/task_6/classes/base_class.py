import pandas
import os

class BaseClass():

    def __init__(self, file_path):
        self.file_path = file_path
        self._df = None

    @property
    def file_path(self):
        return self._file_path
    @file_path.setter
    def file_path(self, value):
        if not os.path.exists(value):
            raise FileNotFoundError(f"The file at {value} does not exist.")
        if not value.endswith('.csv'):
            raise ValueError("The file must be a CSV format.")
        self._file_path = value

    @property
    def df(self):
        return self._df
    def load_data(self):
        """Method for loading data from .csv"""

        try:
            self._df = pandas.read_csv(self.file_path, encoding='latin-1')
        except Exception as e:
            print(f"Unexpected error while loading data: {e}")
        else:
            print(f"Successfully loaded data from {self._file_path}")
