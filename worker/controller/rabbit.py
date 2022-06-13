import pika

from utils.enums.queues import Queues
from utils.thread_safe_tools import ThreadSafeTools


class Rabbit:

    def __init__(self, queue_name: Queues):
        ThreadSafeTools.print(' [*] Opening connection\n')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters())

        ThreadSafeTools.print(' [*] Opening channel\n')
        self.channel = self.connection.channel()

        ThreadSafeTools.print(f' [*] Declaring queue: {queue_name.value}\n')
        self.queue = self.channel.queue_declare(queue=queue_name.value, durable=True)
