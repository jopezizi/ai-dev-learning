"""Moduuli 1: automaattinen tarkistus. Älä muokkaa tätä tiedostoa.

Aja projektin juuressa:  uv run pytest moduuli1 -v

Epäonnistuneen testin viesti kertoo, mikä tehtävä on vielä kesken.
NotImplementedError tarkoittaa, että funktio on vielä pohja.
"""

import math
import random
from pathlib import Path

import pytest

from data import HAKEMUKSET, NELIOT, PAATOKSET, VUOKRAT

KANSIO = Path(__file__).parent
JUURI = KANSIO.parent


def derivaatta(f, x, h=1e-6):
    """Tarkistimen oma numeerinen derivaatta, jotta testit eivät nojaa sinun koodiisi."""
    return (f(x + h) - f(x - h)) / (2 * h)


# ---------- 1.1 Oppiminen on virheen pienentämistä ----------

def test_ennusta():
    from suora import ennusta
    assert ennusta(10, 2, 1) == 21
    assert ennusta(0, 5, 3) == 3, "Kun x on 0, ennusteen pitää olla b (tehtävä 4)"
    assert ennusta(50, 10, 320) == 820


def test_mse():
    from suora import mse
    assert mse([1, 2, 3], [1, 2, 3]) == 0, "Täydellisen ennusteen virhe on 0 (tehtävä 5)"
    assert mse([2, 4], [1, 1]) == 5.0, "(1² + 3²) / 2 = 5 (tehtävä 5)"
    assert mse([0], [-3]) == 9.0, "Virhe neliöidään, joten etumerkki ei vaikuta (tehtävä 5)"


def test_mse_eri_pituudet():
    from suora import mse
    with pytest.raises(ValueError):
        mse([1, 2, 3], [1, 2])


# ---------- 1.2 Kone arvaa itse ----------

def test_numeerinen_derivaatta():
    from gradientti import numeerinen_derivaatta
    assert numeerinen_derivaatta(lambda x: x ** 2, 3) == pytest.approx(6, abs=1e-4)
    assert numeerinen_derivaatta(lambda x: 5 * x + 2, 100) == pytest.approx(5, abs=1e-4)
    assert numeerinen_derivaatta(math.sin, 0) == pytest.approx(1, abs=1e-4)


def test_sovita_loytaa_suoran():
    from gradientti import sovita
    w, b, historia = sovita([0, 1, 2, 3, 4], [1, 3, 5, 7, 9], oppimisnopeus=0.05, kierrokset=1000)
    assert w == pytest.approx(2, abs=0.01), f"w pitäisi olla 2, oli {w} (tehtävä 8)"
    assert b == pytest.approx(1, abs=0.01), f"b pitäisi olla 1, oli {b} (tehtävä 8)"
    assert len(historia) == 1000, "historiassa pitää olla yksi loss jokaiselta kierrokselta (tehtävä 8)"
    assert historia[-1] < historia[0], "Lossin pitää pienentyä koulutuksen aikana (tehtävä 8)"


def test_sovita_skaalatulla_vuokradatalla():
    from gradientti import sovita
    xs = [n / 100 for n in NELIOT]
    w, b, historia = sovita(xs, VUOKRAT, oppimisnopeus=0.3, kierrokset=2000)
    assert historia[-1] < 51, f"Loss jäi arvoon {historia[-1]:.1f}, paras mahdollinen on noin 50,1 (tehtävä 9)"
    assert w / 100 == pytest.approx(10.27, abs=0.05), "Neliöhinnan pitäisi olla noin 10,27 €/m² (tehtävä 9)"


# ---------- 1.3 Oma autograd ----------

def test_value_laskee_arvon():
    from autograd import Value
    a, b, c = Value(2.0), Value(-3.0), Value(10.0)
    d = a * b + c
    assert d.data == 4.0, "2 * -3 + 10 = 4 (tehtävä 10)"
    assert a.grad == 0.0, "Gradientin pitää olla 0, ennen kuin backward() ajetaan (tehtävä 10)"


def test_backward_yksinkertainen():
    from autograd import Value
    a, b, c = Value(2.0), Value(-3.0), Value(10.0)
    d = a * b + c
    d.backward()
    assert d.grad == 1.0, "Lopputuloksen oma gradientti on aina 1 (tehtävä 11)"
    assert c.grad == 1.0, "Summassa gradientti kulkee sellaisenaan (tehtävä 11)"
    assert a.grad == -3.0, "a:n gradientti on b:n arvo (tehtävä 11)"
    assert b.grad == 2.0, "b:n gradientti on a:n arvo (tehtävä 11)"


def test_gradientit_kertyvat():
    from autograd import Value
    a = Value(3.0)
    y = a * a + a
    y.backward()
    assert a.grad == 7.0, (
        f"a:n gradientti oli {a.grad}, piti olla 2*3 + 1 = 7. "
        "Käytä += eikä =, kun sama arvo esiintyy monessa kohdassa (tehtävä 11)"
    )


def test_luvut_ja_lisaoperaatiot():
    from autograd import Value
    a = Value(4.0)
    y = 2 * a + 1 - a ** 2
    assert y.data == 2 * 4 + 1 - 16, "Laskut tavallisen luvun kanssa: 2*a, a+1, a-..., a**2 (tehtävä 12)"
    y.backward()
    assert a.grad == pytest.approx(2 - 2 * 4), "Derivaatta: 2 - 2a (tehtävä 12)"


def test_tanh():
    from autograd import Value
    x = Value(0.7)
    y = x.tanh()
    assert y.data == pytest.approx(math.tanh(0.7))
    y.backward()
    assert x.grad == pytest.approx(derivaatta(math.tanh, 0.7), abs=1e-6), "tanh:n gradientti on 1 - tanh² (tehtävä 12)"


def test_autograd_vs_numeerinen():
    from autograd import Value

    def tavallisilla_luvuilla(x):
        return math.tanh(x * 0.5 - 1) * x ** 3 + 2 * x

    for x0 in [-1.5, 0.3, 2.0]:
        v = Value(x0)
        y = (v * 0.5 - 1).tanh() * v ** 3 + 2 * v
        y.backward()
        odotettu = derivaatta(tavallisilla_luvuilla, x0)
        assert v.grad == pytest.approx(odotettu, rel=1e-5), f"Gradientti väärin kohdassa x = {x0} (tehtävä 12)"


# ---------- 1.4 Ensimmäinen neuroverkko ----------

def test_parametrien_maara():
    from verkko import MLP, Neuron
    assert len(Neuron(3).parameters()) == 4, "Neuronissa on painot jokaiselle syötteelle ja yksi bias (tehtävä 13)"
    assert len(MLP(2, [4, 4, 1]).parameters()) == 37, "(2*4+4) + (4*4+4) + (4+1) = 37 (tehtävä 13)"


def test_verkon_ulostulo():
    from autograd import Value
    from verkko import MLP
    random.seed(0)
    y = MLP(2, [4, 4, 1])([0.5, -0.2])
    assert isinstance(y, Value), "Yhden neuronin viimeinen kerros palauttaa yhden Valuen, ei listaa (tehtävä 13)"
    assert -1 < y.data < 1, "tanh-aktivaation jälkeen arvo on välillä -1 ja 1 (tehtävä 13)"


def test_kouluta_lainahakemukset():
    from verkko import MLP, kouluta
    random.seed(1)
    xs = [[tulot / 6, velat / 5] for tulot, velat in HAKEMUKSET]
    malli = MLP(2, [4, 4, 1])
    historia = kouluta(malli, xs, PAATOKSET, kierrokset=200, oppimisnopeus=0.05)
    assert len(historia) == 200, "historiassa pitää olla loss jokaiselta kierrokselta (tehtävä 14)"
    assert historia[-1] < historia[0] / 10, "Lossin pitäisi pudota alle kymmenesosaan (tehtävä 14)"
    oikein = sum((malli(x).data > 0) == (y > 0) for x, y in zip(xs, PAATOKSET))
    assert oikein == len(xs), f"Verkko luokitteli {oikein}/{len(xs)} oikein, tavoite on kaikki (tehtävä 14)"


# ---------- 1.5 Sama nopeasti: numpy ----------

def test_numpy_asennettu():
    pyproject = (JUURI / "pyproject.toml").read_text()
    assert "numpy" in pyproject, "Aja projektin juuressa: uv add numpy (tehtävä 16)"


def test_numpy_sama_tulos_kuin_omalla_verkolla():
    np = pytest.importorskip("numpy", reason="Aja ensin: uv add numpy (tehtävä 16)")
    from verkko import MLP
    from verkko_np import eteenpain, painot_mlpsta
    random.seed(2)
    malli = MLP(2, [4, 4, 1])
    painot = painot_mlpsta(malli)
    assert painot[0][0].shape == (2, 4), "Ensimmäisen kerroksen W:n muoto on (syötteet, neuronit) eli (2, 4) (tehtävä 17)"
    X = np.array([[t / 6, v / 5] for t, v in HAKEMUKSET])
    tulos = eteenpain(X, painot)
    assert tulos.shape[0] == len(HAKEMUKSET), "Jokaiselle hakemukselle yksi tulos (tehtävä 17)"
    odotettu = [malli(list(x)).data for x in X]
    assert np.allclose(np.ravel(tulos), odotettu), "numpy-verkon pitää antaa täsmälleen samat tulokset kuin Value-verkon (tehtävä 17)"


# ---------- 1.6 Päätös ----------

def test_omat_testit():
    tiedosto = KANSIO / "test_omat_m1.py"
    assert tiedosto.exists(), "moduuli1/test_omat_m1.py puuttuu (tehtävät 4-14)"
    sisalto = tiedosto.read_text()
    maara = sisalto.count("def test_")
    assert maara >= 8, f"Omia testejä on {maara}, tavoite on vähintään 8 (tehtävä 19)"
    for nimi in ["ennusta", "mse", "numeerinen_derivaatta", "Value", "MLP"]:
        assert nimi in sisalto, f"Omista testeistä puuttuu testi kohteelle {nimi} (tehtävä 19)"


def test_paivakirja_moduuli1():
    tiedosto = JUURI / "OPPIMISPAIVAKIRJA.md"
    assert tiedosto.exists(), "OPPIMISPAIVAKIRJA.md puuttuu projektin juuresta"
    assert "moduuli 1" in tiedosto.read_text().lower(), "Lisää päiväkirjaan osio Moduuli 1 (tehtävä 20)"
