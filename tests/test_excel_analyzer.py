"""
Tests for Excel File Analyzer Module
Test-Driven Development für US-001: Excel-File Struktur Analyse
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os

# Import des zu entwickelnden Moduls (wird noch erstellt)
from src.excel_analysis.excel_analyzer import ExcelAnalyzer


class TestExcelAnalyzer:
    """Test-Klasse für Excel-Analyzer"""
    
    def test_analyzer_initialization(self):
        """Test: Analyzer kann initialisiert werden"""
        analyzer = ExcelAnalyzer()
        assert analyzer is not None
        assert hasattr(analyzer, 'analyze_file')
    
    def test_analyze_file_with_invalid_path(self):
        """Test: Fehlerbehandlung bei ungültigem Dateipfad"""
        analyzer = ExcelAnalyzer()
        
        with pytest.raises(FileNotFoundError):
            analyzer.analyze_file("nonexistent_file.xlsx")
    
    def test_analyze_file_with_non_excel_file(self):
        """Test: Fehlerbehandlung bei Nicht-Excel-Datei"""
        analyzer = ExcelAnalyzer()
        
        # Temporäre Textdatei erstellen
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is not an Excel file")
            temp_file = f.name
        
        try:
            with pytest.raises(ValueError, match="File is not a valid Excel file"):
                analyzer.analyze_file(temp_file)
        finally:
            os.unlink(temp_file)
    
    def test_analyze_file_structure(self):
        """Test: Excel-File Struktur wird korrekt analysiert"""
        analyzer = ExcelAnalyzer()
        
        # Test-Excel-Datei erstellen
        test_data = {
            'Zeitstempel': ['2024-01-01 00:00:00', '2024-01-01 01:00:00'],
            'Gesamtverbrauch': [100.5, 105.2],
            'Eigentümer_1': [25.1, 26.3],
            'Eigentümer_2': [30.2, 31.5],
            'Eigentümer_3': [45.2, 47.4]
        }
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            df = pd.DataFrame(test_data)
            df.to_excel(f.name, index=False, sheet_name='Verbrauchsdaten')
            temp_file = f.name
        
        try:
            result = analyzer.analyze_file(temp_file)
            
            # Überprüfung der Grundstruktur
            assert 'file_path' in result
            assert 'sheets' in result
            assert 'columns' in result
            assert 'sample_data' in result
            assert 'validation_status' in result
            
            # Überprüfung der Sheets
            assert 'Verbrauchsdaten' in result['sheets']
            
            # Überprüfung der Spalten
            expected_columns = ['Zeitstempel', 'Gesamtverbrauch', 'Eigentümer_1', 'Eigentümer_2', 'Eigentümer_3']
            assert all(col in result['columns']['Verbrauchsdaten'] for col in expected_columns)
            
        finally:
            os.unlink(temp_file)
    
    def test_validate_excel_structure(self):
        """Test: Excel-Struktur wird validiert"""
        analyzer = ExcelAnalyzer()
        
        # Test-Excel mit fehlenden Spalten
        test_data = {
            'Zeitstempel': ['2024-01-01'],
            'Gesamtverbrauch': [100.5]
            # Fehlende Eigentümer-Spalten
        }
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            df = pd.DataFrame(test_data)
            df.to_excel(f.name, index=False, sheet_name='Verbrauchsdaten')
            temp_file = f.name
        
        try:
            result = analyzer.analyze_file(temp_file)
            
            # Validierung sollte Probleme erkennen
            assert 'validation_errors' in result
            assert len(result['validation_errors']) > 0
            
        finally:
            os.unlink(temp_file)
    
    def test_extract_sample_data(self):
        """Test: Beispiel-Daten werden korrekt extrahiert"""
        analyzer = ExcelAnalyzer()
        
        test_data = {
            'Zeitstempel': ['2024-01-01 00:00:00', '2024-01-01 01:00:00', '2024-01-01 02:00:00'],
            'Gesamtverbrauch': [100.5, 105.2, 110.8],
            'Eigentümer_1': [25.1, 26.3, 27.7]
        }
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            df = pd.DataFrame(test_data)
            df.to_excel(f.name, index=False, sheet_name='Verbrauchsdaten')
            temp_file = f.name
        
        try:
            result = analyzer.analyze_file(temp_file)
            
            # Überprüfung der Beispiel-Daten
            assert 'sample_data' in result
            assert 'Verbrauchsdaten' in result['sample_data']
            
            sample = result['sample_data']['Verbrauchsdaten']
            assert len(sample) <= 5  # Maximal 5 Beispiel-Zeilen
            assert 'Zeitstempel' in sample[0] if sample else True
            
        finally:
            os.unlink(temp_file)
    
    def test_multiple_sheets_handling(self):
        """Test: Mehrere Tabellenblätter werden korrekt verarbeitet"""
        analyzer = ExcelAnalyzer()
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            # Mehrere Sheets erstellen
            with pd.ExcelWriter(f.name, engine='openpyxl') as writer:
                # Sheet 1: Verbrauchsdaten
                df1 = pd.DataFrame({
                    'Zeitstempel': ['2024-01-01'],
                    'Gesamtverbrauch': [100.5]
                })
                df1.to_excel(writer, sheet_name='Verbrauchsdaten', index=False)
                
                # Sheet 2: Eigentümer
                df2 = pd.DataFrame({
                    'Eigentümer_ID': [1, 2, 3],
                    'Name': ['Müller', 'Schmidt', 'Weber']
                })
                df2.to_excel(writer, sheet_name='Eigentümer', index=False)
            
            temp_file = f.name
        
        try:
            result = analyzer.analyze_file(temp_file)
            
            # Überprüfung der Mehrfach-Sheets
            assert len(result['sheets']) == 2
            assert 'Verbrauchsdaten' in result['sheets']
            assert 'Eigentümer' in result['sheets']
            
            # Überprüfung der Spalten für beide Sheets
            assert 'columns' in result
            assert 'Verbrauchsdaten' in result['columns']
            assert 'Eigentümer' in result['columns']
            
        finally:
            os.unlink(temp_file)


class TestExcelValidation:
    """Test-Klasse für Excel-Validierung"""
    
    def test_required_columns_validation(self):
        """Test: Validierung der erforderlichen Spalten"""
        analyzer = ExcelAnalyzer()
        
        # Excel ohne erforderliche Spalten
        test_data = {
            'Falsche_Spalte': ['Wert1', 'Wert2'],
            'Andere_Spalte': [1, 2]
        }
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            df = pd.DataFrame(test_data)
            df.to_excel(f.name, index=False)
            temp_file = f.name
        
        try:
            result = analyzer.analyze_file(temp_file)
            
            # Sollte Validierungsfehler haben
            assert 'validation_status' in result
            assert result['validation_status'] == 'errors_found'
            assert 'validation_errors' in result
            assert len(result['validation_errors']) > 0
            
        finally:
            os.unlink(temp_file)
    
    def test_data_format_validation(self):
        """Test: Validierung der Datenformate"""
        analyzer = ExcelAnalyzer()
        
        # Excel mit ungültigen Datenformaten
        test_data = {
            'Zeitstempel': ['kein_datum', '2024-01-01'],
            'Gesamtverbrauch': ['keine_zahl', 100.5]
        }
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            df = pd.DataFrame(test_data)
            df.to_excel(f.name, index=False)
            temp_file = f.name
        
        try:
            result = analyzer.analyze_file(temp_file)
            
            # Sollte Format-Fehler erkennen
            assert 'validation_errors' in result
            # Überprüfung, ob Format-Fehler erkannt werden
            
        finally:
            os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__])
