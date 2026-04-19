from classes.mixins import *
import re
class FileResults(FileMixin):

    def __init__(self, filename):
        self.result_filename = filename

    @property
    def result_filename(self):
        """Getter for result file"""
        return self._result_filename
    @result_filename.setter
    def result_filename(self, value):
        """Setter for result  file"""
        self._result_filename = value
