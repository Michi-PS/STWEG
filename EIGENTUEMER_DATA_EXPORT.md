# Eigentümer-Daten Export & Import

## 📋 **Übersicht**

Die STWEG-Anwendung bietet verschiedene Möglichkeiten, Eigentümer-Daten zu exportieren und für externe Systeme zur Verfügung zu stellen.

## 🔗 **Verfügbare Export-Formate**

### **1. JSON-Export (Empfohlen)**
```bash
# API-Endpunkt
GET /api/eigentuemer/export?format=json

# Beispiel-Aufruf
curl "http://localhost:8080/api/eigentuemer/export?format=json"
```

**Vorteile:**
- Vollständige Datenstruktur
- Inklusive Metadaten und Beziehungen
- Maschinenlesbar und strukturiert
- Einfach zu verarbeiten

### **2. CSV-Export**
```bash
# API-Endpunkt
GET /api/eigentuemer/export?format=csv

# Beispiel-Aufruf
curl "http://localhost:8080/api/eigentuemer/export?format=csv" -o eigentuemer.csv
```

**Vorteile:**
- Excel-kompatibel
- Einfach zu bearbeiten
- Tabellarische Darstellung

### **3. Excel-Export**
```bash
# API-Endpunkt
GET /api/eigentuemer/export?format=excel

# Beispiel-Aufruf
curl "http://localhost:8080/api/eigentuemer/export?format=excel" -o eigentuemer.xlsx
```

**Vorteile:**
- Professionelle Formatierung
- Inklusive Messpunkte-Count
- Excel-optimiert

## 📁 **Statische Dateien**

### **Beispieldaten**
```bash
# Datei: data/exports/eigentuemer_sample.json
cat data/exports/eigentuemer_sample.json
```

**Inhalt:**
- 4 Beispiel-Eigentümer
- Vollständige Datenstruktur
- Messpunkte-Zuordnungen
- Metadaten

## 🎯 **Verwendungsszenarien**

### **Für Entwickler/APIs**
```javascript
// JavaScript Fetch
fetch('/api/eigentuemer/export?format=json')
  .then(response => response.json())
  .then(data => {
    console.log('Eigentümer-Daten:', data.eigentuemer);
  });
```

```python
# Python Requests
import requests

response = requests.get('http://localhost:8080/api/eigentuemer/export?format=json')
data = response.json()
eigentuemer = data['eigentuemer']
```

### **Für Excel/CSV-Import**
```bash
# CSV für Excel öffnen
curl "http://localhost:8080/api/eigentuemer/export?format=csv" -o eigentuemer.csv
open eigentuemer.csv
```

### **Für Datenbank-Import**
```bash
# JSON für weitere Verarbeitung
curl "http://localhost:8080/api/eigentuemer/export?format=json" > eigentuemer.json
```

## 🔧 **Template für Import**

### **Template herunterladen**
```bash
# CSV-Template
curl "http://localhost:8080/api/eigentuemer/template?format=csv" -o template.csv

# Excel-Template
curl "http://localhost:8080/api/eigentuemer/template?format=excel" -o template.xlsx

# JSON-Template
curl "http://localhost:8080/api/eigentuemer/template?format=json"
```

### **Template-Struktur**
```csv
Name,Wohnung,Anteil,Email,Telefon,Aktiv
Max Mustermann,1A,0.14,max@example.com,+41 44 123 45 67,True
```

## 🌐 **Web-Interface**

### **Export über Dashboard**
1. Öffne http://localhost:8080
2. Navigiere zu "Eigentümer" Modul
3. Klicke auf "Export" Dropdown
4. Wähle Format (JSON/CSV/Excel)
5. Datei wird automatisch heruntergeladen

### **Verfügbare Aktionen**
- ✅ **JSON-Export** - Vollständige Datenstruktur
- ✅ **CSV-Export** - Tabellarische Darstellung  
- ✅ **Excel-Export** - Professionelle Formatierung
- ✅ **Template-Download** - Import-Vorlage

## 📊 **Datenstruktur**

### **JSON-Format**
```json
{
  "export_date": "2024-01-15T10:30:00",
  "total_count": 4,
  "eigentuemer": [
    {
      "id": 1,
      "name": "Anna Müller",
      "wohnung": "1A",
      "anteil": 0.25,
      "anteil_prozent": 25.0,
      "email": "anna.mueller@example.com",
      "telefon": "+41 44 123 45 67",
      "aktiv": true,
      "erstellt_am": "2024-01-01T08:00:00",
      "messpunkte_count": 2,
      "messpunkte": [...]
    }
  ]
}
```

### **CSV-Format**
```csv
Name,Wohnung,Anteil,Anteil_Prozent,Email,Telefon,Aktiv,Erstellt_Am
Anna Müller,1A,0.25,25.0,anna.mueller@example.com,+41 44 123 45 67,True,2024-01-01 08:00:00
```

## 🔐 **Sicherheit & Zugriff**

### **API-Zugriff**
- ✅ **Lokaler Zugriff**: http://localhost:8080
- ✅ **Keine Authentifizierung** (Development)
- ✅ **CORS-freundlich** für Frontend-Integration

### **Datei-Zugriff**
- ✅ **Statische Dateien**: `data/exports/`
- ✅ **Direkter Pfad**: `/Users/rechberger/Documents/Coding/STWEG/data/exports/`
- ✅ **Git-versioniert** (außer sensible Daten)

## 📝 **Beispiele**

### **Komplettes Export-Script**
```bash
#!/bin/bash
# Export aller Formate

echo "📥 Exportiere Eigentümer-Daten..."

# JSON
curl -s "http://localhost:8080/api/eigentuemer/export?format=json" > eigentuemer_$(date +%Y%m%d).json

# CSV  
curl -s "http://localhost:8080/api/eigentuemer/export?format=csv" > eigentuemer_$(date +%Y%m%d).csv

# Excel
curl -s "http://localhost:8080/api/eigentuemer/export?format=excel" > eigentuemer_$(date +%Y%m%d).xlsx

echo "✅ Export abgeschlossen!"
```

### **Python-Integration**
```python
import requests
import pandas as pd

# Eigentümer-Daten abrufen
response = requests.get('http://localhost:8080/api/eigentuemer/export?format=json')
data = response.json()

# Als DataFrame laden
df = pd.DataFrame(data['eigentuemer'])
print(f"Gefunden: {len(df)} Eigentümer")

# Weitere Verarbeitung...
```

## 🎯 **Empfohlene Workflows**

### **Für Entwicklung**
1. **JSON-Export** für API-Integration
2. **Statische Dateien** für Tests
3. **Template** für Datenaufbau

### **Für Produktion**
1. **Excel-Export** für Berichte
2. **CSV-Export** für Datenbank-Import
3. **JSON-Export** für System-Integration

### **Für Backup**
1. **JSON-Export** mit Zeitstempel
2. **Alle Formate** für Redundanz
3. **Regelmäßige Exports** automatisieren

---

**💡 Tipp:** Verwende das Web-Interface für einfache Exports oder die API für automatisierte Workflows!
