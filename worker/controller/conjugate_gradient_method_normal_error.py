from typing import Tuple

import numpy
from pandas import read_pickle

from model.generic_algorithm import GenericAlgorithm
from utils.enums.image_size_options import ImageSizeOptions
from utils.thread_safe_tools import ThreadSafeTools


class ConjugateGradientMethodNormalError(GenericAlgorithm):

    def __init__(self, sinal: numpy.ndarray, image_size: ImageSizeOptions):
        super().__init__(sinal, image_size)

    def generate_image(self) -> Tuple[numpy.ndarray, int]:
        super(ConjugateGradientMethodNormalError, self).generate_image()

        loop_maximum = 50
        loop_counter = 0
        f_next = 0
        error = 0
        best_try_error = 10
        f_old = numpy.zeros((pow(self.image_size, 2),), dtype=numpy.float64)
        best_try = numpy.zeros_like(f_old)
        r_old = numpy.subtract(self.signal_array,
                               numpy.matmul(read_pickle(filepath_or_buffer=self.matriz_h_path).to_numpy(), f_old))
        p_old = numpy.matmul(read_pickle(filepath_or_buffer=self.matriz_ht_path).to_numpy(), r_old)

        for counter in range(loop_maximum):
            loop_counter = counter

            a_i = numpy.divide(
                numpy.matmul(r_old.transpose(), r_old, dtype=float),
                numpy.matmul(p_old.transpose(), p_old)
            )
            f_next = numpy.add(f_old, numpy.multiply(p_old, a_i))
            r_next = numpy.subtract(
                r_old,
                numpy.multiply(
                    numpy.matmul(read_pickle(filepath_or_buffer=self.matriz_h_path).to_numpy(), p_old),
                    a_i
                )
            )
            beta = numpy.divide(
                numpy.matmul(r_next.transpose(), r_next),
                numpy.matmul(r_old.transpose(), r_old)
            )
            p_next = numpy.add(
                numpy.matmul(
                    read_pickle(filepath_or_buffer=self.matriz_ht_path).to_numpy(),
                    r_next
                ),
                numpy.multiply(p_old, beta)
            )
            error = numpy.absolute(numpy.subtract(
                numpy.linalg.norm(r_next, ord=2),
                numpy.linalg.norm(r_old, ord=2)
            ))

            if error < best_try_error:
                best_try = f_next
                best_try_error = error

            p_old = p_next
            f_old = f_next
            r_old = r_next

            if error < self.erro_minimo:
                break

        ThreadSafeTools.print(
            f" [x] Alguns dados sobre a imagem gerada:\n" +
            f"\tNúmero de iterações: {loop_counter}\n" +
            f"\tMenor taxa de erro: {best_try_error}\n" +
            f"\tUltima taxa de erro: {error}\n"
        )

        return f_old, loop_counter
