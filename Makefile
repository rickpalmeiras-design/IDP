PYTHON ?= python

.PHONY: all insumos dados estimacao resultados dissertacao teste
all: insumos dados estimacao resultados

insumos:
	$(PYTHON) scripts/00_ambiente.py
	$(PYTHON) scripts/01_dicionarios.py
	$(PYTHON) scripts/02_insumos.py

dados:
	$(PYTHON) scripts/03_cobertura_pnadc.py
	$(PYTHON) scripts/04_painel_pnadc.py

estimacao:
	$(PYTHON) scripts/05_estimacao.py

resultados:
	$(PYTHON) scripts/06_tabelas_figuras.py

dissertacao:
	$(PYTHON) scripts/06_dissertacao.py

teste:
	$(PYTHON) -m pytest -q
