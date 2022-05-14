import numpy
import pandas
import psutil

from ..utils.thread_safe_tools import ThreadSafeTools


class GlobalData:

    def __init__(self):
        ThreadSafeTools.print(" [*] Loading global data. Wait!\n")

        self.H = pandas.read_csv('../files/H-1/H-1.csv',
                                 header=None, dtype=float).to_numpy()
        self.minimal_error = numpy.float64('1.0e-4')

        self.load_transversal_matrix = psutil.virtual_memory().free > ThreadSafeTools.convert_gigabytes_to_bytes(1)

        if self.load_transversal_matrix:
            ThreadSafeTools.print(" [X] There is more than 1Gb of free memory," +
                                  " so the transposed H matrix will be cached\n"
                                  )
            self.transpose_h = self.H.transpose()
        else:
            ThreadSafeTools.print(" [X] There is less than 1Gb of free memory," +
                                  " so the transposed H matrix will be calculated at run time\n")

        # The both line below assign same value to c variable, but the first one is more expensive to CPU
        # self.c = numpy.linalg.norm(numpy.matmul(self.get_transpose_h(), self.H), ord=2)
        self.c = numpy.float64('8.418007254936936e-08')

    def get_transpose_h(self) -> numpy.ndarray:
        if self.load_transversal_matrix:
            return self.transpose_h
        else:
            return self.H.transpose()
