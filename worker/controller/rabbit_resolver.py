from pika import ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.frame import Method

from utils.enums.queues import Queues
from utils.thread_safe_tools import ThreadSafeTools


class RabbitResolver:
    connection: BlockingConnection
    channel: BlockingChannel
    queue: Method

    def __init__(self, queue_name: Queues, host_name: str = 'localhost', port_number: int = 5672,
                 callback: callable = None, passive: bool = False):
        self.__queue_name = queue_name
        self.__host_name = host_name
        self.__port_number = port_number
        self.__consume_message_callback = callback
        self.__passive = passive

    def __enter__(self):
        ThreadSafeTools.print(' [*] Opening connection\n')
        self.connection = BlockingConnection(ConnectionParameters(host=self.__host_name, port=self.__port_number))

        ThreadSafeTools.print(' [*] Opening channel\n')
        self.channel = self.connection.channel()

        ThreadSafeTools.print(f' [*] Declaring queue: {self.__queue_name.value}\n')
        # TODO aumentar tempo de 'retry' na fila quando não receber o ACK
        self.queue = self.channel.queue_declare(
            queue=self.__queue_name.value, durable=True, passive=self.__passive
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.channel.stop_consuming()
        ThreadSafeTools.print(' [*] Closing channel\n')
        self.channel.close()
        ThreadSafeTools.print(' [*] Closing connection\n')
        self.connection.close()
        del self.queue
        del self.connection
        del self.channel
        del self.__queue_name
        del self

    def start_consuming(self, thread_name, prefetch_count: int = 1):
        ThreadSafeTools.print(f' [*] Starting consuming{" on thread %s" % thread_name if thread_name else ""}\n')
        self.channel.basic_qos(prefetch_count=prefetch_count)
        self.channel.basic_consume(queue=self.__queue_name.value, on_message_callback=self.__consume_message_callback)
        self.channel.start_consuming()
