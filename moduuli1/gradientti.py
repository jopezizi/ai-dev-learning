"""Osa 1.2: kone etsii parhaat parametrit itse."""

from suora import ennusta, mse


def numeerinen_derivaatta(f, x, h=1e-5):
    """Kuinka paljon f(x) muuttuu, kun x:ää tökätään vähän.

    Laske f vähän x:n oikealta ja vasemmalta puolelta ja jaa erotus välimatkalla 2h.
    """
    raise NotImplementedError("Tehtävä 7")


def sovita(xs, ys, oppimisnopeus=0.01, kierrokset=1000):
    """Etsii suoralle parametrit w ja b gradient descentillä.

    Aloita arvoista w = 0 ja b = 0. Joka kierroksella:
      1. laske nykyinen loss ja lisää se historiaan
      2. laske lossin derivaatta w:n suhteen ja b:n suhteen
      3. siirrä w:tä ja b:tä vähän derivaatan vastakkaiseen suuntaan

    Palauttaa (w, b, historia), jossa historia on lista lossin arvoja, yksi per kierros.
    """
    raise NotImplementedError("Tehtävä 8")
