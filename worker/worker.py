import json

import numpy
import pika

from controller.cgne_thread import CgneThread
from controller.fista_thread import FISTAThread
from model.constants import Constants
from utils.global_data import GlobalData
from controller.resource_controller_thread import ResourceControllerThread

from utils.thread_safe_tools import ThreadSafeTools


class Worker:

    def worker_consume_queue(self, ch, method, properties, body) -> None:
        ThreadSafeTools.print(" [X] Consuming worker queue\n")

        decoded = body.decode()

        json_message = json.loads(decoded)

        if json_message['algorithmType'] == self.constants.cgne_algorithm_id:
            CgneThread(self.global_data, numpy.array(json_message['signalArray']), self.resource_controller)

        else:
            FISTAThread(self.global_data, numpy.array(json_message['signalArray']), self.resource_controller)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        ThreadSafeTools.print(' [*] Waiting for messages\n')

    def __init__(self):

        self.constants = Constants()

        self.global_data = GlobalData()

        self.resource_controller = ResourceControllerThread()

        ThreadSafeTools.print(' [*] Opening communication channel\n')

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.constants.worker_name_queue, durable=True)

        ThreadSafeTools.print(' [*] Waiting for messages\n')

        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume(queue=self.constants.worker_name_queue,
                                   on_message_callback=self.worker_consume_queue)

        self.channel.start_consuming()


Worker()
