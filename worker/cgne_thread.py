from threading import Thread

import cv2
import numpy
from PIL import Image

from global_data import GlobalData


class CgneThread(Thread):

    def __init__(self, global_data: GlobalData, g: numpy.ndarray):
        super().__init__()
        self.global_data = global_data
        self.signal = g
        self.run()

    def run(self):
        f_old = numpy.zeros_like(numpy.matmul(self.global_data.get_transpose_h(), self.signal))

        r_old = self.signal - numpy.matmul(self.global_data.H, f_old)

        p_old = numpy.matmul(self.global_data.get_transpose_h(), r_old)

        loop_counter = 0

        loop_maximum = 100

        f_next = 0

        error = 0

        best_try = []

        best_try_error = 99999999999

        while loop_counter < loop_maximum:

            a_i = numpy.matmul(r_old.transpose(), r_old, dtype=float) / \
                  numpy.matmul(p_old.transpose(), p_old)

            f_next = f_old + p_old * a_i

            r_next = r_old - numpy.matmul(self.global_data.H, p_old) * a_i

            beta = numpy.divide(numpy.matmul(r_next.transpose(), r_next),
                                numpy.matmul(r_old.transpose(), r_old))

            p_next = numpy.matmul(self.global_data.get_transpose_h(), r_next) + p_old * beta

            error = numpy.absolute(numpy.linalg.norm(
                r_next, ord=2) - numpy.linalg.norm(r_old, ord=2))

            p_old = p_next

            f_old = f_next

            r_old = r_next

            if error < best_try_error:
                best_try = f_next
                best_try_error = error

            if error < self.global_data.minimal_error:
                break

            loop_counter = 1 + loop_counter

        if loop_counter >= loop_maximum:
            print(' [x] Maximum of', loop_maximum, 'attempts reached, error remains at', error)
            print(' [x] Showing best attempt with error at', best_try_error)
            f_next = best_try

        f_reshaped = f_next.reshape(60, 60)

        first_image = Image.fromarray(cv2.normalize(
            f_reshaped.transpose(), numpy.zeros_like(f_reshaped), 255, 0, cv2.NORM_MINMAX))

        first_image.show()
