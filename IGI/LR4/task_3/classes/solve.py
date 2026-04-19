import statistics
import matplotlib.pyplot as plot
import math

class Solve():

    def __init__(self, x, n, eps):

        self.x = x
        self.n = n
        self.eps = eps
        self.history = []

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):        
        self._x = value

    @property
    def n(self):
        return self._n
    @n.setter
    def n(self, value):        
        self._n = value
    
    @property
    def eps(self):
        return self._eps
    @eps.setter
    def eps(self, value):        
        self._eps = value


    def sum_F(self, cur_x=None, save_history=False) -> float:

        """
        Calculate the sum of the series ln(x+1).        
        Returns:
            float: calculated sum of the series
        """
        current_x = cur_x if cur_x is not None else self.x
        F = 0
        i = 1
        while True:
            part = (-1)**(i-1) * current_x**(i) / i

            if save_history:
                self.history.append(part)
            F += part
            if abs(part) < self.eps or i == self.n:
                break 
            i += 1
        return F
    

    def get_stat(self):
        """Get statistic information"""
        return [
            f"Mean : {statistics.mean(self.history)}",
            f"Median : {statistics.median(self.history)}",
            f"Mode : {statistics.mode(self.history)}",
            f"Dispirsion/Variance : {statistics.variance(self.history)}",
            f"Standart deviation : {statistics.stdev(self.history)}"
        ]
    
    def get_coord(self):
        """Get coordinates (x,y) (x,y_math) for plot Returns: three list of coordinates: x, y, y_math"""
        x_coord = []
        y_coord = []
        y_coord_math = []
        
        x_value = -0.99
        while x_value <= 0.99:
            x_coord.append(x_value)
            x_value += 0.01
        
        y_coord = [self.sum_F(cur_x=x) for x in x_coord]
        y_coord_math = [math.log(1 + x) for x in x_coord]

        return x_coord, y_coord, y_coord_math
    
    def get_plot(self):

        x_coord, y_coord, y_coord_math = self.get_coord()

        F = self.sum_F()

        plot.figure(figsize=(10,6), dpi=100)
        plot.title("Plot compare",loc='center')
        plot.xlabel("X")
        plot.ylabel("Y")

        plot.plot(x_coord, y_coord_math, color='royalblue', linewidth=2.5, label='math.log(1+x)')
        plot.plot(x_coord, y_coord, color='crimson', linestyle='--', linewidth=2, label=f'Taylor')
        plot.scatter(self.x, F, color='crimson')

        plot.axhline(y=0, color='black', linewidth=1)
        plot.axvline(x=0, color='black', linewidth=1)

        plot.legend(
            loc='upper left', 
            shadow=True,
            prop={
                'size':10,
                'style':'italic'
            },
            facecolor='white'
        )
        plot.text(
            0.15,0.85,f"Information\nn={self.n}\neps={self.eps}",
            transform=plot.gca().transAxes,
            horizontalalignment='right',
            verticalalignment='top',
            bbox=dict(
                boxstyle='round',
                pad=0.3,
                facecolor='white'
            )
        )

        plot.annotate(
            f"Result: {F:.4f}",
            xy=(self.x,F),
            xytext=(self.x+0.2,F-0.4),
            arrowprops=dict(
                facecolor='black',
                shrink=0.05,
                width=2,
                headwidth=8
            ),
            fontsize=10,
            bbox=dict(
                boxstyle='round',
                pad=0.3,
                facecolor='white'
            )
        )

        
        plot.grid(True, linestyle=':',alpha=0.6)

        plot.margins(0.15) 
        plot.tight_layout()

        plot.savefig("plot.png", dpi=300)
        plot.show()





    