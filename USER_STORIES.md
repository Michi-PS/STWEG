# User Stories - STWEG Nebenkostenverwaltung

## Epic 1: Excel-File Analyse und Datenverarbeitung

**Beschreibung:** Analyse und Verarbeitung von Excel-Dateien vom ZEV-Server für die Extraktion von Verbrauchsdaten und Strukturinformationen.

### US-001: Excel-File Struktur Analyse
**Als** Administrator der Stockwerkeigentümergesellschaft  
**möchte ich** die Struktur des Excel-Files vom ZEV-Server analysieren  
**damit** ich verstehe, welche Daten verfügbar sind und wie sie strukturiert sind.

**Akzeptanzkriterien:**
- [x] Excel-File kann geladen und gelesen werden
- [x] Alle Tabellenblätter werden identifiziert
- [x] Spaltenüberschriften werden extrahiert
- [x] Datenstruktur wird dokumentiert
- [x] Beispiel-Daten werden angezeigt

### US-002: Datenvalidierung
**Als** Administrator  
**möchte ich** die Excel-Daten validieren  
**damit** ich sicherstellen kann, dass alle notwendigen Informationen vorhanden sind.

**Akzeptanzkriterien:**
- [x] Überprüfung auf fehlende Spalten
- [x] Überprüfung auf leere oder ungültige Werte
- [x] Validierung der Datenformate
- [x] Fehlerbericht bei Problemen

---

## Epic 2: Stromkosten-Verwaltung

**Beschreibung:** Auswertung und Aufteilung der Stromkosten basierend auf Verbrauchsdaten der einzelnen Messpunkte.

### US-003: Messpunkte auswerten
**Als** Administrator  
**möchte ich** die Verbrauchsdaten der einzelnen Messpunkte auswerten  
**damit** ich den Stromverbrauch pro Eigentümer berechnen kann.

**Akzeptanzkriterien:**
- [ ] Gesamtverbrauch wird extrahiert
- [ ] Einzelne Messpunkte werden identifiziert
- [ ] Verbrauchsdaten werden korrekt zugeordnet
- [ ] Zeiträume werden berücksichtigt

### US-004: Stromkosten aufteilen
**Als** Administrator  
**möchte ich** die Stromkosten proportional zum Verbrauch aufteilen  
**damit** jeder Eigentümer nur seinen Anteil zahlt.

**Akzeptanzkriterien:**
- [ ] Gesamtkosten werden auf Verbrauch umgelegt
- [ ] Proportionalberechnung ist korrekt
- [ ] Ergebnisse werden dokumentiert
- [ ] Aufschlüsselung nach Zeiträumen

---

## Epic 3: Nebenkosten-Verwaltung

**Beschreibung:** Verwaltung aller sonstigen Nebenkosten durch PDF-Rechnungen, Jahresrechnungen und Kostenverteilung.

### US-005: PDF-Rechnungen verwalten
**Als** Administrator  
**möchte ich** PDF-Rechnungen einlesen und kategorisieren  
**damit** ich alle Nebenkosten übersichtlich verwalten kann.

**Akzeptanzkriterien:**
- [ ] PDF-Rechnungen können hochgeladen werden
- [ ] Rechnungsdaten werden extrahiert
- [ ] Kategorisierung ist möglich
- [ ] Rechnungen können editiert werden

### US-006: Jahresrechnung erstellen
**Als** Administrator  
**möchte ich** eine Übersicht aller Nebenkosten für das Jahr erstellen  
**damit** ich eine vollständige Abrechnung habe.

**Akzeptanzkriterien:**
- [ ] Alle Rechnungen werden aggregiert
- [ ] Kategorien werden aufgelistet
- [ ] Gesamtbeträge werden berechnet
- [ ] Zeitraum kann gewählt werden

### US-007: Kostenverteilung
**Als** Administrator  
**möchte ich** die Nebenkosten nach definierten Schlüsseln verteilen  
**damit** jeder Eigentümer seinen Anteil kennt.

**Akzeptanzkriterien:**
- [ ] Verschiedene Verteilungsschlüssel verfügbar
- [ ] Anteile werden berechnet
- [ ] Eigentümer-spezifische Aufschlüsselung
- [ ] Nachvollziehbare Berechnung

---

## Epic 4: Rechnungsstellung

**Beschreibung:** Generierung und Versand von individuellen PDF-Rechnungen an alle Eigentümer.

### US-008: PDF-Rechnung generieren
**Als** Administrator  
**möchte ich** individuelle Rechnungen als PDF generieren  
**damit** ich sie an die Eigentümer versenden kann.

**Akzeptanzkriterien:**
- [ ] Rechnung im PDF-Format
- [ ] Eigentümer-spezifische Daten
- [ ] Vollständige Kostenaufschlüsselung
- [ ] Professionelles Layout

### US-009: Rechnungsversand
**Als** Administrator  
**möchte ich** Rechnungen per E-Mail versenden  
**damit** die Eigentümer ihre Rechnungen erhalten.

**Akzeptanzkriterien:**
- [ ] E-Mail-Versand funktioniert
- [ ] PDF-Anhang ist korrekt
- [ ] E-Mail-Template ist professionell
- [ ] Versandbestätigung

---

## Epic 5: Benutzeroberfläche

**Beschreibung:** Benutzerfreundliche Web-Oberfläche für alle administrativen Funktionen.

### US-010: Web-Interface
**Als** Administrator  
**möchte ich** eine benutzerfreundliche Web-Oberfläche  
**damit** ich alle Funktionen einfach bedienen kann.

**Akzeptanzkriterien:**
- [x] Intuitive Navigation
- [x] Responsive Design
- [x] Upload-Funktionen
- [x] Übersichtliche Darstellung der Daten

---

## Epic 6: System-Management

**Beschreibung:** Datenbank-Integration und Benutzer-Management für sichere und kontrollierte Systemnutzung.

### US-011: Datenbank-Integration
**Als** Administrator  
**möchte ich** alle Daten in einer Datenbank speichern  
**damit** ich historische Daten abfragen und verwalten kann.

**Akzeptanzkriterien:**
- [x] Datenbank-Schema ist definiert
- [x] CRUD-Operationen funktionieren
- [x] Datenintegrität ist gewährleistet
- [ ] Backup-Funktionen

### US-012: Benutzer-Management
**Als** Administrator  
**möchte ich** verschiedene Benutzerrollen definieren  
**damit** der Zugriff kontrolliert werden kann.

**Akzeptanzkriterien:**
- [ ] Benutzerregistrierung
- [ ] Rollenbasierte Zugriffe
- [ ] Passwort-Management
- [ ] Audit-Log

---

## Epic 7: Excel-Struktur-Validierung & Produktionssicherheit

**Beschreibung:** Automatische Validierung von Excel-Dateien gegen bekannte Strukturen für Produktionssicherheit.

### US-013: Excel-Struktur-Validierung
**Als** Administrator  
**möchte ich** neue Excel-Dateien automatisch gegen die bekannte Struktur validieren  
**damit** ich Format-Änderungen frühzeitig erkenne und Produktionsausfälle vermeide.

**Akzeptanzkriterien:**
- [ ] Machine-readable Excel-Struktur-Schema definiert
- [ ] Generischer Parser basierend auf Schema-Regeln
- [ ] Automatische Struktur-Validierung neuer Dateien
- [ ] Erkennung von neuen/geänderten/gelöschten Zählern
- [ ] Erkennung von neuen/geänderten Messpunkten
- [ ] Vergleichs-Engine zwischen generischem und Referenz-Parser
- [ ] CLI-Integration für manuelle Validierung
- [ ] Web-Interface Integration für automatische Checks
- [ ] Alerts bei kritischen Struktur-Änderungen

### US-014: Produktions-Validierung
**Als** Administrator  
**möchte ich** jeden neuen Excel-Upload automatisch validieren  
**damit** ich sicherstelle, dass alle Daten korrekt verarbeitet werden können.

**Akzeptanzkriterien:**
- [ ] Automatische Validierung bei Excel-Upload
- [ ] Struktur-Änderungen in Dashboard anzeigen
- [ ] Validierungs-Berichte generieren
- [ ] Historische Struktur-Änderungen verfolgen
- [ ] Rollback-Möglichkeit bei Validierungsfehlern

---

## Epic 8: UI-Modularisierung & Benutzerfreundlichkeit

**Beschreibung:** Modulares Dashboard und verbesserte Benutzerfreundlichkeit für Entwicklungs- und Produktivitäts-Tools.

### US-015: Modulares Dashboard
**Als** Administrator  
**möchte ich** ein modulares Dashboard mit verschiedenen Funktionsbereichen  
**damit** ich zwischen produktiven Funktionen und Entwicklungs-Tools unterscheiden kann.

**Akzeptanzkriterien:**
- [x] Sidebar-Navigation mit Modul-Auswahl
- [x] Excel-Analyse-Modul für produktive Funktionen
- [x] Development-Modul für Entwicklungs-Tools
- [x] Responsive Design für verschiedene Bildschirmgrößen
- [x] Modul-spezifische API-Endpunkte
- [x] State-Management zwischen Modulen

### US-016: Development-Dashboard
**Als** Entwickler  
**möchte ich** ein dediziertes Development-Dashboard  
**damit** ich den Projektfortschritt und alle Entwicklungs-Informationen übersichtlich verwalten kann.

**Akzeptanzkriterien:**
- [x] Vollständige Roadmap-Ansicht
- [x] User Stories-Übersicht mit Status
- [x] Live-Test-Status und Coverage
- [ ] Debug-Logs mit Filterung
- [x] API-Status-Monitoring
- [x] Entwicklungsfortschritt-Visualisierung

### US-017: Eigentümer-Daten-Management
**Als** Administrator  
**möchte ich** die Eigentümer-Daten im Web-Interface bearbeiten können  
**damit** ich Änderungen an Adressen, Namen oder anderen Eigentümer-Informationen einfach verwalten kann.

**Akzeptanzkriterien:**
- [x] Eigentümer-Liste im Dashboard anzeigen
- [x] Einzelne Eigentümer-Daten bearbeiten (Status-Umschaltung)
- [x] Neue Eigentümer hinzufügen
- [x] Eigentümer deaktivieren/aktivieren
- [x] Validierung der Eingabedaten
- [ ] Änderungshistorie verfolgen