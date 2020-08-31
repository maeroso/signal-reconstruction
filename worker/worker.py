# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'


import cv2
from PIL import Image
import numpy
import pandas
import math
import pika
import constantes

# variaveis globais
print(' [*] Carregando dados globais. Aguarde!')

H = pandas.read_csv('./../files/H-1/H-1.txt',
                    header=None, dtype=float).to_numpy()

erro_minimo = numpy.float64('1.0e-4')

c = numpy.linalg.norm(numpy.matmul(H.transpose(), H), ord=2)


def cgne(g):

    f_old = numpy.zeros_like(numpy.matmul(H.transpose(), g))

    r_old = g - numpy.matmul(H, f_old)

    p_old = numpy.matmul(H.transpose(), r_old)

    while True:

        a_i = numpy.matmul(r_old.transpose(), r_old, dtype=float) / \
            numpy.matmul(p_old.transpose(), p_old)

        f_next = f_old + p_old * a_i

        r_next = r_old - numpy.matmul(H, p_old) * a_i

        beta = numpy.divide(numpy.matmul(r_next.transpose(), r_next),
                            numpy.matmul(r_old.transpose(), r_old))

        p_next = numpy.matmul(H.transpose(), r_next) + \
            p_old * beta

        erro = numpy.absolute(numpy.linalg.norm(
            r_next, ord=2) - numpy.linalg.norm(r_old, ord=2))

        p_old = p_next

        f_old = f_next

        r_old = r_next

        if erro < erro_minimo:
            break

    f_reshaped = f_next.reshape(60, 60)

    primeira_imagem = Image.fromarray(cv2.normalize(
        f_reshaped.transpose(), numpy.zeros_like(f_reshaped), 255, 0, cv2.NORM_MINMAX))

    primeira_imagem.show()


def funcao_s(sinal, index, limiar):
    if sinal >= 0:
        if sinal - limiar < 0:
            return 0
        else:
            return sinal - limiar
    else:
        if sinal + limiar >= 0:
            return 0
        else:
            return sinal + limiar


def fast_iterative_shrinkage_thresjolding_algorithm(g):

    f_old = numpy.zeros_like(numpy.matmul(H.transpose(), g))

    y_old = f_old

    alfa_old = float(1)

    lambda_value = numpy.max(numpy.absolute(
        numpy.matmul(H.transpose(), g))) * 0.10

    limiar = numpy.absolute(lambda_value / c)

    for x in range(5):

        f_next = y_old + numpy.matmul(
            H.transpose() * (1/c),
            numpy.subtract(g, numpy.matmul(H, y_old))
        )

        index = 0

        for sinal in f_next:

            f_next[index] = funcao_s(sinal, index, limiar)

            index += 1

        alfa_next = (1 + numpy.sqrt(1 + 4 * math.pow(alfa_old, 2))) / 2

        y_next = f_next + ((alfa_old - 1)/alfa_next) * (f_next - f_old)

        f_old = f_next

        alfa_old = alfa_next

        y_old = y_next

    f_reshaped = f_next.reshape(60, 60)

    primeira_imagem = Image.fromarray(cv2.normalize(
        f_reshaped.transpose(), numpy.zeros_like(f_reshaped), 255, 0, cv2.NORM_MINMAX))

    primeira_imagem.show()


print(' [*] Abrindo canal de comunicação')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=constantes.nome_fila_cgne, durable=True)
channel.queue_declare(queue=constantes.nome_fila_fista, durable=True)
print(' [*] Aguardando por mensagens')


def cgne_worker(ch, method, properties, body):
    print(" [x] Received message on cgne worker")

    g = numpy.fromstring(body)

    # chamar o algoritmo passando G por parâmetro
    cgne(g)

    print(" [x] Done - CGNE")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def fista_worker(ch, method, properties, body):
    print(" [x] Received message on fista worker")

    g = numpy.fromstring(body)

    # chamar o algoritmo passando G por parâmetro
    fast_iterative_shrinkage_thresjolding_algorithm(g)

    print(" [x] Done - FISTA")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=constantes.nome_fila_cgne,
                      on_message_callback=cgne_worker)
channel.basic_consume(queue=constantes.nome_fila_fista,
                      on_message_callback=fista_worker)

channel.start_consuming()
