import numpy 
import pandas

class Matrix():

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.matrix=None

    @property
    def n(self):
        return self._n 
    @n.setter
    def n(self, n):
        if n < 0:
            raise ValueError("n must be positive...")
        self._n=n
    @property
    def m(self):
        return self._m 
    @m.setter
    def m(self, m):
        if m < 0:
            raise ValueError("m must be positive...")
        self._m=m

    def create(self):
        """Method for heirs"""
        pass


    def slicing(self):
        """Demonstration of slicing matrix"""

        print(f"First element: {self.matrix[0,0]}")
        print(f"First row: {self.matrix[0,:]}")
        print(f"First colum: {self.matrix[:,0]}")
        print(f"Slice matrix (0-{self.n-1})(0-{self.m-1}) : {self.matrix[0:self.n-1,0:self.m-1]}")

    def universal(self):
        """Demonstrayion of funcs of numpy"""

        print(f"Plus every element 10: \n{self.matrix + 10}")
        print(f"Multiplication every element on (-5): \n{self.matrix * (-5)}")

        print(f"Minus first row 4:")
        temp_matrix = self.matrix.copy()
        temp_matrix[0, :] = temp_matrix[0,:] - 4
        print(temp_matrix)
    
        print(f"Sin for first colum on:")
        temp_matrix = self.matrix.copy()
        temp_matrix[:,0] = numpy.sin(temp_matrix[:,0])
        print(temp_matrix)
        

        if self.matrix.shape[0] >= 2:
            print(f"Plus first and second row:")
            temp_matrix = self.matrix.copy()
            temp_matrix[0, :] = temp_matrix[0, :] + temp_matrix[1, :]
            print(temp_matrix)

    def create_new_matrix(self):
        """Create new matrix by division max abs"""

        max_abs = numpy.max(numpy.abs(self.matrix))
        if max_abs != 0:
            self.matrix = self.matrix / max_abs
        else:
            print("Matrix is the same, because max element = 0")

    def variance_numpy(self):
        """Variance by numpy"""
        return f'{numpy.var(self.matrix):.2f}'
    
    def variance(self):
        """Manual calculation of variance"""
        return (numpy.sum(self.matrix ** 2) / self.matrix.size) - (numpy.sum(self.matrix) / self.matrix.size)**2
    
    def get_stat(self):
        """Method for static information"""
        return [
            f"mean: {numpy.mean(self.matrix)}",
            f"median: {numpy.median(self.matrix)}",
            f"std: {numpy.std(self.matrix)}",
            f"var: {numpy.var(self.matrix)}",
            f"corr: \n{numpy.corrcoef(self.matrix)}"
        ]

class RandomMatrix(Matrix):
    def __init__(self, n, m, start=-100, end=100):
        super().__init__(n, m)
        self.start=start
        self.end=end
        self.matrix=self.create()

    def create(self):
        """Method for creating matrix by sizies"""
        return numpy.random.randint(self.start, self.end+1, size=(self.n, self.m))

class ArrayMatrix(Matrix):
    def __init__(self, n, m, list_ar):
        super().__init__(n, m)
        self.list_ar=list_ar
        self.matrix=self.create()

    def create(self):
        '''Method for creation matrix based on list'''
        return numpy.array(self.list_ar)

class PandasMatrix(Matrix):

    def __init__(self, df, value):
        data=df[value].values

        if data.ndim == 1:
            data=data.reshape(-1,1)
        n,m=data.shape

        super().__init__(n, m)
        self.matrix=data
    
    
        