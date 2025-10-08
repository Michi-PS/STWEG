#!/usr/bin/env python3
"""
STWEG Eigentümer-Import Script

Dieses Script importiert Eigentümer-Daten aus der Excel-Datei 
'data/sample/Eigentümer.xlsx' in das STWEG-System.

Verwendung:
    python scripts/import_eigentuemer.py [--clean] [--file path/to/file.xlsx]

Optionen:
    --clean    Löscht alle bestehenden Eigentümer-Daten vor dem Import
    --file     Pfad zur Excel-Datei (Standard: data/sample/Eigentümer.xlsx)
"""

import sys
import os
import argparse
import pandas as pd
import requests
import json
from datetime import datetime

# Projekt-Root zum Python-Pfad hinzufügen
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def load_excel_data(file_path):
    """Lädt Eigentümer-Daten aus Excel-Datei"""
    try:
        df = pd.read_excel(file_path)
        print(f"📊 Excel-Datei geladen: {file_path}")
        print(f"   - Spalten: {list(df.columns)}")
        print(f"   - Zeilen: {len(df)}")
        return df
    except Exception as e:
        print(f"❌ Fehler beim Laden der Excel-Datei: {e}")
        return None

def clean_existing_data():
    """Löscht alle bestehenden Eigentümer-Daten"""
    try:
        print("🗑️  Lösche bestehende Eigentümer-Daten...")
        
        # Alle Eigentümer abrufen
        response = requests.get('http://localhost:8080/api/eigentuemer')
        if response.status_code != 200:
            print(f"⚠️  Warnung: API nicht erreichbar ({response.status_code})")
            return False
            
        data = response.json()
        eigentuemer_list = data.get('eigentuemer', [])
        
        # Alle deaktivieren (soft delete)
        deleted_count = 0
        for eig in eigentuemer_list:
            delete_response = requests.delete(f'http://localhost:8080/api/eigentuemer/{eig["id"]}')
            if delete_response.status_code == 200:
                deleted_count += 1
                print(f"   ✅ Deaktiviert: {eig['name']}")
        
        print(f"🗑️  {deleted_count} Eigentümer deaktiviert")
        return True
        
    except Exception as e:
        print(f"⚠️  Warnung beim Löschen: {e}")
        return False

def import_eigentuemer_data(df, api_url='http://localhost:8080'):
    """Importiert Eigentümer-Daten über API"""
    imported_count = 0
    errors = []
    
    print(f"📥 Importiere {len(df)} Eigentümer-Datensätze...")
    
    for idx, row in df.iterrows():
        try:
            # Namen kombinieren
            name1 = str(row['Name 1']) if pd.notna(row['Name 1']) else ''
            name2 = str(row['Name 2']) if pd.notna(row['Name 2']) else ''
            
            if name1 and name2:
                full_name = f'{name1} & {name2}'
            elif name1:
                full_name = name1
            else:
                full_name = 'Unbekannt'
            
            # Promille zu Anteil umrechnen
            anteil = row['Promille'] / 1000.0
            anteil_prozent = row['Promille'] / 10.0
            
            # Eigentümer-Daten
            eigentuemer_data = {
                'name': full_name,
                'wohnung': str(row['Wohnung']),
                'anteil': anteil,
                'anteil_prozent': anteil_prozent,
                'email': None,
                'telefon': None,
                'aktiv': True
            }
            
            # Über API erstellen
            response = requests.post(f'{api_url}/api/eigentuemer', json=eigentuemer_data)
            
            if response.status_code == 201:
                imported_count += 1
                print(f"   ✅ {full_name} (Wohnung {row['Wohnung']}, {row['Promille']}‰)")
            else:
                error_msg = f"{full_name}: {response.status_code} - {response.text}"
                errors.append(error_msg)
                print(f"   ❌ {error_msg}")
                
        except Exception as e:
            error_msg = f"Zeile {idx}: {e}"
            errors.append(error_msg)
            print(f"   ❌ {error_msg}")
    
    return imported_count, errors

def verify_import(api_url='http://localhost:8080'):
    """Verifiziert den Import"""
    try:
        response = requests.get(f'{api_url}/api/eigentuemer')
        if response.status_code == 200:
            data = response.json()
            eigentuemer_list = data.get('eigentuemer', [])
            
            print(f"\n📊 Verifikation:")
            print(f"   - Gesamt Eigentümer: {data['total_count']}")
            print(f"   - Aktive Eigentümer: {data['active_count']}")
            
            total_anteil = sum([e['anteil'] for e in eigentuemer_list])
            print(f"   - Gesamt Anteil: {total_anteil:.3f} ({total_anteil*100:.1f}%)")
            
            print(f"\n📋 Importierte Eigentümer:")
            for eig in eigentuemer_list:
                print(f"   - {eig['name']} (Wohnung {eig['wohnung']}, {eig['anteil_prozent']:.1f}%)")
            
            return True
        else:
            print(f"❌ Verifikation fehlgeschlagen: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Verifikations-Fehler: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Importiert Eigentümer-Daten aus Excel')
    parser.add_argument('--clean', action='store_true', 
                       help='Löscht alle bestehenden Eigentümer-Daten vor dem Import')
    parser.add_argument('--file', default='data/sample/Eigentümer.xlsx',
                       help='Pfad zur Excel-Datei (Standard: data/sample/Eigentümer.xlsx)')
    parser.add_argument('--api-url', default='http://localhost:8080',
                       help='API-URL (Standard: http://localhost:8080)')
    
    args = parser.parse_args()
    
    print("🏠 STWEG Eigentümer-Import")
    print("=" * 50)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Datei: {args.file}")
    print(f"🌐 API: {args.api_url}")
    print()
    
    # Excel-Datei laden
    df = load_excel_data(args.file)
    if df is None:
        sys.exit(1)
    
    # Bestehende Daten löschen (optional)
    if args.clean:
        if not clean_existing_data():
            print("⚠️  Warnung: Bereinigung fehlgeschlagen, aber Import wird fortgesetzt")
        print()
    
    # Daten importieren
    imported_count, errors = import_eigentuemer_data(df, args.api_url)
    
    print(f"\n🎉 Import abgeschlossen!")
    print(f"   ✅ Erfolgreich importiert: {imported_count}")
    if errors:
        print(f"   ❌ Fehler: {len(errors)}")
        for error in errors:
            print(f"      - {error}")
    
    # Verifikation
    if imported_count > 0:
        print()
        verify_import(args.api_url)
    
    print(f"\n💡 Nächste Schritte:")
    print(f"   - Web-Interface: {args.api_url}")
    print(f"   - Eigentümer-Modul aufrufen")
    print(f"   - Export-Funktionen testen")
    print(f"   - Daten über UX bearbeiten")

if __name__ == '__main__':
    main()
