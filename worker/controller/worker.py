import os
import uuid
from datetime import datetime
from threading import Thread, Event

import cv2
import numpy
import requests as requests
from PIL import Image
from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel

from controller.conjugate_gradient_method_normal_error import ConjugateGradientMethodNormalError
from controller.conjugate_gradient_normal_residual import ConjugateGradientNormalResidual
from controller.fast_iterative_shrinkage_threshold_algorithm import FastIterativeShrinkageThresholdAlgorithm
from model.job_request import JobRequest
from model.rabbit_resolver import RabbitResolver
from model.result_response import ResultResponse
from utils.enums.algorithms import Algorithms
from utils.enums.queues import Queues
from utils.enums.status import Status


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
        decoded_body = body.decode('utf-8')

        job_request = JobRequest.parse_raw(decoded_body)

        # ThreadSafeTools.print(f' [x] Received message: \n{job_request.json(ident=True)}\n')

        computed_array: numpy.ndarray = numpy.zeros((pow(job_request.image_size.value, 2),), dtype=numpy.float64)
        interactions_count: int = 0

        requests.post(url=f'http://localhost:3333/job/{job_request.index}',
                      data=ResultResponse(init_datetime=datetime.now(), status=Status.PROCESSING).dict(
                          exclude_unset=True))
        if job_request.algorithm == Algorithms.CONJUGATE_GRADIENT_NORMAL_RESIDUAL:
            with ConjugateGradientNormalResidual.factory_method(
                    signal=job_request.signal_array, image_size=job_request.image_size,
                    algorithm=job_request.algorithm
            ) as algorithm:
                self.load_sources.set()
                computed_array, interactions_count = algorithm.generate_image()
        elif job_request.algorithm == Algorithms.CONJUGATE_GRADIENT_METHOD_NORMAL_ERROR:
            with ConjugateGradientMethodNormalError.factory_method(
                    signal=job_request.signal_array, image_size=job_request.image_size,
                    algorithm=job_request.algorithm
            ) as algorithm:
                self.load_sources.set()
                computed_array, interactions_count = algorithm.generate_image()
        elif job_request.algorithm == Algorithms.FAST_ITERATIVE_SHRINKAGE_THRESHOLD_ALGORITHM:
            with FastIterativeShrinkageThresholdAlgorithm.factory_method(
                    signal=job_request.signal_array, image_size=job_request.image_size,
                    algorithm=job_request.algorithm
            ) as algorithm:
                self.load_sources.set()
                computed_array, interactions_count = algorithm.generate_image()

        image_shape = (job_request.image_size, job_request.image_size)

        first_image = Image.fromarray(
            numpy.uint8(cv2.normalize(
                src=computed_array.reshape(image_shape), alpha=0, beta=255,
                dst=numpy.zeros(shape=image_shape), norm_type=cv2.NORM_MINMAX
            ).transpose()), mode='L'
        )

        first_image.save(
            fp=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../images/', f'{str(uuid.uuid4())}.bmp'))

        first_image.save(
            fp=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../backend/images',
                            f'{str(job_request.index)}.bmp'))

        requests.post(url=f'http://localhost:3333/job/{job_request.index}',
                      data=ResultResponse(final_datetime=datetime.now(), status=Status.FINISHED,
                                          interactions=interactions_count).json(
                          exclude_unset=True))

        ch.basic_ack(delivery_tag=method.delivery_tag)
