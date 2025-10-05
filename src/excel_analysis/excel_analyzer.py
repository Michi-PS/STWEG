"""
Excel File Analyzer for STWEG
Analysiert Excel-Dateien vom ZEV-Server und extrahiert Strukturinformationen
"""

import pandas as pd
import openpyxl
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Logger konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExcelAnalyzer:
    """
    Analysiert Excel-Dateien und extrahiert Strukturinformationen
    
    Diese Klasse implementiert US-001: Excel-File Struktur Analyse
    """
    
    def __init__(self):
        """Initialisiert den Excel-Analyzer"""
        self.required_columns = {
            'Zeitstempel': 'datetime',
            'Gesamtverbrauch': 'numeric'
        }
        self.optional_columns = {
            'Eigentümer_': 'numeric'  # Pattern für Eigentümer-Spalten
        }
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analysiert eine Excel-Datei und gibt Strukturinformationen zurück
        
        Args:
            file_path (str): Pfad zur Excel-Datei
            
        Returns:
            Dict[str, Any]: Analyseergebnis mit Strukturinformationen
            
        Raises:
            FileNotFoundError: Wenn die Datei nicht existiert
            ValueError: Wenn die Datei kein gültiges Excel-Format hat
        """
        logger.info(f"Analysiere Excel-Datei: {file_path}")
        
        # Datei-Existenz prüfen
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")
        
        # Excel-Format prüfen
        if not self._is_excel_file(file_path):
            raise ValueError("File is not a valid Excel file")
        
        try:
            # Excel-Datei laden
            excel_data = pd.ExcelFile(file_path)
            
            # Strukturanalyse durchführen
            result = {
                'file_path': file_path,
                'sheets': excel_data.sheet_names,
                'columns': {},
                'sample_data': {},
                'validation_status': 'unknown',
                'validation_errors': []
            }
            
            # Jedes Tabellenblatt analysieren
            for sheet_name in excel_data.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Spalten extrahieren
                result['columns'][sheet_name] = list(df.columns)
                
                # Beispiel-Daten extrahieren (maximal 5 Zeilen)
                sample_size = min(5, len(df))
                result['sample_data'][sheet_name] = df.head(sample_size).to_dict('records')
            
            # Validierung durchführen
            validation_result = self._validate_structure(result)
            result.update(validation_result)
            
            logger.info(f"Analyse abgeschlossen: {len(result['sheets'])} Sheets gefunden")
            return result
            
        except Exception as e:
            logger.error(f"Fehler bei der Excel-Analyse: {str(e)}")
            raise ValueError(f"Fehler beim Lesen der Excel-Datei: {str(e)}")
    
    def _is_excel_file(self, file_path: str) -> bool:
        """
        Prüft, ob eine Datei ein gültiges Excel-Format hat
        
        Args:
            file_path (str): Pfad zur Datei
            
        Returns:
            bool: True wenn Excel-Format, False sonst
        """
        excel_extensions = ['.xlsx', '.xls', '.xlsm', '.xlsb']
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension not in excel_extensions:
            return False
        
        # Zusätzliche Prüfung mit openpyxl
        try:
            openpyxl.load_workbook(file_path, read_only=True)
            return True
        except:
            return False
    
    def _validate_structure(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validiert die Excel-Struktur gegen erwartete Formate
        
        Args:
            analysis_result (Dict[str, Any]): Ergebnis der Strukturanalyse
            
        Returns:
            Dict[str, Any]: Validierungsergebnis
        """
        validation_result = {
            'validation_status': 'valid',
            'validation_errors': []
        }
        
        # Prüfung der Tabellenblätter
        if not analysis_result['sheets']:
            validation_result['validation_errors'].append("Keine Tabellenblätter gefunden")
            validation_result['validation_status'] = 'errors_found'
        
        # Prüfung der Spalten für jedes Tabellenblatt
        for sheet_name, columns in analysis_result['columns'].items():
            sheet_errors = self._validate_sheet_columns(columns, sheet_name)
            validation_result['validation_errors'].extend(sheet_errors)
        
        # Status aktualisieren
        if validation_result['validation_errors']:
            validation_result['validation_status'] = 'errors_found'
        else:
            validation_result['validation_status'] = 'valid'
        
        return validation_result
    
    def _validate_sheet_columns(self, columns: List[str], sheet_name: str) -> List[str]:
        """
        Validiert die Spalten eines Tabellenblatts
        
        Args:
            columns (List[str]): Liste der Spaltennamen
            sheet_name (str): Name des Tabellenblatts
            
        Returns:
            List[str]: Liste der Validierungsfehler
        """
        errors = []
        
        # Prüfung der erforderlichen Spalten
        for required_col, expected_type in self.required_columns.items():
            if required_col not in columns:
                errors.append(f"Sheet '{sheet_name}': Erforderliche Spalte '{required_col}' nicht gefunden")
        
        # Prüfung auf Eigentümer-Spalten (optional)
        owner_columns = [col for col in columns if col.startswith('Eigentümer_')]
        if not owner_columns and 'Gesamtverbrauch' in columns:
            errors.append(f"Sheet '{sheet_name}': Keine Eigentümer-Spalten gefunden")
        
        # Prüfung der Datenformate (vereinfacht)
        # Hier könnte erweiterte Validierung implementiert werden
        
        return errors
    
    def get_consumption_data(self, file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """
        Extrahiert Verbrauchsdaten aus der Excel-Datei
        
        Args:
            file_path (str): Pfad zur Excel-Datei
            sheet_name (Optional[str]): Name des Tabellenblatts (None für erstes Sheet)
            
        Returns:
            pd.DataFrame: Verbrauchsdaten
        """
        logger.info(f"Extrahiere Verbrauchsdaten aus: {file_path}")
        
        # Analyse durchführen
        analysis = self.analyze_file(file_path)
        
        # Sheet auswählen
        if sheet_name is None:
            sheet_name = analysis['sheets'][0]
        
        # Daten laden
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Datenvalidierung und -bereinigung
        df = self._clean_consumption_data(df)
        
        return df
    
    def _clean_consumption_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Bereinigt und validiert Verbrauchsdaten
        
        Args:
            df (pd.DataFrame): Rohdaten
            
        Returns:
            pd.DataFrame: Bereinigte Daten
        """
        # Leere Zeilen entfernen
        df = df.dropna(how='all')
        
        # Zeitstempel konvertieren (falls vorhanden)
        if 'Zeitstempel' in df.columns:
            try:
                df['Zeitstempel'] = pd.to_datetime(df['Zeitstempel'])
            except:
                logger.warning("Zeitstempel-Spalte konnte nicht konvertiert werden")
        
        # Numerische Spalten konvertieren
        numeric_columns = [col for col in df.columns if col.startswith(('Gesamtverbrauch', 'Eigentümer_'))]
        for col in numeric_columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except:
                logger.warning(f"Spalte '{col}' konnte nicht zu numerisch konvertiert werden")
        
        return df
    
    def generate_report(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generiert einen Textbericht der Analyseergebnisse
        
        Args:
            analysis_result (Dict[str, Any]): Analyseergebnis
            
        Returns:
            str: Formatierten Bericht
        """
        report = []
        report.append("=" * 60)
        report.append("EXCEL-DATEI ANALYSE BERICHT")
        report.append("=" * 60)
        report.append(f"Datei: {analysis_result['file_path']}")
        report.append(f"Status: {analysis_result['validation_status']}")
        report.append("")
        
        # Tabellenblätter
        report.append("TABELLENBLÄTTER:")
        for sheet in analysis_result['sheets']:
            report.append(f"  - {sheet}")
        report.append("")
        
        # Spalten pro Sheet
        report.append("SPALTEN:")
        for sheet_name, columns in analysis_result['columns'].items():
            report.append(f"  {sheet_name}:")
            for col in columns:
                report.append(f"    - {col}")
        report.append("")
        
        # Validierungsfehler
        if analysis_result['validation_errors']:
            report.append("VALIDIERUNGSFEHLER:")
            for error in analysis_result['validation_errors']:
                report.append(f"  - {error}")
        else:
            report.append("VALIDIERUNG: Keine Fehler gefunden")
        
        report.append("=" * 60)
        
        return "\n".join(report)


# Beispiel-Verwendung
if __name__ == "__main__":
    # Test des Analyzers
    analyzer = ExcelAnalyzer()
    
    # Beispiel-Pfad (zu ersetzen mit tatsächlichem Pfad)
    example_file = "data/sample/test_data.xlsx"
    
    try:
        result = analyzer.analyze_file(example_file)
        report = analyzer.generate_report(result)
        print(report)
    except FileNotFoundError:
        print(f"Beispieldatei nicht gefunden: {example_file}")
    except Exception as e:
        print(f"Fehler: {e}")
