# STWEG - Quick Start Guide

## 🚀 App sofort starten

```bash
cd /Users/rechberger/Documents/Coding/STWEG
source venv/bin/activate
make run-web
```

**Oder direkt:**
```bash
cd /Users/rechberger/Documents/Coding/STWEG
source venv/bin/activate
python -c "import sys; sys.path.insert(0, 'src'); from web.app import app; app.run(debug=True, host='0.0.0.0', port=8080)"
```

## 🌐 URLs
- **Dashboard:** http://localhost:8080
- **API-Status:** http://localhost:8080/api/status

## ⚠️ Wichtige Hinweise
- **Port 8080 verwenden** (nicht 5000 - macOS AirPlay Problem)
- **Virtual Environment aktivieren** vor jedem Start
- **App läuft im Hintergrund** - mit Ctrl+C stoppen

## 📁 Projekt-Status
- ✅ Web-Interface funktioniert
- ✅ CLI funktioniert  
- ✅ ZEV-Parser implementiert
- ✅ Datenbank mit 7 Eigentümern
- ✅ API-Endpunkte verfügbar

## 🔧 Weitere Befehle
```bash
make run-cli      # CLI testen
make test         # Tests ausführen
make help         # Alle Befehle anzeigen
```
