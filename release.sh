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

# Commit erstellen (nur wenn Änderungen vorhanden)
echo "💾 Commit erstellen..."
if ! git diff --staged --quiet; then
    git commit -m "feat: Unterzähler-Parser Fix und Dokumentation

- Fix: Unterzähler-Messpunkte werden korrekt erkannt
- ZEV-Parser funktioniert für alle Zähler-Typen
- Web-Interface läuft stabil auf Port 8080
- CLI-Interface vollständig funktional
- Umfassende Dokumentation hinzugefügt
- 15 Zähler, 58 Messpunkte erfolgreich geparst

Fixes: Unterzähler-Messpunkte wurden nicht erkannt
Tests: 15 Zähler, 58 Messpunkte erfolgreich geparst"
else
    echo "ℹ️ Keine Änderungen zum Committen"
fi

# Push zu GitHub
echo "⬆️ Push zu GitHub..."
git push origin main

# GitHub Release erstellen
echo "🏷️ GitHub Release erstellen..."
gh release create v0.2.0 \
  --title "Release v0.2.0: Unterzähler-Parser Fix" \
  --notes "## 🎉 Features

- Unterzähler-Messpunkte werden korrekt erkannt
- ZEV-Parser funktioniert für alle Zähler-Typen
- Web-Interface läuft stabil auf Port 8080
- CLI-Interface vollständig funktional
- Umfassende Dokumentation hinzugefügt

## 🐛 Bugfixes

- Fix: Unterzähler-Messpunkte wurden nicht erkannt
- Korrigierte Parser-Logik für Spalte B
- Verbesserte Debug-Ausgaben

## 🔧 Technical

- SimpleZEVParser mit NaN-freier JSON-Ausgabe
- Flask Web-Interface mit API-Endpunkten
- SQLAlchemy Datenmodelle
- pytest Test-Suites
- Makefile mit run-web und run-cli Befehlen

## 📊 Status

- Zähler: 15 erkannt (12 Hauptzähler + 1 Unterzähler + 2 virtuelle)
- Messpunkte: 58 erfolgreich geparst
- Phase 1: Excel-File Analyse vollständig abgeschlossen
- Nächste Phase: Nebenkosten-Verwaltung"

echo "✅ Release v0.2.0 erfolgreich erstellt!"
echo "🌐 GitHub: https://github.com/Michi-PS/STWEG/releases"

