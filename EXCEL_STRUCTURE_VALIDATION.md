# Excel-Struktur-Validierung & Generischer Parser

## 🎯 **Ziel**
Automatische Validierung neuer Excel-Dateien gegen bekannte Struktur für Produktionssicherheit.

## 📋 **Vorgehensweise**

### **Phase 1: Struktur-Dokumentation (Machine-Readable)**

#### 1.1 Excel-Struktur-Schema definieren
```yaml
# excel_structure_schema.yaml
structure:
  sheets:
    - name: "ZEV_Output"
      type: "main_data"
      validation_rules:
        - required_columns: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
        - header_row: 1
        - data_start_row: 2
  
  patterns:
    hauptzaehler:
      identifier: "CHINV[0-9]{30}"
      location: "column_A"
      name_location: "column_B"
      validation: "regex_match"
    
    unterzaehler:
      identifier: "CHINV[0-9]{30}"
      location: "column_A"
      name_location: "column_B"
      parent_context: "submeter_section"
    
    messpunkt:
      patterns:
        - "Bezug Netz HT [kWh]"
        - "Bezug Netz NT [kWh]"
        - "Bezug lokal HT [kWh]"
        - "Bezug lokal NT [kWh]"
      location: "column_A_or_B"
      data_columns: ["C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]
    
    virtueller_zaehler:
      identifiers: ["XXLOSS", "XXSELF"]
      location: "column_A"
      name_location: "column_B"
```

#### 1.2 Regeln-Engine definieren
```python
# structure_rules.py
class ExcelStructureRules:
    def __init__(self, schema_file):
        self.schema = self.load_schema(schema_file)
    
    def validate_structure(self, excel_data):
        # Validierung gegen Schema
        pass
    
    def extract_entities(self, excel_data):
        # Generische Extraktion basierend auf Regeln
        pass
```

### **Phase 2: Generischer Parser**

#### 2.1 Parser-Architektur
```python
# generic_excel_parser.py
class GenericExcelParser:
    def __init__(self, structure_schema):
        self.schema = structure_schema
        self.rules_engine = ExcelStructureRules(structure_schema)
    
    def parse(self, file_path):
        # 1. Excel laden
        # 2. Struktur validieren
        # 3. Entitäten extrahieren
        # 4. Daten normalisieren
        pass
    
    def compare_with_reference(self, reference_data):
        # Vergleich mit Referenz-Parser
        pass
```

#### 2.2 Vergleichs-Engine
```python
# parser_comparison.py
class ParserComparison:
    def compare_outputs(self, generic_output, reference_output):
        # Strukturelle Unterschiede identifizieren
        # Neue/geänderte/gelöschte Entitäten
        # Datenvalidierung
        pass
```

### **Phase 3: Implementierung**

#### 3.1 Dateien-Struktur
```
src/
├── excel_analysis/
│   ├── structure_schema.yaml          # Machine-readable Schema
│   ├── generic_parser.py              # Neuer generischer Parser
│   ├── structure_rules.py             # Regeln-Engine
│   ├── parser_comparison.py           # Vergleichs-Engine
│   └── simple_zev_parser.py           # Bestehender Parser (Referenz)
```

#### 3.2 CLI-Integration
```bash
# Neue CLI-Befehle
python src/cli.py validate-structure file.xlsx
python src/cli.py compare-parsers file.xlsx
python src/cli.py generate-schema --from-reference
```

### **Phase 4: Produktions-Integration**

#### 4.1 Automatische Validierung
```python
# production_validator.py
class ProductionValidator:
    def validate_new_file(self, file_path):
        # 1. Generischer Parser
        # 2. Vergleich mit Referenz
        # 3. Struktur-Änderungen melden
        # 4. Alerts bei kritischen Änderungen
        pass
```

#### 4.2 Web-Interface Integration
```python
# Neue API-Endpunkte
@app.route('/api/excel/validate-structure/<filename>')
@app.route('/api/excel/compare-parsers/<filename>')
@app.route('/api/excel/structure-changes/<filename>')
```

## 🎯 **Konkrete Vorteile**

1. **Struktur-Änderungen erkennen:** Neue Zähler, geänderte Spalten, neue Messpunkte
2. **Automatische Validierung:** Jedes neue File wird gegen Schema geprüft
3. **Produktionssicherheit:** Frühe Erkennung von Format-Änderungen
4. **Wartbarkeit:** Schema-basierte Regeln statt hardcoded Logic
5. **Dokumentation:** Machine-readable Struktur-Beschreibung

## 🚀 **Implementierungsreihenfolge**

1. **Schema-Definition:** Excel-Struktur in YAML/JSON dokumentieren
2. **Regeln-Engine:** Generische Validierungslogik implementieren
3. **Generischer Parser:** Schema-basierte Extraktion
4. **Vergleichs-Engine:** Output-Validation gegen Referenz
5. **Integration:** CLI + Web-Interface

## 📊 **Erkannte Excel-Struktur (basierend auf Debug-Logs)**

### Zähler-Typen:
- **Hauptzähler:** 13 Stück (CHINV12205150525900000000000000061-70, etc.)
- **Unterzähler:** 1 Stück (CHINV12205150525900000000000000101 - Ladestation 1)
- **Virtuelle Zähler:** 2 Stück (XXLOSS - Verlust, XXSELF)

### Messpunkt-Typen:
- **Bezug Netz HT [kWh]**
- **Bezug Netz NT [kWh]**
- **Bezug lokal HT [kWh]**
- **Bezug lokal NT [kWh]**

### Monats-Header:
Januar, Februar, März, April, Mai, Juni, Juli, August, September, Oktober, November, Dezember

### Spalten-Layout:
- **Spalte A:** Zähler-IDs (CHINV...) oder virtuelle Zähler (XXLOSS, XXSELF)
- **Spalte B:** Zähler-Namen oder Messpunkt-Namen
- **Spalten C-N:** Monatliche Verbrauchsdaten (12 Monate)

## 🔍 **Validierungsregeln**

1. **Zähler-ID Format:** CHINV + 30 Ziffern
2. **Messpunkt-Namen:** Exakte Übereinstimmung mit bekannten Mustern
3. **Daten-Integrität:** Numerische Werte in Monatsspalten
4. **Strukturelle Konsistenz:** Hauptzähler → Unterzähler → Hauptzähler Sequenz
5. **Virtuelle Zähler:** XXLOSS, XXSELF als spezielle Marker

## 📝 **Status**
- **Dokumentiert:** ✅
- **Schema erstellt:** ⏳ (nächster Schritt)
- **Parser implementiert:** ⏳
- **Integration:** ⏳
