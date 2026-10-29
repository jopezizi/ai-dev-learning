"""Osa 1.4: neuroverkko omasta Value-luokasta."""

import random

from autograd import Value


class Neuron:
    def __init__(self, n_in):
        raise NotImplementedError("Tehtävä 13")

    def __call__(self, x):
        raise NotImplementedError("Tehtävä 13")

    def parameters(self):
        raise NotImplementedError("Tehtävä 13")


class Layer:
    def __init__(self, n_in, n_out):
        raise NotImplementedError("Tehtävä 13")

    def __call__(self, x):
        raise NotImplementedError("Tehtävä 13")

    def parameters(self):
        raise NotImplementedError("Tehtävä 13")


class MLP:
    def __init__(self, n_in, koot):
        raise NotImplementedError("Tehtävä 13")

    def __call__(self, x):
        raise NotImplementedError("Tehtävä 13")

    def parameters(self):
        raise NotImplementedError("Tehtävä 13")


def kouluta(malli, xs, ys, kierrokset=100, oppimisnopeus=0.05):
    """Kouluttaa mallin. Palauttaa listan lossin arvoja, yksi per kierros."""
    raise NotImplementedError("Tehtävä 14")
