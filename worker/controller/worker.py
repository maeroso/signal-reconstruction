from threading import Thread, Event

from pika import ConnectionParameters, BlockingConnection, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.frame import Method

from model.message import Message
from utils.enums.queues import Queues
from utils.thread_safe_tools import ThreadSafeTools


class Worker(Thread):
    rabbit_connection: BlockingConnection
    rabbit_channel: BlockingChannel
    load_sources: Event
    rabbit_queue: Method

    def __init__(self, name: str, host: str, load_sources: Event):
        super().__init__(name=name)
        self.rabbit_connection = BlockingConnection(ConnectionParameters(host=host))
        self.rabbit_channel = self.rabbit_connection.channel()
        self.load_sources = load_sources

        self.rabbit_queue = self.rabbit_channel.queue_declare(queue=Queues.WORKER.value, durable=True)
        self.rabbit_channel.basic_qos(prefetch_count=1)
        self.rabbit_channel.basic_consume(queue=Queues.WORKER.value, on_message_callback=self.consume_message)

        self.start()

    def run(self) -> None:
        try:
            self.rabbit_channel.start_consuming()
        except Exception as e:
            ThreadSafeTools.print(f' [X] Error on {self.name}: {e}')
        finally:
            self.rabbit_channel.stop_consuming()
            self.rabbit_connection.close()

    @staticmethod
    def consume_message(ch: BlockingChannel, method, properties: BasicProperties, body: bytes) -> None:

        job_request = Message.parse_raw(body.decode('utf-8'))

        ThreadSafeTools.print(f' [x] Received message: \n{job_request.json(ident=True)}\n')
