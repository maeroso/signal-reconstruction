import os
from threading import Event
from typing import Tuple

import numpy
from PIL import Image
from pandas import read_pickle

from utils.enums.algorithms import Algorithms
from utils.enums.file_name import FileName
from utils.enums.image_size_options import ImageSizeOptions


class GenericAlgorithm:
    signal_array: numpy.ndarray
    image_size: ImageSizeOptions
    free_resource_event: Event = Event()
    matriz_ht_path: str
    matriz_h_path: str
    shape_matriz_h: Tuple[int, int]
    erro_minimo: numpy.float64

    def __init__(self, signal: numpy.ndarray, image_size: ImageSizeOptions):
        super().__init__()
        self.signal_array: numpy.ndarray = signal
        self.image_size = image_size

    def __enter__(self):
        self.free_resource_event.clear()

        self.matriz_h_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../static/',
            FileName.H1_PICKLE.value if self.image_size == ImageSizeOptions.MEDIUM else FileName.H2_PICKLE.value
        )
        self.matriz_ht_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../static/',
            FileName.HT1_PICKLE.value if self.image_size == ImageSizeOptions.MEDIUM else FileName.HT2_PICKLE.value
        )

        self.shape_matriz_h = read_pickle(filepath_or_buffer=self.matriz_h_path).to_numpy().shape

        self.erro_minimo = numpy.float64('1.0e-4')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.signal_array
        del self.free_resource_event
        del self.matriz_h_path
        del self.matriz_ht_path
        del self.shape_matriz_h
        del self.erro_minimo
        del self.image_size
        del self

    def generate_image(self) -> Image:
        raise NotImplementedError

    @staticmethod
    def factory_method(signal: numpy.ndarray, image_size: ImageSizeOptions, algorithm: Algorithms):
        raise NotImplementedError
