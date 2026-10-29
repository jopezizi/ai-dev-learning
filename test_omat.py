from laskin import lisaa_alv, veroton

def test_viiskymmentä():
    assert lisaa_alv(50) == 62.75

def test_veroton_viiskymmentä():
    assert veroton(62.75) == 50.0
