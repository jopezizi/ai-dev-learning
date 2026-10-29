# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Finnish self-learning course project ("Moduuli 0"). The code is a tiny VAT (ALV) calculator in `laskin.py`; the real driver is `test_moduuli0.py`, an auto-grader whose failing tests name the course task (`tehtävä N`) still unfinished. Identifiers, comments and test messages are in Finnish.

## Commands

Uses `uv` with Python 3.12 (pinned in `.python-version`); pytest is a dev dependency.

```sh
uv run pytest -v                                   # all tests (must go through uv: a test asserts .venv is the interpreter)
uv run pytest test_omat.py -v                      # learner's own tests
uv run pytest test_moduuli0.py::test_lisaa_alv -v  # single test
uv run python laskin.py                            # run the calculator
```

## How the grader works

- `test_moduuli0.py` is the course's fixed checker; do not edit it to make tests pass.
- Many tests check repo state, not code: clean working tree, ≥5 commits, `origin` on GitHub, branch pushed with no ahead/behind. These fail on any uncommitted change, so a red run right after editing is expected until commit + push.
- Other tests require files the learner creates: `README.md` (≥2 non-empty lines), `test_omat.py`, `CLAUDE.md` (must contain "suomeksi" and "pytest"), `OPPIMISPAIVAKIRJA.md` (≥4 lines).
- `laskin.py` API expected by the tests:
  - `lisaa_alv(netto, kanta=alv)` adds VAT at rate `kanta` (default 0.255), rounded.
  - `veroton(brutto, kanta=alv)` removes VAT; `veroton(lisaa_alv(x)) == x` must hold for typical prices.
- `laskin.py` has a module-level `print(...)`, so importing it in tests prints output.

## Työskentelytapa
- Vastaa suomeksi, tekniset termit englanniksi.
- Selitä jokainen uusi termi lyhyesti, kun käytät sitä ensimmäisen kerran.
- Aja testit (uv run pytest) jokaisen muutoksen jälkeen ja kerro tulos.
