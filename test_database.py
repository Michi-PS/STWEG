#!/usr/bin/env python3
"""
Test-Script für die Datenbank-Modelle
Kann ohne Terminal ausgeführt werden
"""

import sys
import os

# Python-Pfad erweitern
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_database_setup():
    """Testet die Datenbank-Einrichtung"""
    try:
        from models.models import Base, Eigentuemer, Messpunkt, Verbrauchsdaten, Rechnung
        from models.database import create_tables, get_db_session
        
        print("✅ Modelle erfolgreich importiert")
        
        # Tabellen erstellen
        create_tables()
        print("✅ Datenbank-Tabellen erstellt")
        
        # Session erstellen
        session = get_db_session()
        print("✅ Datenbank-Session erstellt")
        
        # Test: Eigentümer erstellen
        eigentuemer = Eigentuemer(
            name="Test Eigentümer",
            wohnung="1A",
            anteil=0.14,
            email="test@example.com"
        )
        session.add(eigentuemer)
        session.commit()
        print(f"✅ Eigentümer erstellt: {eigentuemer}")
        
        # Test: Messpunkt erstellen
        messpunkt = Messpunkt(
            name="Test_Messpunkt",
            typ="individual",
            eigentuemer_id=eigentuemer.id
        )
        session.add(messpunkt)
        session.commit()
        print(f"✅ Messpunkt erstellt: {messpunkt}")
        
        # Test: Verbrauchsdaten erstellen
        from datetime import datetime
        verbrauch = Verbrauchsdaten(
            zeitstempel=datetime(2024, 1, 1, 12, 0, 0),
            messpunkt_id=messpunkt.id,
            verbrauch=25.5,
            kosten=12.75,
            periode="2024-01"
        )
        session.add(verbrauch)
        session.commit()
        print(f"✅ Verbrauchsdaten erstellt: {verbrauch}")
        
        # Test: Rechnung erstellen
        from datetime import date
        rechnung = Rechnung(
            rechnungsnummer="R-TEST-001",
            rechnungsdatum=date(2024, 1, 15),
            rechnungssteller="Test Rechnungssteller",
            betrag=100.0,
            kategorie="Strom",
            periode="2024-01"
        )
        session.add(rechnung)
        session.commit()
        print(f"✅ Rechnung erstellt: {rechnung}")
        
        session.close()
        print("\n🎉 Alle Datenbank-Tests erfolgreich!")
        return True
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model_relationships():
    """Testet die Beziehungen zwischen den Modellen"""
    try:
        from models.models import Base, Eigentuemer, Messpunkt, Verbrauchsdaten
        from models.database import get_db_session
        
        # Neue Session mit leerer Datenbank
        session = get_db_session()
        
        # Erst alle Tabellen löschen
        from models.database import drop_tables, create_tables
        drop_tables()
        create_tables()
        
        # Beispieldaten erstellen
        eigentuemer_list = Eigentuemer.create_sample_data(session)
        eigentuemer = eigentuemer_list[0]
        
        # Messpunkte erstellen (ohne create_sample_data, da das Konflikte verursacht)
        messpunkt = Messpunkt(
            name="Eigentümer_1",
            typ="individual",
            eigentuemer_id=eigentuemer.id
        )
        session.add(messpunkt)
        session.commit()
        
        # Beziehungen testen
        assert len(eigentuemer.messpunkte) > 0
        print("✅ Eigentümer-Messpunkt Beziehung funktioniert")
        
        assert messpunkt.eigentuemer.id == eigentuemer.id
        print("✅ Messpunkt-Eigentümer Beziehung funktioniert")
        
        session.close()
        print("✅ Alle Beziehungs-Tests erfolgreich!")
        return True
        
    except Exception as e:
        print(f"❌ Beziehungs-Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model_validations():
    """Testet die Validierungen der Modelle"""
    try:
        from models.models import Eigentuemer, Messpunkt, Verbrauchsdaten, Rechnung
        
        # Test: Eigentümer-Validierung
        try:
            eigentuemer = Eigentuemer(
                name="Test",
                wohnung="1A",
                anteil=1.5,  # Ungültig: > 1.0
                email="test@example.com"
            )
            print("❌ Eigentümer-Validierung fehlgeschlagen")
            return False
        except ValueError:
            print("✅ Eigentümer-Validierung funktioniert")
        
        # Test: Messpunkt-Validierung
        try:
            messpunkt = Messpunkt(
                name="Test",
                typ="invalid_type",  # Ungültig
                eigentuemer_id=1
            )
            print("❌ Messpunkt-Validierung fehlgeschlagen")
            return False
        except ValueError:
            print("✅ Messpunkt-Validierung funktioniert")
        
        # Test: Verbrauchsdaten-Validierung
        try:
            from datetime import datetime
            verbrauch = Verbrauchsdaten(
                zeitstempel=datetime(2024, 1, 1, 12, 0, 0),
                messpunkt_id=1,
                verbrauch=25.5,
                kosten=12.75,
                periode="2024/01"  # Ungültiges Format
            )
            print("❌ Verbrauchsdaten-Validierung fehlgeschlagen")
            return False
        except ValueError:
            print("✅ Verbrauchsdaten-Validierung funktioniert")
        
        print("✅ Alle Validierungs-Tests erfolgreich!")
        return True
        
    except Exception as e:
        print(f"❌ Validierungs-Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 STWEG Datenbank-Tests")
    print("=" * 50)
    
    # Tests ausführen
    test1 = test_database_setup()
    print("\n" + "=" * 50)
    
    test2 = test_model_relationships()
    print("\n" + "=" * 50)
    
    test3 = test_model_validations()
    print("\n" + "=" * 50)
    
    # Ergebnis
    if test1 and test2 and test3:
        print("🎉 ALLE TESTS ERFOLGREICH!")
        sys.exit(0)
    else:
        print("❌ EINIGE TESTS FEHLGESCHLAGEN!")
        sys.exit(1)
