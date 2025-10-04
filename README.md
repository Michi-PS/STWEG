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

## Entwicklungsphasen

1. **Phase 1**: Excel-File Analyse Modul
2. **Phase 2**: Grundlegende Datenstrukturen
3. **Phase 3**: Stromkosten-Aufteilung
4. **Phase 4**: Nebenkosten-Verwaltung
5. **Phase 5**: PDF-Rechnungsstellung
6. **Phase 6**: Web-Interface (optional)
