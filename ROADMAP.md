# STWEG - Priorisiertes Backlog

## 📋 **Backlog Status (2025-01-08)**

**Gesamt:** 17 User Stories | **Abgeschlossen:** 6 | **In Bearbeitung:** 0 | **Geplant:** 11

---

## 🎯 **Priorität 1 - KRITISCH (Sofort)**

### US-008: PDF-Rechnung generieren ⭐⭐⭐
**Status:** 🔄 **NÄCHSTE PRIORITÄT**  
**Epic:** Rechnungsstellung  
**Als** Administrator **möchte ich** individuelle Rechnungen als PDF generieren **damit** ich sie an die Eigentümer versenden kann.

**Akzeptanzkriterien:**
- [ ] Rechnung im PDF-Format
- [ ] Eigentümer-spezifische Daten
- [ ] Vollständige Kostenaufschlüsselung
- [ ] Professionelles Layout

### US-013: Excel-Struktur-Validierung ⭐⭐⭐
**Status:** 🔄 **PRODUKTIONSSICHERHEIT**  
**Epic:** Excel-Struktur-Validierung & Produktionssicherheit  
**Als** Administrator **möchte ich** neue Excel-Dateien automatisch gegen die bekannte Struktur validieren **damit** ich Format-Änderungen frühzeitig erkenne und Produktionsausfälle vermeide.

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

---

## 🎯 **Priorität 2 - HOCH (Nächste Sprints)**

### US-003: Messpunkte auswerten ⭐⭐
**Status:** 📋 **GEPLANT**  
**Epic:** Stromkosten-Verwaltung  
**Als** Administrator **möchte ich** die Verbrauchsdaten der einzelnen Messpunkte auswerten **damit** ich den Stromverbrauch pro Eigentümer berechnen kann.

**Akzeptanzkriterien:**
- [ ] Gesamtverbrauch wird extrahiert
- [ ] Einzelne Messpunkte werden identifiziert
- [ ] Verbrauchsdaten werden korrekt zugeordnet
- [ ] Zeiträume werden berücksichtigt

### US-004: Stromkosten aufteilen ⭐⭐
**Status:** 📋 **GEPLANT**  
**Epic:** Stromkosten-Verwaltung  
**Als** Administrator **möchte ich** die Stromkosten proportional zum Verbrauch aufteilen **damit** jeder Eigentümer nur seinen Anteil zahlt.

**Akzeptanzkriterien:**
- [ ] Gesamtkosten werden auf Verbrauch umgelegt
- [ ] Proportionalberechnung ist korrekt
- [ ] Ergebnisse werden dokumentiert
- [ ] Aufschlüsselung nach Zeiträumen

### US-005: PDF-Rechnungen verwalten ⭐⭐
**Status:** 📋 **GEPLANT**  
**Epic:** Nebenkosten-Verwaltung  
**Als** Administrator **möchte ich** PDF-Rechnungen einlesen und kategorisieren **damit** ich alle Nebenkosten übersichtlich verwalten kann.

**Akzeptanzkriterien:**
- [ ] PDF-Rechnungen können hochgeladen werden
- [ ] Rechnungsdaten werden extrahiert
- [ ] Kategorisierung ist möglich
- [ ] Rechnungen können editiert werden

---

## 🎯 **Priorität 3 - MITTEL (Später)**

### US-006: Jahresrechnung erstellen ⭐
**Status:** 📋 **GEPLANT**  
**Epic:** Nebenkosten-Verwaltung  
**Als** Administrator **möchte ich** eine Übersicht aller Nebenkosten für das Jahr erstellen **damit** ich eine vollständige Abrechnung habe.

**Akzeptanzkriterien:**
- [ ] Alle Rechnungen werden aggregiert
- [ ] Kategorien werden aufgelistet
- [ ] Gesamtbeträge werden berechnet
- [ ] Zeitraum kann gewählt werden

### US-007: Kostenverteilung ⭐
**Status:** 📋 **GEPLANT**  
**Epic:** Nebenkosten-Verwaltung  
**Als** Administrator **möchte ich** die Nebenkosten nach definierten Schlüsseln verteilen **damit** jeder Eigentümer seinen Anteil kennt.

**Akzeptanzkriterien:**
- [ ] Verschiedene Verteilungsschlüssel verfügbar
- [ ] Anteile werden berechnet
- [ ] Eigentümer-spezifische Aufschlüsselung
- [ ] Nachvollziehbare Berechnung

### US-009: Rechnungsversand ⭐
**Status:** 📋 **GEPLANT**  
**Epic:** Rechnungsstellung  
**Als** Administrator **möchte ich** Rechnungen per E-Mail versenden **damit** die Eigentümer ihre Rechnungen erhalten.

**Akzeptanzkriterien:**
- [ ] E-Mail-Versand funktioniert
- [ ] PDF-Anhang ist korrekt
- [ ] E-Mail-Template ist professionell
- [ ] Versandbestätigung

### US-014: Produktions-Validierung ⭐
**Status:** 📋 **GEPLANT**  
**Epic:** Excel-Struktur-Validierung & Produktionssicherheit  
**Als** Administrator **möchte ich** jeden neuen Excel-Upload automatisch validieren **damit** ich sicherstelle, dass alle Daten korrekt verarbeitet werden können.

**Akzeptanzkriterien:**
- [ ] Automatische Validierung bei Excel-Upload
- [ ] Struktur-Änderungen in Dashboard anzeigen
- [ ] Validierungs-Berichte generieren
- [ ] Historische Struktur-Änderungen verfolgen
- [ ] Rollback-Möglichkeit bei Validierungsfehlern

---

## 🎯 **Priorität 4 - NIEDRIG (Future)**

### US-010: Web-Interface ⭐
**Status:** 📋 **GEPLANT**  
**Epic:** Benutzeroberfläche  
**Als** Administrator **möchte ich** eine benutzerfreundliche Web-Oberfläche **damit** ich alle Funktionen einfach bedienen kann.

**Akzeptanzkriterien:**
- [ ] Intuitive Navigation
- [ ] Responsive Design
- [ ] Upload-Funktionen
- [ ] Übersichtliche Darstellung der Daten

### US-012: Benutzer-Management ⭐
**Status:** 📋 **GEPLANT**  
**Epic:** System-Management  
**Als** Administrator **möchte ich** verschiedene Benutzerrollen definieren **damit** der Zugriff kontrolliert werden kann.

**Akzeptanzkriterien:**
- [ ] Benutzerregistrierung
- [ ] Rollenbasierte Zugriffe
- [ ] Passwort-Management
- [ ] Audit-Log

---

## ✅ **ABGESCHLOSSEN**

### US-001: Excel-File Struktur Analyse ✅
**Status:** ✅ **ABGESCHLOSSEN**  
**Epic:** Excel-File Analyse und Datenverarbeitung  
**Als** Administrator der Stockwerkeigentümergesellschaft **möchte ich** die Struktur des Excel-Files vom ZEV-Server analysieren **damit** ich verstehe, welche Daten verfügbar sind und wie sie strukturiert sind.

### US-002: Datenvalidierung ✅
**Status:** ✅ **ABGESCHLOSSEN**  
**Epic:** Excel-File Analyse und Datenverarbeitung  
**Als** Administrator **möchte ich** die Excel-Daten validieren **damit** ich sicherstellen kann, dass alle notwendigen Informationen vorhanden sind.

### US-011: Datenbank-Integration ✅
**Status:** ✅ **ABGESCHLOSSEN**  
**Epic:** System-Management  
**Als** Administrator **möchte ich** alle Daten in einer Datenbank speichern **damit** ich historische Daten abfragen und verwalten kann.

### US-015: Modulares Dashboard ✅
**Status:** ✅ **ABGESCHLOSSEN**  
**Epic:** UI-Modularisierung & Benutzerfreundlichkeit  
**Als** Administrator **möchte ich** ein modulares Dashboard mit verschiedenen Funktionsbereichen **damit** ich zwischen produktiven Funktionen und Entwicklungs-Tools unterscheiden kann.

### US-016: Development-Dashboard ✅
**Status:** ✅ **ABGESCHLOSSEN**  
**Epic:** UI-Modularisierung & Benutzerfreundlichkeit  
**Als** Entwickler **möchte ich** ein dediziertes Development-Dashboard **damit** ich den Projektfortschritt und alle Entwicklungs-Informationen übersichtlich verwalten kann.

### US-017: Eigentümer-Daten-Management ✅
**Status:** ✅ **ABGESCHLOSSEN**  
**Epic:** UI-Modularisierung & Benutzerfreundlichkeit  
**Als** Administrator **möchte ich** die Eigentümer-Daten im Web-Interface bearbeiten können **damit** ich Änderungen an Adressen, Namen oder anderen Eigentümer-Informationen einfach verwalten kann.

---

## 🎯 **Nächste Schritte**

1. **US-008 (PDF-Rechnung generieren)** - Nächste Priorität für MVP
2. **US-013 (Excel-Struktur-Validierung)** - Produktionssicherheit
3. **US-003 & US-004 (Stromkosten-Verwaltung)** - Core Business Logic

---

## 📊 **Metriken**

- **Fortschritt:** 35% (6/17 User Stories abgeschlossen)
- **Test-Status:** 41/41 Tests bestehen ✅
- **Code-Qualität:** Alle kritischen Bugs behoben ✅
- **Nächster Meilenstein:** MVP mit PDF-Rechnungsstellung