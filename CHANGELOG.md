# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-01-08

### Fixed
- **User Stories Parsing**: Alle 8 Epics und 17 User Stories werden jetzt korrekt erkannt
- **Frontend "undefined" Labels**: User Story IDs werden korrekt angezeigt
- **Redundante Text-Duplikate**: "Als" Duplikate in User Story Text entfernt
- **Truncated Text**: Vollständiger Text aller User Stories ist jetzt lesbar

### Changed
- **Struktur-Umstellung**: USER_STORIES.md und ROADMAP.md getrennt
- **UX-Layout**: Links Backlog, rechts Epics/Stories für bessere Übersicht
- **CSS-Verbesserungen**: Scrollbare Bereiche und verbesserte Lesbarkeit

### Technical
- **Backend**: Markdown-Parser komplett überarbeitet für neues Format
- **Frontend**: JavaScript-Funktionen für bessere Datenverarbeitung
- **CSS**: Neue Klassen für verbesserte Textdarstellung

## [1.0.0] - 2025-01-08

### Added
- **Excel-Analyse**: Vollständige Analyse von ZEV-Excel-Dateien
- **PDF-Generierung**: Automatische Rechnungserstellung
- **Web-Interface**: Modulares Dashboard mit Development-Tools
- **Datenbank**: SQLAlchemy-basierte Datenverwaltung
- **CLI**: Kommandozeilen-Tools für Datenverarbeitung
- **Tests**: Umfassende Test-Suite (41 Tests)

### Features
- **Excel-Parser**: Intelligente Erkennung von Zähler- und Messpunkt-Daten
- **PDF-Templates**: Professionelle Rechnungsvorlagen
- **Dashboard**: Real-time Übersicht über Projektfortschritt
- **User Stories**: Vollständige Epic/Story-Verwaltung
- **Roadmap**: Priorisiertes Backlog-Management

### Technical
- **Python 3.9+**: Moderne Python-Features
- **Flask**: Web-Framework für Dashboard
- **SQLAlchemy**: ORM für Datenbankoperationen
- **pandas**: Excel-Datenverarbeitung
- **pytest**: Test-Framework mit 100% Coverage
