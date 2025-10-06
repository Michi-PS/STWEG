#!/usr/bin/env python3
"""
CLI für STWEG - Stockwerkeigentümergesellschaft Nebenkostenverwaltung
"""

import argparse
import sys
from pathlib import Path
from excel_analysis.excel_analyzer import ExcelAnalyzer


def main():
    """Hauptfunktion der CLI"""
    parser = argparse.ArgumentParser(
        description="STWEG - Stockwerkeigentümergesellschaft Nebenkostenverwaltung"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Verfügbare Befehle')
    
    # Excel-Analyse Befehl
    excel_parser = subparsers.add_parser('analyze', help='Excel-Datei analysieren')
    excel_parser.add_argument('file', help='Pfad zur Excel-Datei')
    excel_parser.add_argument('--report', '-r', action='store_true', 
                             help='Detaillierten Bericht ausgeben')
    excel_parser.add_argument('--output', '-o', help='Bericht in Datei speichern')
    
    # Validierung Befehl
    validate_parser = subparsers.add_parser('validate', help='Excel-Datei validieren')
    validate_parser.add_argument('file', help='Pfad zur Excel-Datei')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        analyze_excel(args)
    elif args.command == 'validate':
        validate_excel(args)
    else:
        parser.print_help()


def analyze_excel(args):
    """Analysiert eine Excel-Datei"""
    try:
        analyzer = ExcelAnalyzer()
        result = analyzer.analyze_file(args.file)
        
        if args.report:
            report = analyzer.generate_report(result)
            print(report)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"\nBericht gespeichert in: {args.output}")
        else:
            # Kurze Ausgabe
            print(f"Datei: {result['file_path']}")
            print(f"Tabellenblätter: {', '.join(result['sheets'])}")
            print(f"Status: {result['validation_status']}")
            
            if result['validation_errors']:
                print(f"Fehler: {len(result['validation_errors'])} gefunden")
                for error in result['validation_errors'][:3]:  # Erste 3 Fehler
                    print(f"  - {error}")
    
    except FileNotFoundError:
        print(f"Fehler: Datei nicht gefunden: {args.file}")
        sys.exit(1)
    except Exception as e:
        print(f"Fehler: {e}")
        sys.exit(1)


def validate_excel(args):
    """Validiert eine Excel-Datei"""
    try:
        analyzer = ExcelAnalyzer()
        result = analyzer.analyze_file(args.file)
        
        if result['validation_status'] == 'valid':
            print("✓ Excel-Datei ist gültig")
            sys.exit(0)
        else:
            print("✗ Excel-Datei hat Validierungsfehler:")
            for error in result['validation_errors']:
                print(f"  - {error}")
            sys.exit(1)
    
    except Exception as e:
        print(f"Fehler: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

