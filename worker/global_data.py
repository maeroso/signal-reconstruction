import sys

import numpy
import pandas
import psutil


class GlobalData:

    def __init__(self):
        sys.stdout.write(" [*] Loading global data. Wait!\n")

        self.H = pandas.read_csv('./../files/H-1/H-1.txt',
                                 header=None, dtype=float).to_numpy()
        self.minimal_error = numpy.float64('1.0e-4')

        self.load_transversal_matrix = psutil.virtual_memory().free > 1000000000

        if self.load_transversal_matrix:
            sys.stdout.write(" [X] There is more than 1Gb of free memory, so the transposed H matrix will be cached\n")
            self.transpose_h = self.H.transpose()
        else:
            sys.stdout.write(" [X] There is less than 1Gb of free memory" +
                             ", so the transposed H matrix will be calculated at run time\n")

        self.c = numpy.linalg.norm(numpy.matmul(self.get_transpose_h(), self.H), ord=2)

    def get_transpose_h(self):
        if self.load_transversal_matrix:
            return self.transpose_h
        else:
            return self.H.transpose()
