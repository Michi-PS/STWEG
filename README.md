# STWEG - Stockwerkeigentümergesellschaft Nebenkostenverwaltung

## Projektübersicht

Diese Anwendung dient der Verwaltung und Abrechnung der Nebenkosten für eine Stockwerkeigentümergesellschaft mit 7 Eigentümern.

## Hauptfunktionen

### 1. Stromkosten-Aufteilung
- Auswertung der Messpunkte vom Elektrizitätswerk
- Automatische Aufteilung der Stromkosten basierend auf Verbrauchsdaten
- Integration mit ZEV-Server Daten

### 2. Nebenkosten-Verwaltung
- Verwaltung aller sonstigen Nebenkosten (PDF-Rechnungen)
- Erstellung von Jahresrechnungen
- Verteilung nach definierten Schlüsseln

### 3. Rechnungsstellung
- Automatische Erstellung von PDF-Rechnungen
- Versand an alle Eigentümer

## Technische Anforderungen

- Test-Driven Development (TDD)
- Lokale Entwicklung mit späterer Web-Service Option
- Git-basierte Versionskontrolle mit Rollback-Möglichkeiten
- Python-basierte Entwicklung

## Projektstruktur

```
STWEG/
├── src/
│   ├── excel_analysis/     # Excel-File Analyse Modul
│   ├── cost_management/    # Nebenkosten-Verwaltung
│   ├── billing/           # Rechnungsstellung
│   └── models/            # Datenmodelle
├── tests/                 # Test-Dateien
├── docs/                  # Dokumentation
└── data/                  # Eingabedateien (Excel, PDFs)
```

## 🚀 App starten

### Web-Interface (Empfohlen)
```bash
cd /Users/rechberger/Documents/Coding/STWEG
source venv/bin/activate
python -c "
import sys
sys.path.insert(0, 'src')
from web.app import app
print('🚀 STWEG Web-Interface startet auf Port 8080...')
print('🌐 Dashboard: http://localhost:8080')
print('📊 API-Status: http://localhost:8080/api/status')
app.run(debug=True, host='0.0.0.0', port=8080)
"
```

**Wichtig:** Port 5000 ist auf macOS durch AirPlay Receiver belegt, daher Port 8080 verwenden.

### CLI verwenden
```bash
cd /Users/rechberger/Documents/Coding/STWEG
source venv/bin/activate
python src/cli.py --help
python src/cli.py analyze datei.xlsx --report
```

### Verfügbare URLs
- **Dashboard:** http://localhost:8080
- **API-Status:** http://localhost:8080/api/status
- **API-Tests:** http://localhost:8080/api/tests

## Entwicklungsphasen

1. **Phase 1**: Excel-File Analyse Modul ✅
2. **Phase 2**: Grundlegende Datenstrukturen ✅
3. **Phase 3**: Web-Interface & Dashboard ✅
4. **Phase 4**: ZEV-Parser & Stromkosten-Aufteilung ✅ (100% funktional)
5. **Phase 5**: PDF-Rechnungsstellung (bereit zu starten)
6. **Phase 6**: Nebenkosten-Verwaltung

