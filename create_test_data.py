#!/usr/bin/env python3
"""
Script zum Erstellen von Test-Excel-Dateien für STWEG
"""

import pandas as pd
from datetime import datetime, timedelta
import random
from pathlib import Path


def create_sample_excel():
    """Erstellt eine Beispieldatei für Tests"""
    
    # Verzeichnis erstellen
    sample_dir = Path("data/sample")
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # Testdaten generieren
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(hours=i) for i in range(24)]
    
    # Verbrauchsdaten generieren
    data = {
        'Zeitstempel': dates,
        'Gesamtverbrauch': [100 + random.uniform(-10, 10) for _ in range(24)],
        'Eigentümer_1': [25 + random.uniform(-5, 5) for _ in range(24)],
        'Eigentümer_2': [30 + random.uniform(-5, 5) for _ in range(24)],
        'Eigentümer_3': [45 + random.uniform(-5, 5) for _ in range(24)],
    }
    
    df_consumption = pd.DataFrame(data)
    
    # Eigentümer-Daten
    owners_data = {
        'Eigentümer_ID': [1, 2, 3, 4, 5, 6, 7],
        'Name': ['Müller', 'Schmidt', 'Weber', 'Fischer', 'Wagner', 'Becker', 'Schulz'],
        'Wohnung': ['1A', '1B', '2A', '2B', '3A', '3B', '4A'],
        'Anteil': [0.14, 0.14, 0.14, 0.14, 0.14, 0.15, 0.15]
    }
    
    df_owners = pd.DataFrame(owners_data)
    
    # Excel-Datei erstellen
    with pd.ExcelWriter(sample_dir / "test_data.xlsx", engine='openpyxl') as writer:
        df_consumption.to_excel(writer, sheet_name='Verbrauchsdaten', index=False)
        df_owners.to_excel(writer, sheet_name='Eigentümer', index=False)
    
    print(f"Test-Excel-Datei erstellt: {sample_dir / 'test_data.xlsx'}")
    print("Inhalt:")
    print("- Sheet 'Verbrauchsdaten': 24 Stunden Verbrauchsdaten")
    print("- Sheet 'Eigentümer': 7 Eigentümer mit Anteilen")


if __name__ == "__main__":
    create_sample_excel()
