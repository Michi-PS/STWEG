#!/bin/bash

# STWEG Release Script
# Automatisiert Git Commit, Push und GitHub Release

set -e  # Exit on any error

echo "🚀 STWEG Release Script startet..."

# Prüfen ob wir im richtigen Verzeichnis sind
if [ ! -f "README.md" ]; then
    echo "❌ Fehler: Bitte im STWEG Projektverzeichnis ausführen"
    exit 1
fi

# Git Status prüfen
echo "📋 Git Status prüfen..."
git status

# Alle Änderungen hinzufügen
echo "📁 Alle Änderungen hinzufügen..."
git add .

# Commit erstellen
echo "💾 Commit erstellen..."
git commit -m "feat: Phase 3 UX & Visualisierung abgeschlossen

- Web-Dashboard mit Flask implementiert
- Test-Monitoring mit Live-Status  
- Excel-Struktur-Visualisierung
- Test-Button Debugging und Reparatur
- Responsive Design mit Bootstrap
- API-Endpunkte für Status und Tests
- JavaScript-Frontend mit AJAX
- Fix: test-status Element Sichtbarkeit
- Fix: Spinner stoppt nach Test-Abschluss

Fixes: Frontend Test-Button funktioniert jetzt korrekt
Tests: 24 passed, 0 failed
Status: Phase 3 vollständig abgeschlossen"

# Push zu GitHub
echo "⬆️ Push zu GitHub..."
git push origin main

# GitHub Release erstellen
echo "🏷️ GitHub Release erstellen..."
gh release create v0.3.0 \
  --title "Release v0.3.0: UX & Visualisierung" \
  --notes "## 🎉 Features

- Web-Dashboard mit Test-Monitoring
- Excel-Struktur-Visualisierung  
- Responsive UI mit Bootstrap
- Live Test-Status Updates

## 🐛 Bugfixes

- Test-Button Frontend-Integration
- Spinner-Anzeige korrigiert
- API-Test-Parsing repariert

## 🔧 Technical

- Flask Web-Interface
- SQLAlchemy Models
- pytest Integration
- JavaScript Dashboard

## 📊 Status

- Tests: 24 passed, 0 failed
- Phase 3: Vollständig abgeschlossen
- Nächste Phase: PDF Rechnungsstellung"

echo "✅ Release v0.3.0 erfolgreich erstellt!"
echo "🌐 GitHub: https://github.com/Michi-PS/STWEG/releases"
