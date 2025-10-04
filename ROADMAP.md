# Entwicklungs-Roadmap - STWEG Projekt

## Phase 1: Foundation & Excel-Analyse (Woche 1-2)

### Sprint 1.1: Projekt-Setup
- [x] Projektstruktur erstellen
- [ ] GitHub Repository anlegen
- [ ] TDD-Umgebung einrichten (pytest, etc.)
- [ ] Grundlegende Python-Dependencies definieren
- [ ] Git-Workflow mit Feature-Branches etablieren

### Sprint 1.2: Excel-Analyse Modul
- [ ] **US-001**: Excel-File Struktur Analyse
  - [ ] Excel-Reader implementieren (pandas/openpyxl)
  - [ ] Tabellenblatt-Erkennung
  - [ ] Spalten-Mapping
  - [ ] Datenstruktur-Dokumentation
- [ ] **US-002**: Datenvalidierung
  - [ ] Validierungsregeln definieren
  - [ ] Fehlerbehandlung implementieren
  - [ ] Test-Cases für verschiedene Excel-Formate

## Phase 2: Datenmodelle & Grundstrukturen (Woche 3-4)

### Sprint 2.1: Core Models
- [ ] Eigentümer-Datenmodell
- [ ] Messpunkt-Datenmodell
- [ ] Rechnungs-Datenmodell
- [ ] Verbrauchsdaten-Modell

### Sprint 2.2: Datenbank-Setup
- [ ] **US-011**: Datenbank-Integration
  - [ ] SQLite/PostgreSQL Setup
  - [ ] ORM (SQLAlchemy) Konfiguration
  - [ ] Migration-System
  - [ ] Backup-Strategie

## Phase 3: Stromkosten-Verwaltung (Woche 5-6)

### Sprint 3.1: Verbrauchsanalyse
- [ ] **US-003**: Messpunkte auswerten
  - [ ] Excel-Daten in Datenbank importieren
  - [ ] Verbrauchsdaten aggregieren
  - [ ] Zeitraum-Filter
  - [ ] Datenvalidierung

### Sprint 3.2: Kostenverteilung
- [ ] **US-004**: Stromkosten aufteilen
  - [ ] Proportional-Berechnung
  - [ ] Kosten-Mapping
  - [ ] Ergebnis-Validierung
  - [ ] Reporting

## Phase 4: Nebenkosten-Verwaltung (Woche 7-9)

### Sprint 4.1: PDF-Verarbeitung
- [ ] **US-005**: PDF-Rechnungen verwalten
  - [ ] PDF-Upload-Funktionalität
  - [ ] OCR/Text-Extraktion (PyPDF2/pdfplumber)
  - [ ] Rechnungsdaten-Parsing
  - [ ] Kategorisierung-Interface

### Sprint 4.2: Jahresrechnung
- [ ] **US-006**: Jahresrechnung erstellen
  - [ ] Daten-Aggregation
  - [ ] Kategorie-Management
  - [ ] Zeitraum-Auswahl
  - [ ] Export-Funktionen

### Sprint 4.3: Verteilungsschlüssel
- [ ] **US-007**: Kostenverteilung
  - [ ] Verteilungsschlüssel definieren
  - [ ] Berechnungs-Engine
  - [ ] Eigentümer-Anteile
  - [ ] Validierung

## Phase 5: Rechnungsstellung (Woche 10-11)

### Sprint 5.1: PDF-Generierung
- [ ] **US-008**: PDF-Rechnung generieren
  - [ ] Template-System (Jinja2)
  - [ ] PDF-Generierung (ReportLab/WeasyPrint)
  - [ ] Layout-Design
  - [ ] Daten-Integration

### Sprint 5.2: Versand-System
- [ ] **US-009**: Rechnungsversand
  - [ ] E-Mail-Konfiguration
  - [ ] Template-System
  - [ ] Versand-Logging
  - [ ] Fehlerbehandlung

## Phase 6: Web-Interface (Woche 12-14)

### Sprint 6.1: Frontend-Foundation
- [ ] **US-010**: Web-Interface
  - [ ] Flask/FastAPI Backend
  - [ ] HTML/CSS/JavaScript Frontend
  - [ ] Responsive Design
  - [ ] Upload-Funktionen

### Sprint 6.2: User Management
- [ ] **US-012**: Benutzer-Management
  - [ ] Authentifizierung
  - [ ] Rollen-System
  - [ ] Session-Management
  - [ ] Audit-Log

## Phase 7: Testing & Deployment (Woche 15-16)

### Sprint 7.1: Testing & QA
- [ ] Unit-Tests vervollständigen
- [ ] Integration-Tests
- [ ] End-to-End-Tests
- [ ] Performance-Tests
- [ ] Security-Tests

### Sprint 7.2: Deployment
- [ ] Docker-Containerisierung
- [ ] Production-Deployment
- [ ] Monitoring-Setup
- [ ] Backup-Strategie
- [ ] Dokumentation finalisieren

## Technologie-Stack

### Backend
- **Python 3.9+**
- **Flask/FastAPI** (Web-Framework)
- **SQLAlchemy** (ORM)
- **PostgreSQL/SQLite** (Datenbank)
- **Celery** (Background-Tasks)

### Frontend
- **HTML5/CSS3/JavaScript**
- **Bootstrap/Tailwind CSS**
- **Chart.js** (Datenvisualisierung)

### Data Processing
- **pandas** (Excel-Verarbeitung)
- **PyPDF2/pdfplumber** (PDF-Verarbeitung)
- **ReportLab/WeasyPrint** (PDF-Generierung)

### Testing
- **pytest** (Unit-Tests)
- **Selenium** (E2E-Tests)
- **Coverage.py** (Test-Coverage)

### DevOps
- **Git** (Versionskontrolle)
- **Docker** (Containerisierung)
- **GitHub Actions** (CI/CD)

## Meilensteine

- **M1 (Woche 2)**: Excel-Analyse funktional
- **M2 (Woche 4)**: Datenmodelle implementiert
- **M3 (Woche 6)**: Stromkosten-Verteilung funktional
- **M4 (Woche 9)**: Nebenkosten-Verwaltung vollständig
- **M5 (Woche 11)**: PDF-Rechnungsstellung funktional
- **M6 (Woche 14)**: Web-Interface vollständig
- **M7 (Woche 16)**: Production-Ready

## Risiken & Mitigation

### Technische Risiken
- **Excel-Format-Änderungen**: Robuste Parser mit Fallback-Optionen
- **PDF-Parsing-Schwierigkeiten**: Multiple OCR-Engines testen
- **Performance bei großen Datenmengen**: Paginierung und Caching

### Projektrisiken
- **Scope-Creep**: Klare Definition der MVP-Features
- **Zeitdruck**: Agile Entwicklung mit regelmäßigen Reviews
- **Datenqualität**: Frühe Validierung und Benutzer-Feedback

## Erfolgsmetriken

- **Funktionalität**: Alle User Stories erfolgreich implementiert
- **Qualität**: >90% Test-Coverage
- **Performance**: <2s Ladezeit für Standard-Operationen
- **Benutzerfreundlichkeit**: Positive Feedback von End-Usern
- **Wartbarkeit**: Saubere Code-Struktur und Dokumentation
