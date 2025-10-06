"""
Smart Excel Reader - Intelligenter Excel-Parser für ZEV-Dateien
Erkennt automatisch die Struktur und passt die Einlesemethode an
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, List, Any, Tuple, Optional
import re

logger = logging.getLogger(__name__)

class SmartExcelReader:
    """Intelligenter Excel-Reader für ZEV-Dateien"""
    
    def __init__(self):
        self.zev_patterns = {
            'header_indicators': [
                'zwischenbächen', 'zürich', 'leistungsberechnung', 'standard',
                'chinv', 'zev', 'bilanz', 'messung', 'zähler'
            ],
            'month_names': [
                'januar', 'februar', 'märz', 'april', 'mai', 'juni',
                'juli', 'august', 'september', 'oktober', 'november', 'dezember'
            ],
            'data_indicators': [
                'chinv', 'zähler', 'messpunkt', 'wohnung', 'einheit',
                'verbrauch', 'kwh', 'stand', 'zählerstand'
            ]
        }
    
    def analyze_excel_structure(self, file_path: str) -> Dict[str, Any]:
        """
        Analysiert die Excel-Struktur intelligent
        
        Args:
            file_path (str): Pfad zur Excel-Datei
            
        Returns:
            Dict: Struktur-Analyse mit Empfehlungen
        """
        logger.info(f"🔍 Analysiere Excel-Struktur: {file_path}")
        
        try:
            excel_file = pd.ExcelFile(file_path)
            analysis = {
                'file_path': file_path,
                'file_name': Path(file_path).name,
                'sheets': excel_file.sheet_names,
                'recommended_reading_method': None,
                'structure_info': {},
                'sample_data': {}
            }
            
            # Jedes Sheet analysieren
            for sheet_name in excel_file.sheet_names:
                logger.info(f"📊 Analysiere Sheet: {sheet_name}")
                sheet_analysis = self._analyze_sheet_structure(file_path, sheet_name)
                analysis['structure_info'][sheet_name] = sheet_analysis
                
                # Empfehlung für beste Lesart
                if sheet_analysis['recommended_method']:
                    analysis['recommended_reading_method'] = sheet_analysis['recommended_method']
                    analysis['sample_data'][sheet_name] = sheet_analysis['sample_data']
            
            logger.info(f"✅ Struktur-Analyse abgeschlossen")
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Fehler bei der Struktur-Analyse: {str(e)}")
            raise ValueError(f"Fehler beim Analysieren der Excel-Struktur: {str(e)}")
    
    def _analyze_sheet_structure(self, file_path: str, sheet_name: str) -> Dict[str, Any]:
        """Analysiert die Struktur eines einzelnen Sheets"""
        
        analysis = {
            'sheet_name': sheet_name,
            'recommended_method': None,
            'header_row': None,
            'data_start_row': None,
            'structure_type': 'unknown',
            'confidence_score': 0,
            'sample_data': None,
            'column_mapping': {}
        }
        
        # Verschiedene Lesarten testen
        reading_methods = []
        
        # Methode 1: Standard-Lesen
        try:
            df_standard = pd.read_excel(file_path, sheet_name=sheet_name)
            method1 = self._evaluate_reading_method(df_standard, 'standard', 0)
            reading_methods.append(method1)
        except Exception as e:
            reading_methods.append({'method': 'standard', 'error': str(e), 'score': 0})
        
        # Methode 2-10: Verschiedene Header-Zeilen
        for header_row in range(1, 11):
            try:
                df_header = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)
                method = self._evaluate_reading_method(df_header, f'header_{header_row}', header_row)
                reading_methods.append(method)
            except Exception:
                continue
        
        # Methode 11: Ohne Header
        try:
            df_no_header = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
            method_no_header = self._evaluate_reading_method(df_no_header, 'no_header', None)
            reading_methods.append(method_no_header)
        except Exception as e:
            reading_methods.append({'method': 'no_header', 'error': str(e), 'score': 0})
        
        # Beste Methode auswählen
        valid_methods = [m for m in reading_methods if 'error' not in m]
        if valid_methods:
            best_method = max(valid_methods, key=lambda x: x['score'])
            analysis.update(best_method)
        
        return analysis
    
    def _evaluate_reading_method(self, df: pd.DataFrame, method_name: str, header_row: Optional[int]) -> Dict[str, Any]:
        """Bewertet eine Lesart und gibt Score zurück"""
        
        if df.empty:
            return {
                'method': method_name,
                'score': 0,
                'error': 'DataFrame ist leer'
            }
        
        score = 0
        structure_type = 'unknown'
        confidence_factors = []
        
        # Basis-Score für gültige Daten
        if len(df) > 0:
            score += 10
            confidence_factors.append('Daten vorhanden')
        
        # Spalten-Analyse
        columns = [str(col).lower() for col in df.columns]
        
        # ZEV-Header-Erkennung
        header_indicators = sum(1 for pattern in self.zev_patterns['header_indicators'] 
                               if any(pattern in col for col in columns))
        if header_indicators > 0:
            score += 20
            confidence_factors.append(f'ZEV-Header erkannt ({header_indicators})')
        
        # Monatsnamen-Erkennung
        month_indicators = sum(1 for pattern in self.zev_patterns['month_names'] 
                              if any(pattern in col for col in columns))
        if month_indicators >= 6:  # Mindestens 6 Monate
            score += 30
            structure_type = 'zev_monthly_data'
            confidence_factors.append(f'Monatsdaten erkannt ({month_indicators})')
        
        # Daten-Indikatoren
        data_indicators = sum(1 for pattern in self.zev_patterns['data_indicators'] 
                             if any(pattern in col for col in columns))
        if data_indicators > 0:
            score += 15
            confidence_factors.append(f'Daten-Indikatoren ({data_indicators})')
        
        # Spaltenanzahl-Bewertung
        col_count = len(df.columns)
        if 8 <= col_count <= 20:  # Typische ZEV-Spaltenanzahl
            score += 10
            confidence_factors.append(f'Optimale Spaltenanzahl ({col_count})')
        
        # Datenqualität
        non_empty_rows = len(df.dropna(how='all'))
        if non_empty_rows > 10:
            score += 15
            confidence_factors.append(f'Viele Datenzeilen ({non_empty_rows})')
        
        # Sample-Daten extrahieren
        sample_data = self._extract_sample_data(df)
        
        # Header-Row schätzen
        estimated_header_row = self._estimate_header_row(df, header_row)
        
        return {
            'method': method_name,
            'score': score,
            'structure_type': structure_type,
            'confidence_factors': confidence_factors,
            'sample_data': sample_data,
            'header_row': estimated_header_row,
            'data_start_row': estimated_header_row + 1 if estimated_header_row else 0,
            'column_mapping': self._create_column_mapping(df.columns),
            'shape': df.shape,
            'columns': list(df.columns)
        }
    
    def _extract_sample_data(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Extrahiert Sample-Daten für Anzeige"""
        sample_data = []
        
        # Erste 5 Zeilen, erste 10 Spalten
        for i in range(min(5, len(df))):
            row_data = {}
            for j in range(min(10, len(df.columns))):
                col_name = str(df.columns[j])
                value = df.iloc[i, j]
                
                # NaN-Werte bereinigen
                if pd.isna(value):
                    row_data[col_name] = ''
                else:
                    row_data[col_name] = str(value)
            
            sample_data.append(row_data)
        
        return sample_data
    
    def _estimate_header_row(self, df: pd.DataFrame, header_row: Optional[int]) -> Optional[int]:
        """Schätzt die Header-Zeile basierend auf Dateninhalt"""
        
        # Wenn header_row gegeben, verwende das
        if header_row is not None:
            return header_row
        
        # Suche nach typischen Header-Mustern in den ersten 10 Zeilen
        for i in range(min(10, len(df))):
            row_values = [str(val).lower() for val in df.iloc[i].values if not pd.isna(val)]
            
            # Prüfe auf Header-Indikatoren
            header_matches = sum(1 for pattern in self.zev_patterns['header_indicators'] 
                               if any(pattern in val for val in row_values))
            
            month_matches = sum(1 for pattern in self.zev_patterns['month_names'] 
                              if any(pattern in val for val in row_values))
            
            if header_matches > 0 or month_matches >= 6:
                return i
        
        return None
    
    def _create_column_mapping(self, columns: List[str]) -> Dict[str, str]:
        """Erstellt ein Mapping der Spalten zu erkannten Typen"""
        
        mapping = {}
        
        for col in columns:
            col_lower = str(col).lower()
            
            # Monatsnamen
            if any(month in col_lower for month in self.zev_patterns['month_names']):
                mapping[str(col)] = 'month'
            
            # Zähler/Messpunkt
            elif any(pattern in col_lower for pattern in ['zähler', 'messpunkt', 'chinv']):
                mapping[str(col)] = 'meter_point'
            
            # Wohnung/Einheit
            elif any(pattern in col_lower for pattern in ['wohnung', 'einheit', 'apt']):
                mapping[str(col)] = 'apartment'
            
            # Verbrauch
            elif any(pattern in col_lower for pattern in ['verbrauch', 'kwh', 'stand']):
                mapping[str(col)] = 'consumption'
            
            # Kosten
            elif any(pattern in col_lower for pattern in ['kosten', 'betrag', 'eur', 'chf']):
                mapping[str(col)] = 'cost'
            
            else:
                mapping[str(col)] = 'unknown'
        
        return mapping
    
    def read_excel_with_recommended_method(self, file_path: str) -> Dict[str, Any]:
        """
        Liest Excel-Datei mit der empfohlenen Methode
        
        Args:
            file_path (str): Pfad zur Excel-Datei
            
        Returns:
            Dict: Gelesene Daten mit Metadaten
        """
        
        # Struktur analysieren
        structure_analysis = self.analyze_excel_structure(file_path)
        
        if not structure_analysis['recommended_reading_method']:
            raise ValueError("Keine geeignete Lesart gefunden")
        
        recommended_method = structure_analysis['recommended_reading_method']
        
        # Mit empfohlener Methode lesen
        for sheet_name, sheet_info in structure_analysis['structure_info'].items():
            if sheet_info['method'] == recommended_method['method']:
                
                # DataFrame mit empfohlener Methode lesen
                if recommended_method['method'] == 'no_header':
                    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
                elif recommended_method['method'].startswith('header_'):
                    header_row = int(recommended_method['method'].split('_')[1])
                    df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)
                else:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                return {
                    'success': True,
                    'data': df,
                    'structure_analysis': structure_analysis,
                    'reading_method': recommended_method,
                    'sheet_name': sheet_name
                }
        
        raise ValueError("Empfohlene Lesart konnte nicht angewendet werden")

