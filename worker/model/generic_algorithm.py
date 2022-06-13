from threading import Event

import numpy


class GenericAlgorithm:
    signal_array: numpy.ndarray
    free_resource_event: Event = Event()

    def __init__(self, signal: numpy.ndarray):
        super().__init__()
        self.signal_array: numpy.ndarray = signal
        self.free_resource_event.clear()
