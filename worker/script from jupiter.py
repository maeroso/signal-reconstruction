# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

import time
import cv2
from PIL import Image
import numpy
import pandas

start = time.time()

H = pandas.read_csv('./files/H-1/H-1.txt',
                    header=None, dtype=float).to_numpy()


g = pandas.read_csv('./files/avaliacao/sinal1.csv', sep='\n',
                        decimal=',', header=None, dtype=float).to_numpy()

f_old = numpy.zeros_like(numpy.matmul(H.transpose(), g))

r_old = g - numpy.matmul(H, f_old)


p_old = numpy.matmul(H.transpose(), r_old)


for index in range(1):

    a_i = numpy.matmul(r_old.transpose(), r_old, dtype=float) / \
        numpy.matmul(p_old.transpose(), p_old)

    f_next = f_old + numpy.matmul(p_old, a_i)

    r_next = r_old - numpy.matmul(numpy.matmul(H, p_old), a_i)

    beta = numpy.divide(numpy.matmul(r_next.transpose(), r_next),
                        numpy.matmul(r_old.transpose(), r_old))

    p_next = numpy.matmul(H.transpose(), r_next) + numpy.matmul(p_old, beta)

    p_old = p_next

    f_old = f_next

    r_old = r_next

end = time.time()
print('Fim do precessamento da imagem -> Minutos: ' + str(int((end - start) / 60)) +
      '   Segundos: ' + str(int((end - start) / 60)))

f_reshaped = f_next.reshape(60, 60)

primeiraImagem = Image.fromarray(cv2.normalize(
    f_reshaped, numpy.zeros_like(f_reshaped), 255, 0, cv2.NORM_MINMAX))

primeiraImagem.show()


# %%
