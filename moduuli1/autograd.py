"""Osa 1.3: oma automaattinen derivointi.

Value on luku, joka muistaa mistä se laskettiin, ja osaa siksi laskea
derivaattansa kaikkien niiden lukujen suhteen, joista se syntyi.
"""

import math


class Value:
    def __init__(self, data, _lapset=()):
        self.data = data            # itse luku
        self.grad = 0.0             # lopputuloksen derivaatta tämän luvun suhteen
        self._lapset = set(_lapset) # Valuet, joista tämä laskettiin
        self._backward = lambda: None  # funktio, joka vie gradientin lapsille

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"

    def __add__(self, other):
        raise NotImplementedError("Tehtävä 10")

    def __mul__(self, other):
        raise NotImplementedError("Tehtävä 10")

    def backward(self):
        raise NotImplementedError("Tehtävä 11")

    # Tehtävä 12: __pow__, tanh, __neg__, __sub__, __radd__, __rmul__, __rsub__
