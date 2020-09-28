# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

import json
import sys
import time

import numpy
import pika
import psutil

from cgne_thread import CgneThread
from constants import Constants
from fista_thread import FISTAThread
from global_data import GlobalData


class Worker:

    def worker_consume_queue(self, ch, method, properties, body):
        sys.stdout.write(" [X] Consuming worker queue\n")

        decoded = body.decode()

        json_message = json.loads(
            # TODO tratar json antes de enviar para a fila, o back deve cuidar desse tratamento
            # TODO remover esse tratamento de emergencia feito com replace
            decoded.replace(',[""]', "")
        )

        show_warning_message = False

        overload = psutil.cpu_percent(percpu=False, interval=5) > 90

        low_memory = psutil.virtual_memory().free < 600000000

        while overload or low_memory:
            if not show_warning_message:
                if overload:
                    sys.stdout.write(" [!] Unable to launch the thread, CPU load greater than 90%\n")
                if low_memory:
                    sys.stdout.write(" [!] Unable to start the thread, RAM remaining less than 600Mb\n")
                show_warning_message = True

            time.sleep(.800)

            overload = psutil.cpu_percent(percpu=False, interval=5) > 90

            low_memory = psutil.virtual_memory().free < 250000000

        if json_message['algorithmType'] == self.constants.cgne_algorithm_id:
            CgneThread(self.global_data, numpy.array(json_message['signalArray']))
            sys.stdout.write(" [*] CGNE thread was initiate\n")
        else:
            FISTAThread(self.global_data, numpy.array(json_message['signalArray']))
            sys.stdout.write(" [*] FISTA thread was initiate\n")

        ch.basic_ack(delivery_tag=method.delivery_tag)
        sys.stdout.write(' [*] Waiting for messages\n')

    def __init__(self):

        self.constants = Constants()

        self.global_data = GlobalData()

        sys.stdout.write(' [*] Opening communication channel\n')

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.constants.worker_name_queue, durable=True)

        sys.stdout.write(' [*] Waiting for messages\n')

        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume(queue=self.constants.worker_name_queue,
                                   on_message_callback=self.worker_consume_queue)

        self.channel.start_consuming()


Worker()
