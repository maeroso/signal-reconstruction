# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import time
import cv2
from PIL import Image
import numpy
import pandas
import math
import tracemalloc
import resource


tracemalloc.start()


print(
    f"Current memory usage is {tracemalloc.get_traced_memory()[0] / 10**6}MB")


# %%

H = pandas.read_csv('./../files/H-1/H-1.txt',
                    header=None, dtype=float).to_numpy()

print(
    f"Current memory usage is {tracemalloc.get_traced_memory()[0] / 10**6}MB")

# %%

g = pandas.read_csv('./../files/avaliacao/sinal2.csv', sep='\n',
                    decimal=',', header=None, dtype=float).to_numpy()

print(
    f"Current memory usage is {tracemalloc.get_traced_memory()[0] / 10**6}MB")

# %%
erroMinimo = numpy.float64('1.0e-4')

print(
    f"Current memory usage is {tracemalloc.get_traced_memory()[0] / 10**6}MB")

# %%


f_old = numpy.zeros_like(numpy.matmul(H.transpose(), g))

r_old = g - numpy.matmul(H, f_old)


p_old = numpy.matmul(H.transpose(), r_old)


while True:

    a_i = numpy.matmul(r_old.transpose(), r_old, dtype=float) / \
        numpy.matmul(p_old.transpose(), p_old)

    f_next = f_old + numpy.matmul(p_old, a_i)

    r_next = r_old - numpy.matmul(numpy.matmul(H, p_old), a_i)

    beta = numpy.divide(numpy.matmul(r_next.transpose(), r_next),
                        numpy.matmul(r_old.transpose(), r_old))

    p_next = numpy.matmul(H.transpose(), r_next) + numpy.matmul(p_old, beta)

    erro = numpy.absolute(numpy.linalg.norm(
        r_next, ord=2) - numpy.linalg.norm(r_old, ord=2))

    p_old = p_next

    f_old = f_next

    r_old = r_next

    if erro < erroMinimo:
        break

print(
    f"Current memory usage is {tracemalloc.get_traced_memory()[0] / 10**6}MB")

f_reshaped = f_next.reshape(60, 60)

primeiraImagem = Image.fromarray(cv2.normalize(
    f_reshaped.transpose(), numpy.zeros_like(f_reshaped), 255, 0, cv2.NORM_MINMAX))

primeiraImagem.show()

print(
    f"Current memory usage is {tracemalloc.get_traced_memory()[0] / 10**6}MB")

# %%

c = numpy.linalg.norm(numpy.matmul(H.transpose(), H), ord=2)

print(
    f"Current memory usage is {tracemalloc.get_traced_memory()[0] / 10**6}MB")

# %%

f_old = numpy.zeros_like(numpy.matmul(H.transpose(), g))

y_old = f_old

alfa_old = float(1)


lambdaValue = numpy.max(numpy.absolute(numpy.matmul(H.transpose(), g))) * 0.10

limiar = numpy.absolute(lambdaValue / c)
print(
    f"Current memory usage is {tracemalloc.get_traced_memory()[0] / 10**6}MB")

for x in range(2):

    shrinkageVector = y_old + numpy.matmul(
        H.transpose() * (1/c),
        numpy.subtract(g, numpy.matmul(H, y_old))
    )

    f_next = numpy.where(numpy.logical_or(
        shrinkageVector <= -limiar, shrinkageVector >= limiar), 0, shrinkageVector)

    alfa_next = (1 + numpy.sqrt(1 + 4 * math.pow(alfa_old, 2))) / 2

    y_next = f_next + ((alfa_old - 1)/alfa_next) * (f_next - f_old)

    f_old = f_next

    alfa_old = alfa_next

    y_old = y_next

print(
    f"Current memory usage is {tracemalloc.get_traced_memory()[0] / 10**6}MB")


f_reshaped = f_next.reshape(60, 60)

primeiraImagem = Image.fromarray(cv2.normalize(
    f_reshaped.transpose(), numpy.zeros_like(f_reshaped), 255, 0, cv2.NORM_MINMAX))

primeiraImagem.show()


tracemalloc.stop()

# %%
