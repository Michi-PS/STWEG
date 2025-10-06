#!/usr/bin/env python3
"""
Einfacher ZEV-Parser - garantiert NaN-frei für JSON
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, Any, List

class SimpleZEVParser:
    """Einfacher ZEV-Parser ohne NaN-Probleme"""
    
    def __init__(self):
        self.month_names = [
            "Januar", "Februar", "März", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember"
        ]
    
    def parse_zev_file(self, file_path: str) -> Dict[str, Any]:
        """Parst ZEV-Datei und gibt garantiert JSON-sichere Daten zurück"""
        
        print(f"🔍 SimpleZEVParser: Parse {Path(file_path).name}")
        
        try:
            # Excel laden
            df = pd.read_excel(file_path, header=None)
            df = df.fillna('')  # Alle NaN zu leeren Strings
            
            result = {
                'file_name': Path(file_path).name,
                'structure_verified': True,
                'structure_info': {
                    'errors': [],
                    'warnings': [],
                    'month_columns': ['Januar', 'Februar']  # Basierend auf Screenshot
                },
                'summary': {
                    'total_zaehler': 0,
                    'total_messpunkte': 0,
                    'hauptzaehler': 0,
                    'unterzaehler': 0,
                    'virtuelle_zaehler': 0
                },
                'zaehler_overview': []
            }
            
            # Dynamische Zähler-Suche: Hauptzähler (Spalte A) und Unterzähler (Spalte B)
            zaehler_count = 0
            total_messpunkte = 0
            current_zaehler = None
            month_columns = []  # Monats-Spalten sammeln
            in_submeter_section = False  # Flag für Unterzähler-Bereich
            
            for idx, row in df.iterrows():
                col_a = str(row[0]).strip() if len(row) > 0 else ''
                col_b = str(row[1]).strip() if len(row) > 1 else ''
                col_c = str(row[2]).strip() if len(row) > 2 else ''
                
                # Debug: Zeige alle Zeilen mit Unterzähler-Context
                if current_zaehler and current_zaehler['type'] == 'unterzaehler':
                    print(f"🔍 DEBUG Alle Zeilen (Unterzähler): Zeile {idx}: col_a='{col_a}', col_b='{col_b}', current_zaehler={current_zaehler['id']}")
                
                # Debug: Zeige alle Zeilen mit potentiellen Zähler-IDs
                if col_a.startswith('XX') or 'CHINV' in col_a.upper():
                    print(f"🔍 DEBUG Zeile {idx}: col_a='{col_a}', col_b='{col_b}', in_submeter={in_submeter_section}")
                
                # "Untermessungen" Header erkennen -> Unterzähler-Bereich starten
                if 'Untermessungen' in col_a or 'Untermessungen' in col_b or 'Untermessungen' in col_c:
                    in_submeter_section = True
                    print(f"🔄 DEBUG Starte Unterzähler-Modus in Zeile {idx}")
                    continue  # Header überspringen
                
                # Zähler-ID in Spalte A erkannt -> Beendet Unterzähler-Modus und startet neuen Hauptzähler
                if col_a and ('CHINV' in col_a.upper() or col_a.startswith('XX')):
                    # Vorherigen Zähler abschließen
                    if current_zaehler:
                        result['zaehler_overview'].append(current_zaehler)
                    
                    # Unterzähler-Modus beenden (neuer Hauptzähler gefunden)
                    if in_submeter_section:
                        in_submeter_section = False
                        print(f"🔄 DEBUG Beende Unterzähler-Modus in Zeile {idx}")
                    
                    # Monats-Header aus derselben Zeile extrahieren (Spalten E-P)
                    current_month_columns = []
                    for col_idx in range(4, min(16, len(row))):  # Spalten E-P (4-15)
                        if col_idx < len(row):
                            month_name = str(row[col_idx]).strip()
                            if month_name in self.month_names:
                                current_month_columns.append(month_name)
                    
                    # Monats-Spalten für alle Zähler sammeln
                    if current_month_columns and not month_columns:
                        month_columns = current_month_columns
                        result['structure_info']['month_columns'] = month_columns
                    
                    # Neuen Hauptzähler starten
                    zaehler_count += 1
                    zaehler_type = 'hauptzaehler' if 'CHINV' in col_a.upper() else 'virtueller_zaehler'
                    
                    # Code und Name aus nächster Zeile
                    code_und_name = ''
                    if idx + 1 < len(df):
                        code_und_name = str(df.iloc[idx + 1, 0]).strip() if len(df.iloc[idx + 1]) > 0 else ''
                    
                    print(f"✅ DEBUG Erstelle Hauptzähler: {zaehler_type} - {col_a} - {code_und_name}")
                    
                    current_zaehler = {
                        'id': col_a,
                        'type': zaehler_type,
                        'code_und_name': code_und_name,
                        'messpunkte_count': 0,
                        'messpunkte_names': [],
                        'messpunkte_details': [],
                        'month_columns': current_month_columns,
                        'parent_id': None  # Hauptzähler haben keinen Parent
                    }
                
                # Unterzähler in Spalte B erkennen (nur im Unterzähler-Modus)
                elif in_submeter_section and col_b and ('CHINV' in col_b.upper() or col_b.startswith('XX')):
                    # Vorherigen Zähler abschließen
                    if current_zaehler:
                        result['zaehler_overview'].append(current_zaehler)
                    
                    # Monats-Header aus derselben Zeile extrahieren (Spalten E-P)
                    current_month_columns = []
                    for col_idx in range(4, min(16, len(row))):  # Spalten E-P (4-15)
                        if col_idx < len(row):
                            month_name = str(row[col_idx]).strip()
                            if month_name in self.month_names:
                                current_month_columns.append(month_name)
                    
                    print(f"🔍 DEBUG Unterzähler Monats-Header: {current_month_columns}")
                    
                    # Neuen Unterzähler starten
                    zaehler_count += 1
                    zaehler_type = 'unterzaehler' if 'CHINV' in col_b.upper() else 'virtueller_unterzaehler'
                    
                    # Code und Name aus nächster Zeile (Spalte B)
                    code_und_name = ''
                    if idx + 1 < len(df):
                        code_und_name = str(df.iloc[idx + 1, 1]).strip() if len(df.iloc[idx + 1]) > 1 else ''
                    
                    print(f"✅ DEBUG Erstelle Unterzähler: {zaehler_type} - {col_b} - {code_und_name}")
                    
                    current_zaehler = {
                        'id': col_b,
                        'type': zaehler_type,
                        'code_und_name': code_und_name,
                        'messpunkte_count': 0,
                        'messpunkte_names': [],
                        'messpunkte_details': [],
                        'month_columns': current_month_columns,
                        'parent_id': 'Hauptzähler'  # Unterzähler gehören zu Hauptzähler
                    }
                
                # Messpunkte erkennen (nach Zähler-ID)
                elif current_zaehler and not col_a.startswith('Untermessungen'):
                    # Für Unterzähler: Messpunkte können in verschiedenen Spalten stehen
                    messpunkt_candidates = []
                    
                    # Für Unterzähler: Messpunkte stehen hauptsächlich in Spalte B
                    if current_zaehler['type'] == 'unterzaehler':
                        if col_b and col_b != current_zaehler['code_und_name']:
                            messpunkt_candidates.append(('B', col_b))
                        # Auch Spalte A prüfen, falls dort Messpunkte stehen
                        if col_a and col_a != current_zaehler['code_und_name']:
                            messpunkt_candidates.append(('A', col_a))
                    else:
                        # Für Hauptzähler: Messpunkte stehen in Spalte A
                        if col_a and col_a != current_zaehler['code_und_name']:
                            messpunkt_candidates.append(('A', col_a))
                    
                    # Für jeden Kandidaten prüfen
                    for col_letter, messpunkt_text in messpunkt_candidates:
                        is_messpunkt = (
                            '[kWh]' in messpunkt_text or  # Standard kWh-Messpunkte
                            ('Bezug' in messpunkt_text and ('Netz' in messpunkt_text or 'lokal' in messpunkt_text)) or  # Bezug-Messpunkte
                            'Messung' in messpunkt_text or  # Messung-Messpunkte
                            ('Verbrauch' in messpunkt_text or 'Leistung' in messpunkt_text) or  # Andere Verbrauchs-Messpunkte
                            (current_zaehler['type'].startswith('virtuell') and len(messpunkt_text) > 5)  # Virtuelle Zähler: alles außer kurzen Titeln
                        )
                        
                        # Debug: Zeige Messpunkt-Erkennung
                        print(f"🔍 DEBUG Messpunkt-Prüfung ({col_letter}): '{messpunkt_text}' -> is_messpunkt={is_messpunkt} (Zähler: {current_zaehler['id']})")
                        
                        if is_messpunkt:
                            messpunkt_name = messpunkt_text
                            current_zaehler['messpunkte_names'].append(messpunkt_name)
                            current_zaehler['messpunkte_count'] += 1
                            total_messpunkte += 1
                            
                            # Werte aus Monats-Spalten extrahieren
                            messpunkt_values = {}
                            if current_zaehler['month_columns']:
                                for i, month_name in enumerate(current_zaehler['month_columns']):
                                    col_idx = 4 + i  # E=4, F=5, etc.
                                    if col_idx < len(row):
                                        value = row[col_idx]
                                        if pd.notna(value) and str(value).strip() != '':
                                            try:
                                                messpunkt_values[month_name] = float(value)
                                            except (ValueError, TypeError):
                                                messpunkt_values[month_name] = str(value)
                                        else:
                                            messpunkt_values[month_name] = 0.0
                                
                                print(f"🔍 DEBUG Messpunkt '{messpunkt_name}' Werte: {messpunkt_values}")
                            else:
                                print(f"⚠️ DEBUG Messpunkt '{messpunkt_name}' hat keine Monats-Spalten!")
                            
                            messpunkt_detail = {
                                'name': messpunkt_name,
                                'values': messpunkt_values
                            }
                            current_zaehler['messpunkte_details'].append(messpunkt_detail)
            
            # Letzten Zähler hinzufügen
            if current_zaehler:
                result['zaehler_overview'].append(current_zaehler)
            
            # Zusammenfassung aktualisieren
            result['summary']['total_zaehler'] = len(result['zaehler_overview'])
            result['summary']['total_messpunkte'] = total_messpunkte
            
            # Zähler-Typen zählen
            for zaehler in result['zaehler_overview']:
                if zaehler['type'] == 'hauptzaehler':
                    result['summary']['hauptzaehler'] += 1
                elif zaehler['type'] == 'unterzaehler':
                    result['summary']['unterzaehler'] += 1
                elif zaehler['type'].startswith('virtuell'):
                    result['summary']['virtuelle_zaehler'] += 1
            
            print(f"✅ SimpleZEVParser: {len(result['zaehler_overview'])} Zähler, {total_messpunkte} Messpunkte gefunden")
            
            # JSON-Test
            try:
                json.dumps(result)
                print("✅ SimpleZEVParser: JSON-Test erfolgreich")
            except Exception as json_error:
                print(f"❌ SimpleZEVParser: JSON-Fehler: {json_error}")
                result['structure_verified'] = False
                result['structure_info']['errors'].append(f"JSON-Serialisierung fehlgeschlagen: {json_error}")
            
            return result
            
        except Exception as e:
            print(f"❌ SimpleZEVParser: Fehler: {e}")
            return {
                'file_name': Path(file_path).name,
                'structure_verified': False,
                'structure_info': {'errors': [str(e)], 'warnings': []},
                'summary': {'total_zaehler': 0, 'total_messpunkte': 0},
                'zaehler_overview': []
            }