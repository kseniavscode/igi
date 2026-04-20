from abc import ABC, abstractmethod
import math

import matplotlib.pyplot as plot 
import matplotlib.patches as patches


class GeometricFigure(ABC):
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


class Pentagon(GeometricFigure):

    name_figure = "Regular pentagon"

    def __init__(self, a, color_name):
        self.side = a
        
        self.color_obj = GeometricColor(color_name)

    @property
    def side(self):
        return self._side
    @side.setter
    def side(self, value):
        self._side = value

    def __format__(self, format_spec):
        BLUE = '\033[94m'
        RESET = '\033[0m'
        if format_spec == 'info':
            return "{3} : color is {0}, side is {1}, square is {blue}{2:.2f}{reset}".format(self.color_obj.color, self.side, self.get_square(), self.get_name_figure(), blue=BLUE, reset=RESET)
        if format_spec == 'short':
            return "Pentagone (a = {})".format(self.side)
    
    @classmethod
    def get_name_figure(cls):
        """Get name of figure"""
        return cls.name_figure
    
    def get_square(self):
        """Override abstract method about getting square"""
        return (5 * self.side**2) / (4 * math.tan(math.pi / 5))
    
    def draw(self, label):
        """Method for painting pentagone, and with label"""

        r = self.side / (2 * math.sin(math.pi / 5))
        figure, axes = plot.subplots()

        pentagone = patches.RegularPolygon(
            (0.5, 0.5), 5, radius=r,  
            facecolor=self.color_obj.color,
            edgecolor='black'
        )
        axes.add_patch(pentagone)

        margin = r * 1.1
        axes.set_xlim(0.5 - margin, 0.5 + margin)
        axes.set_ylim(0.5 - margin, 0.5 + margin)

        axes.text(
            0.5,0.5,label,
            ha='center',
            va='center',
            fontsize=12,
            color= 'white' if self.color_obj.color != 'white' else 'black',
            fontweight='bold'
        )
        axes.set_aspect('equal')

        plot.title(self.get_name_figure())
        plot.savefig("result.png")
        plot.show()

        