from pandas import read_csv, DataFrame, read_pickle
import numpy
import cv2
from PIL import Image
from os.path import exists


class CGNR():
    __n_amostras = 794
    __n_sensores = 64
    __erro_minimo = numpy.float64('1.0e-4')
    __shape_matriz_h = None
    __shape_matriz_h_transposta = None
    __contador = 0
    __sinal = None
    __matriz_h_path = '../files/H-1/H-1.pickle'
    __matriz_ht_path = '../files/H-1/HT-1.pickle'

    def __init__(self):
        if exists(self.__matriz_h_path):
            self.__shape_matriz_h = read_pickle(filepath_or_buffer=self.__matriz_h_path).to_numpy().shape
        else:
            matriz_H = read_csv(filepath_or_buffer='../files/H-1/H-1.csv', header=None, dtype=float).to_numpy()
            self.__shape_matriz_h = matriz_H.shape
            DataFrame(data=matriz_H, dtype=float).to_pickle(path=self.__matriz_h_path)
        if exists(self.__matriz_ht_path):
            self.__shape_matriz_h_transposta = read_pickle(filepath_or_buffer=self.__matriz_ht_path).to_numpy().shape
        else:
            matriz_H_transposta = read_pickle(filepath_or_buffer=self.__matriz_h_path).to_numpy().transpose()
            self.__shape_matriz_h_transposta = matriz_H_transposta.shape
            DataFrame(data=matriz_H_transposta, dtype=float).to_pickle(path=self.__matriz_ht_path)

    def load_sinal(self, path: str, n_sinal_incremento: int = 1) -> None:
        sinal_original = read_csv(filepath_or_buffer=path, header=None, dtype=float, sep='\t',
                                  decimal=',').to_numpy()
        sinal = numpy.zeros(shape=sinal_original.shape)
        sinal_old = sinal_original
        for _ in range(n_sinal_incremento):
            for linha in range(self.__n_sensores):
                for coluna in range(self.__n_amostras):
                    epsulon = 100 + 1 / 20 * coluna * numpy.sqrt(coluna)
                    array_position = linha * self.__n_amostras + coluna
                    sinal[array_position, 0] = sinal_old[array_position, 0] * epsulon
            sinal_old = sinal
        self.__sinal = sinal

    def generate_image(self):
        f_old = numpy.zeros((3600, 1), dtype=numpy.float64)
        r_old = numpy.subtract(self.__sinal, numpy.zeros(shape=(self.__shape_matriz_h[0], 1)))
        z_old = numpy.matmul(read_pickle(filepath_or_buffer=self.__matriz_ht_path).to_numpy(), r_old)
        p_old = z_old

        ultimo_erro = numpy.float64('9999.0')
        melhor_imagem = f_old
        n_iteracao = 0
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
        first_image.save(fp=f'images/image numero {self.__contador}.bmp')
        print(
            f"Alguns dados sobre a imagem gerada:\n"
            f"\tNúmero de iterações: {n_iteracao}\n"
            f"\tMenor taxa de erro: {ultimo_erro}\n"
            f"\tUltima taxa de erro: {erro}\n"
        )
        self.__contador += 1


cgnr = CGNR()
cgnr.load_sinal(path='../files/avaliacao/sinal2.csv')
cgnr.generate_image()
