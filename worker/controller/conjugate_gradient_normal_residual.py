import os.path
import uuid

import cv2
import numpy
from PIL import Image
from pandas import read_pickle

from model.generic_algorithm import GenericAlgorithm
from utils.enums.algorithms import Algorithms
from utils.enums.image_size_options import ImageSizeOptions
from utils.thread_safe_tools import ThreadSafeTools


class ConjugateGradientNormalResidual(GenericAlgorithm):

    def __init__(self, sinal: numpy.ndarray, image_size: ImageSizeOptions):
        super().__init__(sinal, image_size)

    @staticmethod
    def factory_method(signal: numpy.ndarray, image_size: ImageSizeOptions,
                       algorithm: Algorithms.CONJUGATE_GRADIENT_NORMAL_RESIDUAL) -> GenericAlgorithm:
        return ConjugateGradientNormalResidual(signal, image_size)

    def generate_image(self) -> Image:
        f_old = numpy.zeros((pow(self.image_size.value, 2), 1), dtype=numpy.float64)
        r_old = numpy.subtract(self.signal_array, numpy.zeros(shape=(self.shape_matriz_h[0], 1)))
        z_old = numpy.matmul(read_pickle(filepath_or_buffer=self.matriz_ht_path).to_numpy(), r_old)
        p_old = z_old

        ultimo_erro = numpy.float64('9999.0')
        melhor_imagem = f_old
        iteration_number = 0
        error: numpy.float64 = numpy.float64('0')

        for _ in range(150):
            iteration_number += 1
            w_new = numpy.matmul(read_pickle(filepath_or_buffer=self.matriz_h_path).to_numpy(), p_old)
            alpha = numpy.divide(numpy.power(numpy.linalg.norm(z_old), 2), numpy.power(numpy.linalg.norm(w_new), 2))
            f_new = numpy.add(f_old, alpha * p_old)
            r_new = numpy.subtract(r_old, w_new * alpha)
            z_new = numpy.matmul(read_pickle(filepath_or_buffer=self.matriz_ht_path).to_numpy(), r_new)
            beta = numpy.divide(numpy.power(numpy.linalg.norm(z_new), 2), numpy.power(numpy.linalg.norm(z_old), 2))
            p_new = numpy.add(z_new, beta * p_old)
            error = numpy.absolute(numpy.subtract(numpy.linalg.norm(r_new, ord=2), numpy.linalg.norm(r_old, ord=2)))
            if error < ultimo_erro:
                melhor_imagem = f_new
                ultimo_erro = error
            if error < self.erro_minimo:
                print("Bateu no erro minimo")
                break
            f_old = f_new
            r_old = r_new
            z_old = z_new
            p_old = p_new

        image_shape = (self.image_size.value, self.image_size.value)

        first_image = Image.fromarray(
            numpy.uint8(cv2.normalize(
                src=melhor_imagem.reshape(image_shape), alpha=0, beta=255,
                dst=numpy.zeros_like(shape=image_shape), norm_type=cv2.NORM_MINMAX
            ).transpose()), mode='L'
        )

        first_image.save(
            fp=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../images/', f'{str(uuid.uuid4())}.bmp'))

        ThreadSafeTools.print(
            f" [x] Alguns dados sobre a imagem gerada:\n" +
            f"\tNúmero de iterações: {iteration_number}\n" +
            f"\tMenor taxa de erro: {ultimo_erro}\n" +
            f"\tUltima taxa de erro: {error}\n"
        )

        return first_image
