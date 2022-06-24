import numpy
from pydantic import BaseModel

from utils.enums.algorithms import Algorithms
from utils.enums.image_size_options import ImageSizeOptions


class TypedArray(numpy.ndarray):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_type

    @classmethod
    def validate_type(cls, val):
        return numpy.array(val, dtype=cls.inner_type)


class ArrayMeta(type):
    def __getitem__(self, t):
        return type('Array', (TypedArray,), {'inner_type': t})


class Array(numpy.ndarray, metaclass=ArrayMeta):
    pass


class JobRequest(BaseModel):
    index: int
    algorithm: Algorithms
    signal_array: Array[float]
    image_size: ImageSizeOptions
