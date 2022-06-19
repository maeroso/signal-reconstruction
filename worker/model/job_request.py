import numpy
from pydantic import BaseModel, validator

from utils.enums.algorithms import Algorithms
from utils.enums.image_size_options import ImageSizeOptions


class JobRequest(BaseModel):
    index: int
    algorithm: Algorithms
    signal_array: numpy.ndarray
    image_size: ImageSizeOptions

    @staticmethod
    @validator('signal_array', pre=True)
    def parse_values(value):
        return numpy.array(value, dtype=float)

    class Config:
        arbitrary_types_allowed = True
