import os
import uuid

import cv2
import numpy
from PIL import Image
from pandas import read_pickle

from model.generic_algorithm import GenericAlgorithm
from utils.enums.algorithms import Algorithms
from utils.enums.image_size_options import ImageSizeOptions
from utils.thread_safe_tools import ThreadSafeTools


class ConjugateGradientMethodNormalError(GenericAlgorithm):

    def __init__(self, sinal: numpy.ndarray, image_size: ImageSizeOptions):
        super().__init__(sinal, image_size)

    @staticmethod
    def factory_method(signal: numpy.ndarray, image_size: ImageSizeOptions,
                       algorithm: Algorithms.CONJUGATE_GRADIENT_METHOD_NORMAL_ERROR) -> GenericAlgorithm:
        return ConjugateGradientMethodNormalError(signal, image_size)

    def generate_image(self) -> Image:
        loop_maximum = 100
        loop_counter = 0
        f_next = 0
        error = 0
        best_try_error = 10
        f_old = numpy.zeros((pow(self.image_size, 2), 1), dtype=numpy.float64)
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

        image_shape = (self.image_size.value, self.image_size.value)

        first_image = Image.fromarray(
            numpy.uint8(cv2.normalize(
                src=best_try.reshape(image_shape), alpha=0, beta=255,
                dst=numpy.zeros_like(shape=image_shape), norm_type=cv2.NORM_MINMAX
            ).transpose()), mode='L'
        )

        first_image.save(
            fp=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../images/', f'{str(uuid.uuid4())}.bmp'))

        ThreadSafeTools.print(
            f" [x] Alguns dados sobre a imagem gerada:\n" +
            f"\tNúmero de iterações: {loop_counter}\n" +
            f"\tMenor taxa de erro: {best_try_error}\n" +
            f"\tUltima taxa de erro: {error}\n"
        )

        return first_image
