import numpy

from controller.conjugate_gradient_method_normal_error import ConjugateGradientMethodNormalError
from controller.conjugate_gradient_normal_residual import ConjugateGradientNormalResidual
from controller.fast_iterative_shrinkage_threshold_algorithm import FastIterativeShrinkageThresholdAlgorithm
from model.generic_algorithm import GenericAlgorithm
from utils.enums.algorithms import Algorithms
from utils.enums.image_size_options import ImageSizeOptions


class FactoryAlgorithm:

    @staticmethod
    def factor(signal: numpy.ndarray, image_size: ImageSizeOptions, algorithm: Algorithms) -> GenericAlgorithm:

        if algorithm == Algorithms.CONJUGATE_GRADIENT_NORMAL_RESIDUAL:
            return ConjugateGradientNormalResidual(signal, image_size)
        elif algorithm == Algorithms.CONJUGATE_GRADIENT_METHOD_NORMAL_ERROR:
            return ConjugateGradientMethodNormalError(signal, image_size)
        elif algorithm == Algorithms.FAST_ITERATIVE_SHRINKAGE_THRESHOLD_ALGORITHM:
            return FastIterativeShrinkageThresholdAlgorithm(signal, image_size)
        else:
            raise NotImplementedError("Algoritmo solicitado não foi implementado")
