"""Moduuli 0: automaattinen tarkistus.

Aja projektikansiossa komennolla:  uv run pytest -v

Jokainen testi vastaa yhtä tai useampaa tehtävää. Epäonnistuneen testin
viesti kertoo, mikä tehtävä on vielä kesken.
"""

import subprocess
import sys
from pathlib import Path

JUURI = Path(__file__).parent


def git(*args):
    """Ajaa git-komennon projektikansiossa ja palauttaa sen tulosteen."""
    tulos = subprocess.run(["git", *args], cwd=JUURI, capture_output=True, text=True)
    return tulos.stdout.strip()


# ---------- 0.3 Git ja GitHub ----------

def test_readme_on_olemassa():
    readme = JUURI / "README.md"
    assert readme.exists(), "README.md puuttuu (tehtävä 7)"
    rivit = [r for r in readme.read_text().splitlines() if r.strip()]
    assert len(rivit) >= 2, "README.md:ssä pitäisi olla vähintään 2 riviä (tehtävä 9)"


def test_repo_on_yhdistetty_githubiin():
    osoite = git("remote", "get-url", "origin")
    assert "github.com" in osoite, "Repoa ei ole yhdistetty GitHubiin (tehtävä 8)"


def test_vahintaan_viisi_commitia():
    maara = int(git("rev-list", "--count", "HEAD") or 0)
    assert maara >= 5, f"Commiteja on {maara}, tavoite on vähintään 5"


def test_kaikki_muutokset_on_tallennettu():
    kesken = git("status", "--porcelain")
    assert kesken == "", f"Tallentamattomia muutoksia:\n{kesken}\nTee git add ja git commit."


def test_kaikki_on_lahetetty_githubiin():
    tila = git("status", "--porcelain=v2", "--branch")
    rivi = next((r for r in tila.splitlines() if r.startswith("# branch.ab")), None)
    assert rivi is not None, "Haaraa ei ole yhdistetty GitHubiin (tehtävä 8)"
    assert rivi == "# branch.ab +0 -0", f"Koneesi ja GitHub eroavat ({rivi}). Aja git push."


# ---------- 0.4 Python-projekti ----------

def test_python_versio_on_kiinnitetty():
    tiedosto = JUURI / ".python-version"
    assert tiedosto.exists(), ".python-version puuttuu (tehtävä 10: uv python pin)"
    paa, ala = map(int, tiedosto.read_text().strip().split(".")[:2])
    assert (paa, ala) >= (3, 11), "Python-version pitää olla vähintään 3.11"


def test_testit_ajetaan_projektin_omalla_pythonilla():
    assert ".venv" in sys.prefix, "Aja testit komennolla: uv run pytest -v"


def test_gitignore_suojaa_oikeat_asiat():
    tiedosto = JUURI / ".gitignore"
    assert tiedosto.exists(), ".gitignore puuttuu (tehtävä 11)"
    sisalto = tiedosto.read_text()
    for kohta in [".venv", ".env"]:
        assert kohta in sisalto, f"{kohta} puuttuu .gitignoresta (tehtävä 11)"


def test_virtuaaliymparisto_ei_ole_gitissa():
    assert ".venv/" not in git("ls-files"), ".venv on päätynyt gittiin, katso tehtävä 11"


def test_lisaa_alv():
    from laskin import lisaa_alv
    assert lisaa_alv(100) == 125.5
    assert lisaa_alv(0) == 0
    assert lisaa_alv(10, 0.14) == 11.4, "Toisen parametrin pitää vaihtaa verokanta"


# ---------- 0.5 Automaattinen tarkistus ----------

def test_pytest_on_kehitysriippuvuutena():
    assert "pytest" in (JUURI / "pyproject.toml").read_text(), "Aja: uv add --dev pytest (tehtävä 14)"
    assert (JUURI / "uv.lock").exists(), "uv.lock puuttuu (tehtävä 14)"


def test_omat_testit_on_kirjoitettu():
    tiedosto = JUURI / "test_omat.py"
    assert tiedosto.exists(), "test_omat.py puuttuu (tehtävä 16)"
    assert "def test_" in tiedosto.read_text(), "test_omat.py:ssä ei ole yhtään testifunktiota"


# ---------- 0.6 Claude Code ----------

def test_claude_md_on_tehty():
    tiedosto = JUURI / "CLAUDE.md"
    assert tiedosto.exists(), "CLAUDE.md puuttuu (tehtävä 18: /init)"
    sisalto = tiedosto.read_text().lower()
    assert "suomeksi" in sisalto, "Lisää omat työskentelyohjeesi CLAUDE.md:hen (tehtävä 18)"
    assert "pytest" in sisalto, "Lisää CLAUDE.md:hen ohje ajaa testit (tehtävä 18)"


def test_veroton():
    import laskin
    assert hasattr(laskin, "veroton"), "veroton() puuttuu (tehtävä 20, Claude Code tekee tämän)"
    assert laskin.veroton(125.5) == 100.0
    assert laskin.veroton(11.4, 0.14) == 10.0


def test_alv_edestakaisin():
    from laskin import lisaa_alv, veroton
    for hinta in [1.0, 19.99, 250.0, 1234.56]:
        assert veroton(lisaa_alv(hinta)) == hinta, f"veroton(lisaa_alv({hinta})) ei palauta {hinta}"


# ---------- 0.7 Päätös ----------

def test_oppimispaivakirja():
    tiedosto = JUURI / "OPPIMISPAIVAKIRJA.md"
    assert tiedosto.exists(), "OPPIMISPAIVAKIRJA.md puuttuu (tehtävä 23)"
    rivit = [r for r in tiedosto.read_text().splitlines() if r.strip()]
    assert len(rivit) >= 4, "Kirjoita päiväkirjaan vähintään 4 riviä (tehtävä 23)"
