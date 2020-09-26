import pandas
import numpy


class GlobalData:

    def __init__(self, load_transversal_matrix):
        print(' [*] Loading global data. Wait!')

        self.H = pandas.read_csv('./../files/H-1/H-1.txt',
                                 header=None, dtype=float).to_numpy()
        self.minimal_error = numpy.float64('1.0e-4')

        self.load_transversal_matrix = load_transversal_matrix

        if load_transversal_matrix:
            self.transversal_h = self.H.transpose()
            self.c = numpy.linalg.norm(numpy.matmul(self.transversal_h, self.H), ord=2)

        else:
            self.c = numpy.linalg.norm(numpy.matmul(self.H.transpose(), self.H), ord=2)

    def get_transversal_h(self):
        if self.load_transversal_matrix:
            return self.transversal_h
        else:
            return self.H.transpose()
