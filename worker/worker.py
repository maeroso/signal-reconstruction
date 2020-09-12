# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'


import math

import cv2
import numpy
import pandas
import pika
from PIL import Image

import constantes

# global data
print(' [*] Loading global data. Wait!')

H = pandas.read_csv('./../files/H-1/H-1.txt',
                    header=None, dtype=float).to_numpy()

minimal_error = numpy.float64('1.0e-4')

c = numpy.linalg.norm(numpy.matmul(H.transpose(), H), ord=2)


def cgne(g):
    f_old = numpy.zeros_like(numpy.matmul(H.transpose(), g))

    r_old = g - numpy.matmul(H, f_old)

    p_old = numpy.matmul(H.transpose(), r_old)

    loop_counter = 0

    loop_maximum = 100

    f_next = 0

    error = 0

    best_try = []

    best_try_error = 99999999999

    while loop_counter < loop_maximum:

        a_i = numpy.matmul(r_old.transpose(), r_old, dtype=float) / \
              numpy.matmul(p_old.transpose(), p_old)

        f_next = f_old + p_old * a_i

        r_next = r_old - numpy.matmul(H, p_old) * a_i

        beta = numpy.divide(numpy.matmul(r_next.transpose(), r_next),
                            numpy.matmul(r_old.transpose(), r_old))

        p_next = numpy.matmul(H.transpose(), r_next) + p_old * beta

        error = numpy.absolute(numpy.linalg.norm(
            r_next, ord=2) - numpy.linalg.norm(r_old, ord=2))

        p_old = p_next

        f_old = f_next

        r_old = r_next

        if error < best_try_error:
            best_try = f_next
            best_try_error = error

        if error < minimal_error:
            break

        loop_counter = 1 + loop_counter

    if loop_counter >= loop_maximum:
        print(' [x] Maximum of', loop_maximum, 'attempts reached, error remains at', error)
        print(' [x] Showing best attempt with error at', best_try_error)
        f_next = best_try

    f_reshaped = f_next.reshape(60, 60)

    first_image = Image.fromarray(cv2.normalize(
        f_reshaped.transpose(), numpy.zeros_like(f_reshaped), 255, 0, cv2.NORM_MINMAX))

    first_image.show()


def s_function(signal, threshold):
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


def fast_iterative_shrinkage_thresholding_algorithm(g):
    f_old = numpy.zeros_like(numpy.matmul(H.transpose(), g))

    y_old = f_old

    alfa_old = float(1)

    lambda_value = numpy.max(numpy.absolute(
        numpy.matmul(H.transpose(), g))) * 0.10

    threshold = numpy.absolute(lambda_value / c)

    f_next = 0

    loop_counter = 0

    loop_maximum = 30

    error = 0

    for x in range(15):

        f_next = y_old + numpy.matmul(
            H.transpose() * (1 / c),
            numpy.subtract(g, numpy.matmul(H, y_old))
        )

        index = 0

        for signal in f_next:
            f_next[index] = s_function(signal, threshold)

            index += 1

        alfa_next = (1 + numpy.sqrt(1 + 4 * math.pow(alfa_old, 2))) / 2

        y_next = f_next + ((alfa_old - 1) / alfa_next) * (f_next - f_old)

        f_old = f_next

        alfa_old = alfa_next

        y_old = y_next

    if loop_counter >= loop_maximum:
        print('[x] Maximum attempt limit reached, image error remains at ', error)

    f_reshaped = f_next.reshape(60, 60)

    first_image = Image.fromarray(cv2.normalize(
        f_reshaped.transpose(), numpy.zeros_like(f_reshaped), 255, 0, cv2.NORM_MINMAX))

    first_image.show()


print(' [*] Opening communication channel')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=constantes.nome_fila_cgne, durable=True)
channel.queue_declare(queue=constantes.nome_fila_fista, durable=True)
print(' [*] Waiting for messages')


def convert_string_to_float(value):
    return float(value)


def cgne_worker(ch, method, properties, body):
    print(" [x] Received message on cgne worker")

    decoded = body.decode()

    splinted = decoded.split(',')

    string_array = numpy.array(splinted)

    g = string_array.astype(numpy.float64)

    ch.basic_ack(delivery_tag=method.delivery_tag)

    # call the algorithm passing 'g' by parameter
    cgne(g)

    print(" [x] Done - CGNE")


def fista_worker(ch, method, properties, body):
    print(" [x] Received message on FISTA worker")

    decoded = body.decode()

    splinted = decoded.split(',')

    string_array = numpy.array(splinted)

    g = string_array.astype(numpy.float64)

    # call the algorithm passing 'g' by parameter
    fast_iterative_shrinkage_thresholding_algorithm(g)

    print(" [x] Done - FISTA")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=constantes.nome_fila_cgne,
                      on_message_callback=cgne_worker)
channel.basic_consume(queue=constantes.nome_fila_fista,
                      on_message_callback=fista_worker)

channel.start_consuming()
