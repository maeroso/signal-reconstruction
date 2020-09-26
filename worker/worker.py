# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

import json

import numpy
import pika

from cgne_thread import CgneThread
from constants import Constants
from fista_thread import FISTAThread
from global_data import GlobalData


class Worker:

    def worker_consume_queue(self, ch, method, properties, body):
        print(" [X] Consuming worker queue")

        decoded = body.decode()

        json_message = json.loads(
            # TODO tratar json antes de enviar para a fila, o back deve cuidar desse tratamento
            # TODO remover esse tratamento de emergencia feito com replace
            decoded.replace(',[""]', "")
        )

        if json_message['algorithmType'] == self.constants.cgne_algorithm_id:
            CgneThread(self.global_data, numpy.array(json_message['signalArray']))
            print(" [*] CGNE thread was initiate")
        else:
            FISTAThread(self.global_data, numpy.array(json_message['signalArray']))
            print(" [*] FISTA thread was initiate")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __init__(self):
        self.constants = Constants()

        self.global_data = GlobalData(False)

        print(' [*] Opening communication channel')

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.constants.worker_name_queue, durable=True)

        print(' [*] Waiting for messages')

        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume(queue=self.constants.worker_name_queue,
                                   on_message_callback=self.worker_consume_queue)

        self.channel.start_consuming()


Worker()
