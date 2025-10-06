# STWEG - Stockwerkeigentümergesellschaft Nebenkostenverwaltung
# Makefile für Entwicklung

.PHONY: help install test test-cov lint format clean setup-data run-analyzer run-web run-cli

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
	@echo "  run-web     - Web-App starten (Port 8080)"
	@echo "  run-cli     - CLI testen"

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

# Web-App starten
run-web:
	python -c "import sys; sys.path.insert(0, 'src'); from web.app import app; print('🚀 STWEG Web-Interface startet auf Port 8080...'); print('🌐 Dashboard: http://localhost:8080'); app.run(debug=True, host='0.0.0.0', port=8080)"

# CLI testen
run-cli:
	python src/cli.py --help

# Entwicklungsumgebung einrichten
setup: install setup-data
	@echo "Entwicklungsumgebung eingerichtet!"
	@echo "Führen Sie 'make test' aus, um die Tests zu starten"

