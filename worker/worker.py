# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

import numpy
import pika

from constantes import Constantes
from global_data import GlobalData
from fista_thread import FISTAThread
from cgne_thread import CgneThread


class Worker:

    def cgne_worker(self, ch, method, properties, body):
        print(" [x] Received message on cgne worker")

        decoded = body.decode()

        splinted = decoded.split(',')

        string_array = numpy.array(splinted)

        g = string_array.astype(numpy.float64)

        ch.basic_ack(delivery_tag=method.delivery_tag)

        # call the algorithm passing 'g' by parameter
        CgneThread(self.global_data, g)

        print(" [x] Done - CGNE")

    def fista_worker(self, ch, method, properties, body):
        print(" [x] Received message on FISTA worker")

        decoded = body.decode()

        splinted = decoded.split(',')

        string_array = numpy.array(splinted)

        g = string_array.astype(numpy.float64)

        # call the algorithm passing 'g' by parameter

        FISTAThread(self.global_data, g)

        print(" [x] Done - FISTA")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __init__(self):
        self.constants = Constantes()

        self.global_data = GlobalData(False)

        print(' [*] Opening communication channel')

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.constants.nome_fila_cgne, durable=True)
        self.channel.queue_declare(queue=self.constants.nome_fila_fista, durable=True)

        print(' [*] Waiting for messages')

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.constants.nome_fila_cgne,
                                   on_message_callback=self.cgne_worker)
        self.channel.basic_consume(queue=self.constants.nome_fila_fista,
                                   on_message_callback=self.fista_worker)

        self.channel.start_consuming()
