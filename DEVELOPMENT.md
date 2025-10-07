# STWEG - Entwickler-Dokumentation

## 🚀 App starten

### Schnellstart
```bash
cd /Users/rechberger/Documents/Coding/STWEG
source venv/bin/activate
python -c "
import sys
sys.path.insert(0, 'src')
from web.app import app
app.run(debug=True, host='0.0.0.0', port=8080)
"
```

### Detaillierte Schritte

1. **Projektverzeichnis wechseln:**
   ```bash
   cd /Users/rechberger/Documents/Coding/STWEG
   ```

2. **Virtual Environment aktivieren:**
   ```bash
   source venv/bin/activate
   ```

3. **Web-App starten:**
   ```bash
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

## 🔧 Technische Details

### Port-Konfiguration
- **Standard-Port:** 8080 (nicht 5000!)
- **Grund:** Port 5000 ist auf macOS durch AirPlay Receiver belegt
- **Alternative Ports:** 8081, 8082, 3000, 8000

### Projektstruktur
```
STWEG/
├── src/
│   ├── web/app.py          # Flask Web-Interface
│   ├── cli.py              # Command Line Interface
│   ├── excel_analysis/     # Excel-Parser Module
│   └── models/             # Datenmodelle
├── tests/                  # Test-Suites
├── data/                   # Upload/Export Verzeichnisse
└── venv/                   # Virtual Environment
```

### Verfügbare Module
- **Web-App:** `src/web/app.py` - Flask-Interface mit Dashboard
- **CLI:** `src/cli.py` - Command Line Interface
- **ZEV-Parser:** `src/excel_analysis/simple_zev_parser.py` - Excel-Analyse
- **Datenmodelle:** `src/models/` - SQLAlchemy-Modelle

### API-Endpunkte
- `GET /` - Dashboard
- `GET /api/status` - Projektstatus
- `GET /api/tests` - Test-Status
- `POST /api/excel/upload` - Excel-Upload
- `GET /api/excel/analyze/<filename>` - Excel-Analyse
- `GET /api/excel/explore/<filename>` - ZEV-Exploration

### CLI-Befehle
```bash
python src/cli.py --help
python src/cli.py analyze datei.xlsx --report
python src/cli.py validate datei.xlsx
```

## 🐛 Bekannte Probleme

### Port 5000 belegt
**Problem:** `Address already in use - Port 5000 is in use by another program`
**Lösung:** Port 8080 verwenden (siehe Start-Befehle oben)

### Import-Fehler
**Problem:** Module nicht gefunden
**Lösung:** `sys.path.insert(0, 'src')` vor Imports verwenden

### Virtual Environment
**Problem:** Dependencies nicht gefunden
**Lösung:** `source venv/bin/activate` ausführen

## 📊 Aktueller Status

### Implementierte Features
- ✅ Web-Interface (Flask)
- ✅ CLI-Interface
- ✅ ZEV-Excel-Parser (NaN-frei)
- ✅ Datenbank-Modelle (SQLAlchemy)
- ✅ Test-Suites (pytest)
- ✅ API-Endpunkte

### Datenbank-Status
- **Eigentümer:** 7 (alle aktiv)
- **Messpunkte:** 15+ (alle ZEV-Zähler erkannt)
- **Verbrauchsdaten:** Vollständig (alle Monate für alle Zähler)
- **Rechnungen:** 0 (bereit für PDF-Generierung)

### Entwicklungsphase
- **Aktuell:** Phase 5 - PDF-Rechnungsstellung (bereit zu starten)
- **Abgeschlossen:** Phase 4 - ZEV-Parser (100% funktional)
- **Nächste:** PDF-Rechnung-Erstellung & Kostenverteilung

## 🔍 Debugging

### Logs anzeigen
Die Flask-App läuft im Debug-Modus und zeigt detaillierte Logs in der Konsole.

### API testen
```bash
curl http://localhost:8080/api/status
curl http://localhost:8080/api/tests
```

### Tests ausführen
```bash
pytest tests/ -v
pytest tests/ --cov=src --cov-report=html
```

## 📝 Notizen für zukünftige Sessions

1. **App immer auf Port 8080 starten** (nicht 5000)
2. **Virtual Environment aktivieren** vor jedem Start
3. **sys.path.insert(0, 'src')** für Module-Imports
4. **Web-App läuft im Hintergrund** - nicht vergessen zu stoppen
5. **API-Endpunkte** sind vollständig funktional
6. **ZEV-Parser** ist 100% funktional - alle 15 Zähler und Messpunkte erkannt
