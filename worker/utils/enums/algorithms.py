from enum import unique, IntEnum


@unique
class Algorithms(IntEnum):
    """
    Enum for algorithms
    """

    CONJUGATE_GRADIENT_METHOD_NORMAL_ERROR = 1
    CONJUGATE_GRADIENT_NORMAL_RESIDUAL = 2
    FATS_ITERATIVE_SHRINKAGE_THRESHOLD_ALGORITHM = 3
