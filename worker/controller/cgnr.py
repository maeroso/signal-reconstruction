import uuid

import cv2
import numpy
from PIL import Image
from pandas import read_pickle

from model.generic_algorithm import GenericAlgorithm
from utils.thread_safe_tools import ThreadSafeTools


class CGNR(GenericAlgorithm):

    def __init__(self, sinal: numpy.ndarray):
        super().__init__(sinal)

        ThreadSafeTools.print(" [*] CGNE thread was initiate. Id: " + str(self.ident) + "\n")
        self.__compute()

    def __compute(self) -> None:
        f_old = numpy.zeros((3600, 1), dtype=numpy.float64)
        r_old = numpy.subtract(self.signal_array, numpy.zeros(shape=(self.__shape_matriz_h[0], 1)))
        z_old = numpy.matmul(read_pickle(filepath_or_buffer=self.__matriz_ht_path).to_numpy(), r_old)
        p_old = z_old

        ultimo_erro = numpy.float64('9999.0')
        melhor_imagem = f_old
        n_iteracao = 0

        # TODO send event to check resources usage

        for _ in range(150):
            n_iteracao += 1
            w_new = numpy.matmul(read_pickle(filepath_or_buffer=self.__matriz_h_path).to_numpy(), p_old)
            alpha = numpy.divide(numpy.power(numpy.linalg.norm(z_old), 2), numpy.power(numpy.linalg.norm(w_new), 2))
            f_new = numpy.add(f_old, alpha * p_old)
            r_new = numpy.subtract(r_old, w_new * alpha)
            z_new = numpy.matmul(read_pickle(filepath_or_buffer=self.__matriz_ht_path).to_numpy(), r_new)
            beta = numpy.divide(numpy.power(numpy.linalg.norm(z_new), 2), numpy.power(numpy.linalg.norm(z_old), 2))
            p_new = numpy.add(z_new, beta * p_old)
            erro = numpy.absolute(numpy.subtract(numpy.linalg.norm(r_new, ord=2), numpy.linalg.norm(r_old, ord=2)))
            if erro < ultimo_erro:
                melhor_imagem = f_new
                ultimo_erro = erro
            if erro < self.__erro_minimo:
                print("Bateu no erro minimo")
                break
            f_old = f_new
            r_old = r_new
            z_old = z_new
            p_old = p_new
        reshape = melhor_imagem.reshape(60, 60)
        normalized = cv2.normalize(src=reshape, alpha=0, beta=255, dst=numpy.zeros_like(reshape),
                                   norm_type=cv2.NORM_MINMAX)
        first_image = Image.fromarray(numpy.uint8(normalized.transpose()), mode='L')

        # TODO send image to the back-end
        first_image.save(fp=f'images/{str(uuid.uuid4())}.bmp')

        print(
            f"Alguns dados sobre a imagem gerada:\n"
            f"\tNúmero de iterações: {n_iteracao}\n"
            f"\tMenor taxa de erro: {ultimo_erro}\n"
            f"\tUltima taxa de erro: {erro}\n"
        )
