"""
Rechnungs-Datenmodell für STWEG
Repräsentiert die Nebenkosten-Rechnungen (PDF-Dateien)
"""

import re
from datetime import date
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Rechnung(Base):
    """
    Rechnungs-Datenmodell
    
    Repräsentiert eine Nebenkosten-Rechnung (PDF-Datei).
    Enthält alle relevanten Informationen für die Kostenverteilung.
    """
    
    __tablename__ = 'rechnungen'
    
    # Primärschlüssel
    id = Column(Integer, primary_key=True, index=True)
    
    # Rechnungsdaten
    rechnungsnummer = Column(String(50), nullable=False, unique=True, index=True)
    rechnungsdatum = Column(Date, nullable=False, index=True)
    rechnungssteller = Column(String(100), nullable=False, index=True)
    
    # Finanzielle Daten
    betrag = Column(Float, nullable=False)  # Gesamtbetrag in CHF
    
    # Kategorisierung
    kategorie = Column(String(50), nullable=False, index=True)  # z.B. "Strom", "Heizung", "Wasser"
    
    # Periode
    periode = Column(String(7), nullable=False, index=True)  # YYYY-MM Format
    
    # Datei-Informationen
    pdf_pfad = Column(String(500), nullable=True)  # Pfad zur PDF-Datei
    pdf_original_name = Column(String(255), nullable=True)  # Original-Dateiname
    
    # Status
    verarbeitet = Column(String(20), default='pending', nullable=False)  # pending, processed, error
    
    # Zeitstempel
    erstellt_am = Column(DateTime(timezone=True), server_default=func.now())
    aktualisiert_am = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Indizes für bessere Performance
    __table_args__ = (
        Index('idx_kategorie_periode', 'kategorie', 'periode'),
        Index('idx_rechnungssteller_periode', 'rechnungssteller', 'periode'),
    )
    
    def __init__(self, **kwargs):
        """Initialisierung mit Validierung"""
        # Periode validieren
        if 'periode' in kwargs:
            periode = kwargs['periode']
            if not self._validate_periode_format(periode):
                raise ValueError(f"Periode muss im Format YYYY-MM sein, erhalten: {periode}")
        
        # Betrag validieren
        if 'betrag' in kwargs:
            betrag = kwargs['betrag']
            if betrag < 0:
                raise ValueError(f"Betrag darf nicht negativ sein, erhalten: {betrag}")
        
        # Rechnungsdatum validieren
        if 'rechnungsdatum' in kwargs:
            rechnungsdatum = kwargs['rechnungsdatum']
            if not isinstance(rechnungsdatum, date):
                raise ValueError(f"Rechnungsdatum muss ein date-Objekt sein, erhalten: {type(rechnungsdatum)}")
        
        # Status validieren
        if 'verarbeitet' in kwargs:
            status = kwargs['verarbeitet']
            if status not in ['pending', 'processed', 'error']:
                raise ValueError(f"Status muss 'pending', 'processed' oder 'error' sein, erhalten: {status}")
        
        super().__init__(**kwargs)
    
    def __repr__(self):
        """String-Repräsentation für Debugging"""
        return f"<Rechnung(id={self.id}, rechnungsnummer='{self.rechnungsnummer}', kategorie='{self.kategorie}', betrag={self.betrag})>"
    
    def __str__(self):
        """Benutzerfreundliche String-Darstellung"""
        return f"Rechnung({self.rechnungsnummer} - {self.kategorie} - {self.betrag} CHF)"
    
    @staticmethod
    def _validate_periode_format(periode):
        """Validiert das Periode-Format (YYYY-MM)"""
        if not isinstance(periode, str):
            return False
        
        pattern = r'^\d{4}-\d{2}$'
        if not re.match(pattern, periode):
            return False
        
        # Zusätzliche Validierung: Jahr und Monat
        try:
            year, month = periode.split('-')
            year = int(year)
            month = int(month)
            
            if not (1900 <= year <= 2100):
                return False
            
            if not (1 <= month <= 12):
                return False
            
            return True
        except (ValueError, TypeError):
            return False
    
    @property
    def jahr(self):
        """Gibt das Jahr aus der Periode zurück"""
        return int(self.periode.split('-')[0])
    
    @property
    def monat(self):
        """Gibt den Monat aus der Periode zurück"""
        return int(self.periode.split('-')[1])
    
    @property
    def is_pending(self):
        """Prüft, ob die Rechnung noch verarbeitet werden muss"""
        return self.verarbeitet == 'pending'
    
    @property
    def is_processed(self):
        """Prüft, ob die Rechnung bereits verarbeitet wurde"""
        return self.verarbeitet == 'processed'
    
    @property
    def has_error(self):
        """Prüft, ob bei der Verarbeitung ein Fehler aufgetreten ist"""
        return self.verarbeitet == 'error'
    
    @classmethod
    def get_by_periode(cls, session, periode):
        """Gibt alle Rechnungen für eine Periode zurück"""
        return session.query(cls).filter(cls.periode == periode).all()
    
    @classmethod
    def get_by_kategorie(cls, session, kategorie):
        """Gibt alle Rechnungen einer Kategorie zurück"""
        return session.query(cls).filter(cls.kategorie == kategorie).all()
    
    @classmethod
    def get_by_kategorie_and_periode(cls, session, kategorie, periode):
        """Gibt Rechnungen für eine Kategorie und Periode zurück"""
        return session.query(cls).filter(
            cls.kategorie == kategorie,
            cls.periode == periode
        ).all()
    
    @classmethod
    def get_pending_rechnungen(cls, session):
        """Gibt alle ausstehenden Rechnungen zurück"""
        return session.query(cls).filter(cls.verarbeitet == 'pending').all()
    
    @classmethod
    def get_total_betrag_periode(cls, session, periode):
        """Berechnet den Gesamtbetrag aller Rechnungen einer Periode"""
        result = session.query(func.sum(cls.betrag)).filter(cls.periode == periode).scalar()
        return result or 0.0
    
    @classmethod
    def get_total_betrag_kategorie_periode(cls, session, kategorie, periode):
        """Berechnet den Gesamtbetrag einer Kategorie für eine Periode"""
        result = session.query(func.sum(cls.betrag)).filter(
            cls.kategorie == kategorie,
            cls.periode == periode
        ).scalar()
        return result or 0.0
    
    @classmethod
    def get_betrag_by_kategorie_periode(cls, session, periode):
        """Gibt Beträge gruppiert nach Kategorie für eine Periode zurück"""
        from sqlalchemy import func
        return session.query(
            cls.kategorie,
            func.sum(cls.betrag).label('total_betrag'),
            func.count(cls.id).label('anzahl_rechnungen')
        ).filter(
            cls.periode == periode
        ).group_by(cls.kategorie).all()
    
    @classmethod
    def get_available_kategorien(cls, session):
        """Gibt alle verfügbaren Kategorien zurück"""
        result = session.query(cls.kategorie).distinct().all()
        return [row[0] for row in result]
    
    @classmethod
    def get_available_perioden(cls, session):
        """Gibt alle verfügbaren Perioden zurück"""
        result = session.query(cls.periode).distinct().order_by(cls.periode).all()
        return [row[0] for row in result]
    
    def mark_as_processed(self, session):
        """Markiert die Rechnung als verarbeitet"""
        self.verarbeitet = 'processed'
        session.commit()
    
    def mark_as_error(self, session, error_message=None):
        """Markiert die Rechnung als fehlerhaft"""
        self.verarbeitet = 'error'
        if error_message:
            # Hier könnte ein error_message Feld hinzugefügt werden
            pass
        session.commit()
    
    def to_dict(self):
        """Konvertiert die Rechnung zu einem Dictionary"""
        return {
            'id': self.id,
            'rechnungsnummer': self.rechnungsnummer,
            'rechnungsdatum': self.rechnungsdatum.isoformat() if self.rechnungsdatum else None,
            'rechnungssteller': self.rechnungssteller,
            'betrag': self.betrag,
            'kategorie': self.kategorie,
            'periode': self.periode,
            'jahr': self.jahr,
            'monat': self.monat,
            'pdf_pfad': self.pdf_pfad,
            'pdf_original_name': self.pdf_original_name,
            'verarbeitet': self.verarbeitet,
            'is_pending': self.is_pending,
            'is_processed': self.is_processed,
            'has_error': self.has_error,
            'erstellt_am': self.erstellt_am.isoformat() if self.erstellt_am else None,
            'aktualisiert_am': self.aktualisiert_am.isoformat() if self.aktualisiert_am else None
        }
    
    def update_from_dict(self, data):
        """Aktualisiert die Rechnung aus einem Dictionary"""
        allowed_fields = [
            'rechnungsnummer', 'rechnungsdatum', 'rechnungssteller', 
            'betrag', 'kategorie', 'periode', 'pdf_pfad', 
            'pdf_original_name', 'verarbeitet'
        ]
        
        for field, value in data.items():
            if field in allowed_fields and hasattr(self, field):
                setattr(self, field, value)
    
    @classmethod
    def create_sample_data(cls, session):
        """
        Erstellt Beispieldaten für Rechnungen
        Für Tests und Entwicklung
        """
        from datetime import date
        
        rechnungen_data = [
            {
                'rechnungsnummer': 'R-2024-001',
                'rechnungsdatum': date(2024, 1, 15),
                'rechnungssteller': 'Elektrizitätswerk Zürich',
                'betrag': 1250.50,
                'kategorie': 'Strom',
                'periode': '2024-01',
                'pdf_pfad': '/data/rechnungen/strom_2024_01.pdf',
                'verarbeitet': 'processed'
            },
            {
                'rechnungsnummer': 'R-2024-002',
                'rechnungsdatum': date(2024, 1, 20),
                'rechnungssteller': 'Heizung AG',
                'betrag': 850.75,
                'kategorie': 'Heizung',
                'periode': '2024-01',
                'pdf_pfad': '/data/rechnungen/heizung_2024_01.pdf',
                'verarbeitet': 'processed'
            },
            {
                'rechnungsnummer': 'R-2024-003',
                'rechnungsdatum': date(2024, 1, 25),
                'rechnungssteller': 'Wasserversorgung',
                'betrag': 320.00,
                'kategorie': 'Wasser',
                'periode': '2024-01',
                'pdf_pfad': '/data/rechnungen/wasser_2024_01.pdf',
                'verarbeitet': 'pending'
            },
            {
                'rechnungsnummer': 'R-2024-004',
                'rechnungsdatum': date(2024, 2, 10),
                'rechnungssteller': 'Hausversicherung',
                'betrag': 450.00,
                'kategorie': 'Versicherung',
                'periode': '2024-02',
                'pdf_pfad': '/data/rechnungen/versicherung_2024_02.pdf',
                'verarbeitet': 'processed'
            },
            {
                'rechnungsnummer': 'R-2024-005',
                'rechnungsdatum': date(2024, 2, 15),
                'rechnungssteller': 'Hauswart Service',
                'betrag': 200.00,
                'kategorie': 'Hauswart',
                'periode': '2024-02',
                'pdf_pfad': '/data/rechnungen/hauswart_2024_02.pdf',
                'verarbeitet': 'pending'
            }
        ]
        
        rechnungen_list = []
        for data in rechnungen_data:
            rechnung = cls(**data)
            session.add(rechnung)
            rechnungen_list.append(rechnung)
        
        session.commit()
        return rechnungen_list
