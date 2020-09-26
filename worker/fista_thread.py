import math

import cv2
from PIL import Image

from global_data import GlobalData
from threading import Thread
import numpy


class FISTAThread(Thread):

    def __init__(self, global_data: GlobalData, g: numpy.ndarray):
        super().__init__()
        self.global_data = global_data
        self.signal_array = g
        self.start()

    @staticmethod
    def s_function(signal, threshold):
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

    def run(self):
        f_old = numpy.zeros_like(numpy.matmul(self.global_data.get_transpose_h(), self.signal_array))

        y_old = f_old

        alfa_old = float(1)

        lambda_value = numpy.max(numpy.absolute(
            numpy.matmul(self.global_data.get_transpose_h(), self.signal_array))) * 0.10

        threshold = numpy.absolute(lambda_value / self.global_data.c)

        f_next = 0

        loop_counter = 0

        loop_maximum = 30

        error = 0

        for x in range(15):

            f_next = y_old + numpy.matmul(
                self.global_data.get_transpose_h() * (1 / self.global_data.c),
                numpy.subtract(self.signal_array, numpy.matmul(self.global_data.H, y_old))
            )

            index = 0

            for signal in f_next:
                f_next[index] = self.s_function(signal, threshold)

                index += 1

            alfa_next = (1 + numpy.sqrt(1 + 4 * math.pow(alfa_old, 2))) / 2

            y_next = f_next + ((alfa_old - 1) / alfa_next) * (f_next - f_old)

            f_old = f_next

            alfa_old = alfa_next

            y_old = y_next

        if loop_counter >= loop_maximum:
            print('[x] Maximum attempt limit reached, image error remains at ', error)

        f_reshaped = f_next.reshape(60, 60)

        first_image = Image.fromarray(cv2.normalize(
            f_reshaped.transpose(), numpy.zeros_like(f_reshaped), 255, 0, cv2.NORM_MINMAX))

        first_image.save('./images/last_generated_image_by_fista_algorithm.jpg')
