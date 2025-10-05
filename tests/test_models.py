"""
Tests für Datenmodelle - STWEG
Test-Driven Development für Phase 2: Datenmodelle & Grundstrukturen
"""

import pytest
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Import der zu entwickelnden Modelle
from src.models.models import Base, Eigentuemer, Messpunkt, Verbrauchsdaten, Rechnung
from src.models.database import get_session


class TestEigentuemerModel:
    """Test-Klasse für Eigentümer-Datenmodell"""
    
    @pytest.fixture
    def db_session(self):
        """Erstellt eine temporäre Datenbank für Tests"""
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
        session.close()
    
    def test_eigentuemer_creation(self, db_session):
        """Test: Eigentümer kann erstellt werden"""
        eigentuemer = Eigentuemer(
            name="Max Mustermann",
            wohnung="1A",
            anteil=0.14,
            email="max.mustermann@example.com",
            aktiv=True
        )
        
        db_session.add(eigentuemer)
        db_session.commit()
        
        # Überprüfung
        assert eigentuemer.id is not None
        assert eigentuemer.name == "Max Mustermann"
        assert eigentuemer.wohnung == "1A"
        assert eigentuemer.anteil == 0.14
        assert eigentuemer.email == "max.mustermann@example.com"
        assert eigentuemer.aktiv is True
    
    def test_eigentuemer_required_fields(self, db_session):
        """Test: Erforderliche Felder werden validiert"""
        # Test ohne Name
        with pytest.raises(IntegrityError):
            eigentuemer = Eigentuemer(
                wohnung="1A",
                anteil=0.14,
                email="test@example.com"
            )
            db_session.add(eigentuemer)
            db_session.commit()
    
    def test_eigentuemer_anteil_validation(self, db_session):
        """Test: Anteil muss zwischen 0 und 1 liegen"""
        # Gültiger Anteil
        eigentuemer = Eigentuemer(
            name="Test",
            wohnung="1A",
            anteil=0.5,
            email="test@example.com"
        )
        db_session.add(eigentuemer)
        db_session.commit()
        
        # Ungültiger Anteil (> 1)
        with pytest.raises(ValueError):
            eigentuemer = Eigentuemer(
                name="Test2",
                wohnung="1B",
                anteil=1.5,
                email="test2@example.com"
            )
    
    def test_eigentuemer_wohnung_unique(self, db_session):
        """Test: Wohnung muss eindeutig sein"""
        eigentuemer1 = Eigentuemer(
            name="Person 1",
            wohnung="1A",
            anteil=0.14,
            email="person1@example.com"
        )
        
        eigentuemer2 = Eigentuemer(
            name="Person 2",
            wohnung="1A",  # Gleiche Wohnung
            anteil=0.14,
            email="person2@example.com"
        )
        
        db_session.add(eigentuemer1)
        db_session.commit()
        
        with pytest.raises(IntegrityError):
            db_session.add(eigentuemer2)
            db_session.commit()
    
    def test_eigentuemer_string_representation(self, db_session):
        """Test: String-Darstellung des Eigentümers"""
        eigentuemer = Eigentuemer(
            name="Max Mustermann",
            wohnung="1A",
            anteil=0.14,
            email="max@example.com"
        )
        
        db_session.add(eigentuemer)
        db_session.commit()
        
        assert str(eigentuemer) == "Eigentuemer(1A - Max Mustermann)"
        assert repr(eigentuemer) == f"<Eigentuemer(id={eigentuemer.id}, wohnung='1A', name='Max Mustermann')>"


class TestMesspunktModel:
    """Test-Klasse für Messpunkt-Datenmodell"""
    
    @pytest.fixture
    def db_session(self):
        """Erstellt eine temporäre Datenbank für Tests"""
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
        session.close()
    
    @pytest.fixture
    def sample_eigentuemer(self, db_session):
        """Erstellt einen Beispiel-Eigentümer"""
        eigentuemer = Eigentuemer(
            name="Max Mustermann",
            wohnung="1A",
            anteil=0.14,
            email="max@example.com"
        )
        db_session.add(eigentuemer)
        db_session.commit()
        return eigentuemer
    
    def test_messpunkt_creation(self, db_session, sample_eigentuemer):
        """Test: Messpunkt kann erstellt werden"""
        messpunkt = Messpunkt(
            name="Eigentümer_1",
            typ="individual",
            eigentuemer_id=sample_eigentuemer.id,
            aktiv=True
        )
        
        db_session.add(messpunkt)
        db_session.commit()
        
        assert messpunkt.id is not None
        assert messpunkt.name == "Eigentümer_1"
        assert messpunkt.typ == "individual"
        assert messpunkt.eigentuemer_id == sample_eigentuemer.id
        assert messpunkt.aktiv is True
    
    def test_messpunkt_types(self, db_session, sample_eigentuemer):
        """Test: Verschiedene Messpunkt-Typen"""
        # Individual-Messpunkt
        individual = Messpunkt(
            name="Eigentümer_1",
            typ="individual",
            eigentuemer_id=sample_eigentuemer.id
        )
        
        # Gemeinschafts-Messpunkt
        gemeinschaft = Messpunkt(
            name="Gemeinschaft",
            typ="gemeinschaft",
            eigentuemer_id=None
        )
        
        db_session.add_all([individual, gemeinschaft])
        db_session.commit()
        
        assert individual.typ == "individual"
        assert gemeinschaft.typ == "gemeinschaft"
        assert gemeinschaft.eigentuemer_id is None
    
    def test_messpunkt_eigentuemer_relationship(self, db_session, sample_eigentuemer):
        """Test: Verknüpfung zwischen Messpunkt und Eigentümer"""
        messpunkt = Messpunkt(
            name="Eigentümer_1",
            typ="individual",
            eigentuemer_id=sample_eigentuemer.id
        )
        
        db_session.add(messpunkt)
        db_session.commit()
        
        # Überprüfung der Beziehung
        assert messpunkt.eigentuemer.id == sample_eigentuemer.id
        assert messpunkt in sample_eigentuemer.messpunkte


class TestVerbrauchsdatenModel:
    """Test-Klasse für Verbrauchsdaten-Modell"""
    
    @pytest.fixture
    def db_session(self):
        """Erstellt eine temporäre Datenbank für Tests"""
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
        session.close()
    
    @pytest.fixture
    def sample_messpunkt(self, db_session):
        """Erstellt einen Beispiel-Messpunkt"""
        eigentuemer = Eigentuemer(
            name="Max Mustermann",
            wohnung="1A",
            anteil=0.14,
            email="max@example.com"
        )
        db_session.add(eigentuemer)
        db_session.commit()
        
        messpunkt = Messpunkt(
            name="Eigentümer_1",
            typ="individual",
            eigentuemer_id=eigentuemer.id
        )
        db_session.add(messpunkt)
        db_session.commit()
        return messpunkt
    
    def test_verbrauchsdaten_creation(self, db_session, sample_messpunkt):
        """Test: Verbrauchsdaten können erstellt werden"""
        zeitstempel = datetime(2024, 1, 1, 12, 0, 0)
        
        verbrauch = Verbrauchsdaten(
            zeitstempel=zeitstempel,
            messpunkt_id=sample_messpunkt.id,
            verbrauch=25.5,
            kosten=12.75,
            periode="2024-01"
        )
        
        db_session.add(verbrauch)
        db_session.commit()
        
        assert verbrauch.id is not None
        assert verbrauch.zeitstempel == zeitstempel
        assert verbrauch.messpunkt_id == sample_messpunkt.id
        assert verbrauch.verbrauch == 25.5
        assert verbrauch.kosten == 12.75
        assert verbrauch.periode == "2024-01"
    
    def test_verbrauchsdaten_messpunkt_relationship(self, db_session, sample_messpunkt):
        """Test: Verknüpfung zwischen Verbrauchsdaten und Messpunkt"""
        verbrauch = Verbrauchsdaten(
            zeitstempel=datetime(2024, 1, 1, 12, 0, 0),
            messpunkt_id=sample_messpunkt.id,
            verbrauch=25.5,
            kosten=12.75,
            periode="2024-01"
        )
        
        db_session.add(verbrauch)
        db_session.commit()
        
        assert verbrauch.messpunkt.id == sample_messpunkt.id
        assert verbrauch in sample_messpunkt.verbrauchsdaten
    
    def test_verbrauchsdaten_periode_format(self, db_session, sample_messpunkt):
        """Test: Periode muss YYYY-MM Format haben"""
        # Gültige Periode
        verbrauch = Verbrauchsdaten(
            zeitstempel=datetime(2024, 1, 1, 12, 0, 0),
            messpunkt_id=sample_messpunkt.id,
            verbrauch=25.5,
            kosten=12.75,
            periode="2024-01"
        )
        
        db_session.add(verbrauch)
        db_session.commit()
        
        assert verbrauch.periode == "2024-01"
        
        # Ungültige Periode
        with pytest.raises(ValueError):
            verbrauch2 = Verbrauchsdaten(
                zeitstempel=datetime(2024, 1, 1, 12, 0, 0),
                messpunkt_id=sample_messpunkt.id,
                verbrauch=25.5,
                kosten=12.75,
                periode="2024/01"  # Falsches Format
            )


class TestRechnungModel:
    """Test-Klasse für Rechnungs-Datenmodell"""
    
    @pytest.fixture
    def db_session(self):
        """Erstellt eine temporäre Datenbank für Tests"""
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
        session.close()
    
    def test_rechnung_creation(self, db_session):
        """Test: Rechnung kann erstellt werden"""
        rechnung = Rechnung(
            rechnungsnummer="R-2024-001",
            rechnungsdatum=date(2024, 1, 15),
            rechnungssteller="Elektrizitätswerk Zürich",
            betrag=1250.50,
            kategorie="Strom",
            periode="2024-01",
            pdf_pfad="/data/rechnungen/strom_2024_01.pdf"
        )
        
        db_session.add(rechnung)
        db_session.commit()
        
        assert rechnung.id is not None
        assert rechnung.rechnungsnummer == "R-2024-001"
        assert rechnung.rechnungsdatum == date(2024, 1, 15)
        assert rechnung.rechnungssteller == "Elektrizitätswerk Zürich"
        assert rechnung.betrag == 1250.50
        assert rechnung.kategorie == "Strom"
        assert rechnung.periode == "2024-01"
        assert rechnung.pdf_pfad == "/data/rechnungen/strom_2024_01.pdf"
    
    def test_rechnung_kategorien(self, db_session):
        """Test: Verschiedene Rechnungskategorien"""
        kategorien = ["Strom", "Heizung", "Wasser", "Versicherung", "Hauswart"]
        
        rechnungen = []
        for i, kategorie in enumerate(kategorien):
            rechnung = Rechnung(
                rechnungsnummer=f"R-2024-{i+1:03d}",
                rechnungsdatum=date(2024, 1, 15),
                rechnungssteller=f"Anbieter {kategorie}",
                betrag=100.0 + i * 50,
                kategorie=kategorie,
                periode="2024-01"
            )
            rechnungen.append(rechnung)
        
        db_session.add_all(rechnungen)
        db_session.commit()
        
        for rechnung in rechnungen:
            assert rechnung.kategorie in kategorien
    
    def test_rechnung_periode_validation(self, db_session):
        """Test: Periode-Validierung für Rechnungen"""
        # Gültige Periode
        rechnung = Rechnung(
            rechnungsnummer="R-2024-001",
            rechnungsdatum=date(2024, 1, 15),
            rechnungssteller="Test",
            betrag=100.0,
            kategorie="Strom",
            periode="2024-01"
        )
        
        db_session.add(rechnung)
        db_session.commit()
        
        assert rechnung.periode == "2024-01"


class TestModelRelationships:
    """Test-Klasse für Modell-Beziehungen"""
    
    @pytest.fixture
    def db_session(self):
        """Erstellt eine temporäre Datenbank für Tests"""
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
        session.close()
    
    def test_complete_relationship_chain(self, db_session):
        """Test: Vollständige Beziehungskette von Eigentümer zu Verbrauchsdaten"""
        # Eigentümer erstellen
        eigentuemer = Eigentuemer(
            name="Max Mustermann",
            wohnung="1A",
            anteil=0.14,
            email="max@example.com"
        )
        db_session.add(eigentuemer)
        db_session.commit()
        
        # Messpunkt erstellen
        messpunkt = Messpunkt(
            name="Eigentümer_1",
            typ="individual",
            eigentuemer_id=eigentuemer.id
        )
        db_session.add(messpunkt)
        db_session.commit()
        
        # Verbrauchsdaten erstellen
        verbrauch = Verbrauchsdaten(
            zeitstempel=datetime(2024, 1, 1, 12, 0, 0),
            messpunkt_id=messpunkt.id,
            verbrauch=25.5,
            kosten=12.75,
            periode="2024-01"
        )
        db_session.add(verbrauch)
        db_session.commit()
        
        # Beziehungen testen
        assert verbrauch.messpunkt.eigentuemer.id == eigentuemer.id
        assert verbrauch in eigentuemer.verbrauchsdaten
        assert len(eigentuemer.verbrauchsdaten) == 1


if __name__ == "__main__":
    pytest.main([__file__])
