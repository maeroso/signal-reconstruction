from threading import Thread, Event

from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel

from model.generic_algorithm import GenericAlgorithm
from model.job_request import JobRequest
from model.rabbit_resolver import RabbitResolver
from utils.enums.queues import Queues
from utils.thread_safe_tools import ThreadSafeTools


class Worker(Thread):
    load_sources: Event

    def __init__(self, name: str, host: str, load_sources: Event):
        super().__init__(name=name)
        self.load_sources = load_sources
        self.start()

    def run(self) -> None:
        with RabbitResolver(queue_name=Queues.JOB_REQUEST_QUEUE, callback=self.consume_message) as rabbit_resolver:
            rabbit_resolver.start_consuming(thread_name=self.name)

    def consume_message(self, ch: BlockingChannel, method, properties: BasicProperties, body: bytes) -> None:
        job_request = JobRequest.parse_raw(body.decode('utf-8'))

        ThreadSafeTools.print(f' [x] Received message: \n{job_request.json(ident=True)}\n')

        with GenericAlgorithm.factory_method(
                signal=job_request.signal_array, image_size=job_request.image_size,
                algorithm=job_request.algorithm
        ) as algorithm:
            self.load_sources.set()
            image = algorithm.generate_image()

            # TODO send image to the back-end
            # TODO compute generation time

        ch.basic_ack(delivery_tag=method.delivery_tag)
