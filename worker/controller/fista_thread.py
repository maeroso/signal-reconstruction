from threading import Thread, Event

import cv2
import numpy
from PIL import Image

from ..utils.global_data import GlobalData
from ..utils.thread_safe_tools import ThreadSafeTools
from ..controller.resource_controller_thread import ResourceControllerThread
from ..model.solicitation_resource_access_container import SolicitationResourceAccessContainer


class FISTAThread(Thread):

    def __init__(self, global_data: GlobalData, g: numpy.ndarray, controller: ResourceControllerThread):
        super().__init__()
        self.global_data = global_data
        self.signal_array = g
        self.free_resource_event: Event = Event()
        self.free_resource_event.clear()
        self.resource_controller = controller

        self.start()
        ThreadSafeTools.print(" [*] FISTA thread was initiate. Id: " + str(self.ident) + "\n")

    @staticmethod
    def s_function(signal, threshold) -> int:
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

    def run(self) -> None:
        f_old = numpy.zeros((3600,), dtype=numpy.float64)

        y_old = f_old

        alfa_old = float(1)

        lambda_value = numpy.multiply(
            numpy.max(
                numpy.absolute(
                    numpy.matmul(self.global_data.get_transpose_h(), self.signal_array)
                )
            ), 0.10)

        threshold = numpy.absolute(
            numpy.divide(lambda_value, self.global_data.c)
        )

        f_next = 0

        loop_counter = 0

        loop_maximum = 20

        error = 0

        for counter in range(loop_maximum):

            self.resource_controller.request_resource(SolicitationResourceAccessContainer(
                minimum_free_memory=2,
                identification=self.ident,
                maximum_cpu_load=85,
                thread_wake_up_event=self.free_resource_event
            ))

            # TODO esse método pesa 2 GB de RAM, deve ser quebrado em pedaçoes menores para debbug e melhoramentos
            f_next = numpy.add(y_old,
                               numpy.matmul(
                                   numpy.multiply(self.global_data.get_transpose_h(),
                                                  numpy.divide(1, self.global_data.c)
                                                  ),
                                   numpy.subtract(self.signal_array,
                                                  numpy.matmul(self.global_data.H, y_old)
                                                  )
                               )
                               )

            index = 0

            self.resource_controller.request_resource(SolicitationResourceAccessContainer(
                identification=self.ident,
                thread_wake_up_event=self.free_resource_event,
                maximum_cpu_load=70
            ))

            # TODO essa iteração é extremamente demorada, provavelmente dvido a troca de contexto contante,
            #  uma solução se faz necessária
            for signal in f_next:
                if signal >= 0:
                    if signal - threshold < 0:
                        f_next[index] = 0
                    else:
                        f_next[index] = numpy.subtract(signal, threshold)
                else:
                    if signal + threshold >= 0:
                        f_next[index] = 0
                    else:
                        f_next[index] = numpy.add(signal, threshold)

                index += 1

            alfa_next = numpy.divide(
                numpy.add(1,
                          numpy.sqrt(numpy.add(1,
                                               numpy.multiply(4,
                                                              numpy.power(alfa_old, 2)
                                                              )
                                               )
                                     )
                          )
                , 2
            )

            y_next = numpy.add(
                f_next,
                numpy.multiply(
                    numpy.divide(
                        numpy.subtract(alfa_old, 1), alfa_next
                    ),
                    numpy.subtract(f_next, f_old)
                )
            )

            f_old = f_next

            alfa_old = alfa_next

            y_old = y_next

            loop_counter = counter

        ThreadSafeTools.print(" [X] Data about image generated by fista thread " + str(self.ident) +
                              " -> actual error: " + str(error) + "  expected error: <" +
                              str(self.global_data.minimal_error) + "  loop counter: " + str(loop_counter) + "\n"
                              )

        f_reshaped = f_next.reshape(60, 60)

        normalized = cv2.normalize(src=f_reshaped, alpha=0, beta=255, dst=numpy.zeros_like(f_reshaped),
                                   norm_type=cv2.NORM_MINMAX)

        first_image = Image.fromarray(numpy.uint8(normalized.transpose()), mode='L')

        first_image.save('./images/FISTA - ' + str(self.ident) + '.bmp')

        del self
