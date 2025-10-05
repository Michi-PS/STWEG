# Entwicklungs-Roadmap - STWEG Projekt

## Phase 1: Foundation & Excel-Analyse (Woche 1-2) ✅ **ABGESCHLOSSEN**

### Sprint 1.1: Projekt-Setup ✅
- [x] Projektstruktur erstellen
- [x] GitHub Repository anlegen (https://github.com/Michi-PS/STWEG)
- [x] TDD-Umgebung einrichten (pytest, etc.)
- [x] Grundlegende Python-Dependencies definieren
- [x] Git-Workflow mit Feature-Branches etablieren

### Sprint 1.2: Excel-Analyse Modul ✅
- [x] **US-001**: Excel-File Struktur Analyse ✅
  - [x] Excel-Reader implementieren (pandas/openpyxl)
  - [x] Tabellenblatt-Erkennung
  - [x] Spalten-Mapping
  - [x] Datenstruktur-Dokumentation
  - [x] CLI-Interface für einfache Bedienung
  - [x] Vollständige Test-Suite (9 Tests, 100% Erfolg)
- [x] **US-002**: Datenvalidierung ✅
  - [x] Validierungsregeln definieren
  - [x] Fehlerbehandlung implementieren
  - [x] Test-Cases für verschiedene Excel-Formate
  - [x] Validierung gegen erwartete Formate

## Phase 2: Datenmodelle & Grundstrukturen (Woche 3-4) ✅ **ABGESCHLOSSEN**

### Sprint 2.1: Core Models ✅
- [x] Eigentümer-Datenmodell
- [x] Messpunkt-Datenmodell
- [x] Rechnungs-Datenmodell
- [x] Verbrauchsdaten-Modell

### Sprint 2.2: Datenbank-Setup ✅
- [x] **US-011**: Datenbank-Integration
  - [x] SQLite Setup
  - [x] ORM (SQLAlchemy) Konfiguration
  - [x] Session-Management
  - [x] Vollständige Test-Suite

## Phase 2.5: Testing & Validation (Woche 4) 🎯 **AKTUELL**

### Sprint 2.3: Datenbank-Tests
- [ ] **DB-TEST-001**: Vollständige Modell-Tests
  - [ ] pytest-Tests ausführen
  - [ ] Datenbank-CRUD-Operationen testen
  - [ ] Beziehungen zwischen Modellen validieren
  - [ ] Validierungsregeln testen

## Phase 3: UX & Visualisierung (Woche 5)

### Sprint 3.1: Web-Interface Foundation
- [ ] **US-013**: Erste Visualisierung
  - [ ] Flask/FastAPI Backend Setup
  - [ ] HTML/CSS Frontend-Grundlage
  - [ ] Dashboard mit aktueller Projektübersicht
  - [ ] Test-Status-Darstellung
  - [ ] Excel-Struktur-Visualisierung

### Sprint 3.2: Test-Dashboard
- [ ] **US-014**: Test-Status-Monitoring
  - [ ] Automatische Test-Ausführung
  - [ ] Test-Ergebnisse visualisieren
  - [ ] Code-Coverage anzeigen
  - [ ] Test-Historie verfolgen

## Phase 4: MVP Rechnungsstellung (Woche 6)

### Sprint 4.1: PDF-Generierung
- [ ] **US-015**: Erste PDF-Rechnung
  - [ ] Template-System für Rechnungen
  - [ ] PDF-Generierung mit ReportLab
  - [ ] Dummy-Daten für erste Tests
  - [ ] Rechnungsformat nach Vorgabe

### Sprint 4.2: Rechnungs-Interface
- [ ] **US-016**: Rechnungs-Management
  - [ ] Rechnung erstellen/verwalten
  - [ ] PDF-Vorschau
  - [ ] Rechnung herunterladen
  - [ ] Rechnungs-Templates verwalten

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
- **Python 3.13** ✅ (kompatibel mit allen Dependencies)
- **Flask/FastAPI** (Web-Framework)
- **SQLAlchemy** (ORM)
- **PostgreSQL/SQLite** (Datenbank)
- **Celery** (Background-Tasks)

### Frontend
- **HTML5/CSS3/JavaScript**
- **Bootstrap/Tailwind CSS**
- **Chart.js** (Datenvisualisierung)

### Data Processing
- **pandas 2.3.3** ✅ (Excel-Verarbeitung)
- **openpyxl 3.1.5** ✅ (Excel-Engine)
- **PyPDF2/pdfplumber** (PDF-Verarbeitung)
- **ReportLab/WeasyPrint** (PDF-Generierung)

### Testing
- **pytest 8.4.2** ✅ (Unit-Tests)
- **pytest-cov 7.0.0** ✅ (Coverage-Reports)
- **pytest-mock 3.15.1** ✅ (Mock-Testing)
- **Selenium** (E2E-Tests)

### DevOps
- **Git** ✅ (Versionskontrolle - Repository: https://github.com/Michi-PS/STWEG)
- **Docker** (Containerisierung)
- **GitHub Actions** (CI/CD)

## Meilensteine

- **M1 (Woche 2)**: Excel-Analyse funktional ✅ **ERREICHT**
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
- **Qualität**: >90% Test-Coverage ✅ (9/9 Tests bestanden, 100% Erfolg)
- **Performance**: <2s Ladezeit für Standard-Operationen
- **Benutzerfreundlichkeit**: Positive Feedback von End-Usern
- **Wartbarkeit**: Saubere Code-Struktur und Dokumentation

## Aktueller Status (Stand: Januar 2025)

### ✅ **Abgeschlossen:**
- **Phase 1**: Foundation & Excel-Analyse (100%)
- **User Stories**: US-001, US-002 (Excel-Analyse und Validierung)
- **Test-Coverage**: 9 Tests, 100% Erfolg
- **Technologie-Stack**: Python 3.13, pandas 2.3.3, pytest 8.4.2
- **Repository**: GitHub Repository erstellt und funktional

### 🎯 **Nächste Schritte:**
- **Phase 2.5**: Datenbank-Tests validieren ✅ **AKTUELL**
- **Phase 3**: UX & Visualisierung (Dashboard, Test-Status)
- **Phase 4**: MVP Rechnungsstellung (PDF-Generierung)
- **Phase 5**: Excel-Struktur-Analyse Integration
