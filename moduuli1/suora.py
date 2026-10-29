"""Osa 1.1: suora malli ja sen virhe."""


def ennusta(x, w, b):
    """Palauttaa suoran mallin ennusteen: w * x + b.

    w (paino) kertoo, kuinka paljon ennuste kasvaa, kun x kasvaa yhdellä.
    b (bias) on ennuste, kun x on 0.
    """
    raise NotImplementedError("Tehtävä 4")


def mse(ennusteet, oikeat):
    """Mean squared error: virheiden neliöiden keskiarvo.

    Jokaiselle parille lasketaan (ennuste - oikea)², ja tuloksista otetaan keskiarvo.
    Jos listat ovat eri pituisia, nostaa ValueErrorin.
    """
    raise NotImplementedError("Tehtävä 5")
