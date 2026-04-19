from abc import ABC, abstractmethod
class GeomenricFigure(ABC):
    @abstractmethod
    def get_square(self):
        """Abstract method for calculating square of figure"""
        pass

class GeometricColor():

    def __init__(self, color_name):
        self.color = color_name
    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        self._color = value