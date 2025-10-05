# STWEG - Stockwerkeigentümergesellschaft Nebenkostenverwaltung
# Makefile für Entwicklung

.PHONY: help install test test-cov lint format clean setup-data run-analyzer

# Standardziel
help:
	@echo "STWEG - Verfügbare Befehle:"
	@echo "  install     - Dependencies installieren"
	@echo "  test        - Tests ausführen"
	@echo "  test-cov    - Tests mit Coverage ausführen"
	@echo "  lint        - Code-Qualität prüfen"
	@echo "  format      - Code formatieren"
	@echo "  clean       - Temporäre Dateien löschen"
	@echo "  setup-data  - Test-Daten erstellen"
	@echo "  run-analyzer - Excel-Analyzer testen"

# Dependencies installieren
install:
	pip install -r requirements.txt

# Tests ausführen
test:
	pytest tests/ -v

# Tests mit Coverage
test-cov:
	pytest tests/ --cov=src --cov-report=html --cov-report=term

# Code-Qualität prüfen
lint:
	flake8 src/ tests/
	mypy src/

# Code formatieren
format:
	black src/ tests/
	isort src/ tests/

# Temporäre Dateien löschen
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

# Test-Daten erstellen
setup-data:
	python create_test_data.py

# Excel-Analyzer testen
run-analyzer:
	python src/cli.py analyze data/sample/test_data.xlsx --report

# Entwicklungsumgebung einrichten
setup: install setup-data
	@echo "Entwicklungsumgebung eingerichtet!"
	@echo "Führen Sie 'make test' aus, um die Tests zu starten"
