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


class FastIterativeShrinkageThresholdAlgorithm(GenericAlgorithm):

    def __init__(self, sinal: numpy.ndarray, image_size: ImageSizeOptions):
        super().__init__(sinal, image_size)

        self.__c = numpy.linalg.norm(
            numpy.matmul(
                read_pickle(filepath_or_buffer=self.matriz_ht_path).to_numpy(),
                read_pickle(filepath_or_buffer=self.matriz_h_path).to_numpy()
            ),
            ord=2
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.__c
        super(FastIterativeShrinkageThresholdAlgorithm, self).__exit__(exc_type, exc_val, exc_tb)

    @staticmethod
    def factory_method(signal: numpy.ndarray, image_size: ImageSizeOptions,
                       algorithm: Algorithms.FAST_ITERATIVE_SHRINKAGE_THRESHOLD_ALGORITHM) -> GenericAlgorithm:
        return FastIterativeShrinkageThresholdAlgorithm(signal, image_size)

    @staticmethod
    def s_function(signal, threshold) -> int:
        if signal >= 0:
            if signal - threshold < 0:
                return 0
            else:
                return signal - threshold
        else:
            if signal + threshold >= 0:
                return 0
            else:
                return signal + threshold

    def generate_image(self) -> Image:

        f_old = numpy.zeros((pow(self.image_size.value, 2), 1), dtype=numpy.float64)
        y_old = f_old
        alfa_old = float(1)
        lambda_value = numpy.multiply(
            numpy.max(numpy.absolute(
                numpy.matmul(
                    read_pickle(filepath_or_buffer=self.matriz_ht_path).to_numpy(),
                    self.signal_array
                )
            )),
            0.10
        )
        threshold = numpy.absolute(numpy.divide(lambda_value, self.__c))
        f_next = 0
        loop_counter = 0
        loop_maximum = 20
        error = 0

        for counter in range(loop_maximum):

            # TODO esse método pesa 2 GB de RAM, deve ser quebrado em pedaçoes menores para debbug e melhoramentos
            f_next = numpy.add(
                y_old, numpy.matmul(
                    numpy.multiply(
                        read_pickle(filepath_or_buffer=self.matriz_ht_path).to_numpy(),
                        numpy.divide(1, self.__c)
                    ),
                    numpy.subtract(
                        self.signal_array,
                        numpy.matmul(read_pickle(filepath_or_buffer=self.matriz_h_path).to_numpy(), y_old)
                    )
                )
            )
            index = 0

            # TODO essa iteração é extremamente demorada, provavelmente dvido a troca de contexto contante,
            #  uma solução se faz necessária
            for signal in f_next:
                if signal >= 0:
                    if signal - threshold < 0:
                        f_next[index] = 0
                    else:
                        f_next[index] = numpy.subtract(signal, threshold)
                else:
                    if signal + threshold >= 0:
                        f_next[index] = 0
                    else:
                        f_next[index] = numpy.add(signal, threshold)

                index += 1

            alfa_next = numpy.divide(
                numpy.add(
                    1,
                    numpy.sqrt(numpy.add(
                        1,
                        numpy.multiply(
                            4,
                            numpy.power(alfa_old, 2)
                        )
                    ))
                ),
                2
            )
            y_next = numpy.add(
                f_next,
                numpy.multiply(
                    numpy.divide(
                        numpy.subtract(alfa_old, 1),
                        alfa_next
                    ),
                    numpy.subtract(f_next, f_old)
                )
            )
            f_old = f_next
            alfa_old = alfa_next
            y_old = y_next
            loop_counter = counter

        image_shape = (self.image_size.value, self.image_size.value)

        first_image = Image.fromarray(
            numpy.uint8(cv2.normalize(
                src=f_old.reshape(image_shape), alpha=0, beta=255,
                dst=numpy.zeros_like(shape=image_shape), norm_type=cv2.NORM_MINMAX
            ).transpose()), mode='L'
        )

        first_image.save(
            fp=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../images/', f'{str(uuid.uuid4())}.bmp'))

        ThreadSafeTools.print(
            f" [x] Alguns dados sobre a imagem gerada:\n" +
            f"\tNúmero de iterações: {loop_counter}\n" +
            # f"\tMenor taxa de erro: {ultimo_erro}\n" +
            f"\tUltima taxa de erro: {error}\n"
        )

        return first_image
