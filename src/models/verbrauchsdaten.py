"""
Verbrauchsdaten-Modell für STWEG
Repräsentiert die Verbrauchsdaten aus dem Excel-File vom ZEV-Server
"""

import re
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Verbrauchsdaten(Base):
    """
    Verbrauchsdaten-Modell
    
    Repräsentiert eine Zeile Verbrauchsdaten aus dem Excel-File.
    Enthält Zeitstempel, Messpunkt, Verbrauch und Kosten.
    """
    
    __tablename__ = 'verbrauchsdaten'
    
    # Primärschlüssel
    id = Column(Integer, primary_key=True, index=True)
    
    # Zeitstempel
    zeitstempel = Column(DateTime, nullable=False, index=True)
    
    # Verknüpfung zu Messpunkt
    messpunkt_id = Column(Integer, ForeignKey('messpunkte.id'), nullable=False, index=True)
    
    # Verbrauchsdaten
    verbrauch = Column(Float, nullable=False)  # Verbrauch in kWh
    kosten = Column(Float, nullable=True)  # Kosten in CHF (optional)
    
    # Periode (YYYY-MM Format)
    periode = Column(String(7), nullable=False, index=True)  # z.B. "2024-01"
    
    # Zeitstempel für Audit
    erstellt_am = Column(DateTime(timezone=True), server_default=func.now())
    
    # Beziehungen
    messpunkt = relationship("Messpunkt", back_populates="verbrauchsdaten")
    
    # Indizes für bessere Performance
    __table_args__ = (
        Index('idx_zeitstempel_messpunkt', 'zeitstempel', 'messpunkt_id'),
        Index('idx_periode_messpunkt', 'periode', 'messpunkt_id'),
    )
    
    def __init__(self, **kwargs):
        """Initialisierung mit Validierung"""
        # Periode validieren
        if 'periode' in kwargs:
            periode = kwargs['periode']
            if not self._validate_periode_format(periode):
                raise ValueError(f"Periode muss im Format YYYY-MM sein, erhalten: {periode}")
        
        # Zeitstempel validieren
        if 'zeitstempel' in kwargs:
            zeitstempel = kwargs['zeitstempel']
            if not isinstance(zeitstempel, datetime):
                raise ValueError(f"Zeitstempel muss ein datetime-Objekt sein, erhalten: {type(zeitstempel)}")
        
        # Verbrauch validieren
        if 'verbrauch' in kwargs:
            verbrauch = kwargs['verbrauch']
            if verbrauch < 0:
                raise ValueError(f"Verbrauch darf nicht negativ sein, erhalten: {verbrauch}")
        
        # Kosten validieren
        if 'kosten' in kwargs and kwargs['kosten'] is not None:
            kosten = kwargs['kosten']
            if kosten < 0:
                raise ValueError(f"Kosten dürfen nicht negativ sein, erhalten: {kosten}")
        
        super().__init__(**kwargs)
    
    def __repr__(self):
        """String-Repräsentation für Debugging"""
        return f"<Verbrauchsdaten(id={self.id}, zeitstempel={self.zeitstempel}, messpunkt_id={self.messpunkt_id}, verbrauch={self.verbrauch})>"
    
    def __str__(self):
        """Benutzerfreundliche String-Darstellung"""
        messpunkt_name = self.messpunkt.name if self.messpunkt else f"ID:{self.messpunkt_id}"
        return f"Verbrauchsdaten({messpunkt_name} - {self.zeitstempel.strftime('%Y-%m-%d %H:%M')} - {self.verbrauch} kWh)"
    
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
    def kosten_pro_kwh(self):
        """Berechnet die Kosten pro kWh"""
        if self.kosten is None or self.verbrauch == 0:
            return None
        return round(self.kosten / self.verbrauch, 4)
    
    @property
    def jahr(self):
        """Gibt das Jahr aus der Periode zurück"""
        return int(self.periode.split('-')[0])
    
    @property
    def monat(self):
        """Gibt den Monat aus der Periode zurück"""
        return int(self.periode.split('-')[1])
    
    @classmethod
    def get_by_periode(cls, session, periode):
        """Gibt alle Verbrauchsdaten für eine Periode zurück"""
        return session.query(cls).filter(cls.periode == periode).all()
    
    @classmethod
    def get_by_messpunkt(cls, session, messpunkt_id):
        """Gibt alle Verbrauchsdaten für einen Messpunkt zurück"""
        return session.query(cls).filter(cls.messpunkt_id == messpunkt_id).all()
    
    @classmethod
    def get_by_messpunkt_and_periode(cls, session, messpunkt_id, periode):
        """Gibt Verbrauchsdaten für einen Messpunkt und eine Periode zurück"""
        return session.query(cls).filter(
            cls.messpunkt_id == messpunkt_id,
            cls.periode == periode
        ).all()
    
    @classmethod
    def get_zeitraum(cls, session, start_datum, end_datum):
        """Gibt alle Verbrauchsdaten in einem Zeitraum zurück"""
        return session.query(cls).filter(
            cls.zeitstempel >= start_datum,
            cls.zeitstempel <= end_datum
        ).all()
    
    @classmethod
    def get_total_verbrauch_periode(cls, session, periode):
        """Berechnet den Gesamtverbrauch für eine Periode"""
        result = session.query(func.sum(cls.verbrauch)).filter(cls.periode == periode).scalar()
        return result or 0.0
    
    @classmethod
    def get_total_kosten_periode(cls, session, periode):
        """Berechnet die Gesamtkosten für eine Periode"""
        result = session.query(func.sum(cls.kosten)).filter(
            cls.periode == periode,
            cls.kosten.isnot(None)
        ).scalar()
        return result or 0.0
    
    @classmethod
    def get_verbrauch_by_messpunkt_periode(cls, session, periode):
        """Gibt Verbrauchsdaten gruppiert nach Messpunkt für eine Periode zurück"""
        from sqlalchemy import func
        return session.query(
            cls.messpunkt_id,
            func.sum(cls.verbrauch).label('total_verbrauch'),
            func.sum(cls.kosten).label('total_kosten')
        ).filter(
            cls.periode == periode
        ).group_by(cls.messpunkt_id).all()
    
    def to_dict(self):
        """Konvertiert die Verbrauchsdaten zu einem Dictionary"""
        return {
            'id': self.id,
            'zeitstempel': self.zeitstempel.isoformat() if self.zeitstempel else None,
            'messpunkt_id': self.messpunkt_id,
            'messpunkt_name': self.messpunkt.name if self.messpunkt else None,
            'verbrauch': self.verbrauch,
            'kosten': self.kosten,
            'kosten_pro_kwh': self.kosten_pro_kwh,
            'periode': self.periode,
            'jahr': self.jahr,
            'monat': self.monat,
            'erstellt_am': self.erstellt_am.isoformat() if self.erstellt_am else None
        }
    
    def update_from_dict(self, data):
        """Aktualisiert die Verbrauchsdaten aus einem Dictionary"""
        allowed_fields = ['zeitstempel', 'messpunkt_id', 'verbrauch', 'kosten', 'periode']
        
        for field, value in data.items():
            if field in allowed_fields and hasattr(self, field):
                setattr(self, field, value)
    
    @classmethod
    def create_sample_data(cls, session, anzahl_tage=7):
        """
        Erstellt Beispieldaten für Verbrauchsdaten
        Für Tests und Entwicklung
        """
        from .messpunkt import Messpunkt
        from datetime import timedelta
        
        # Messpunkte laden
        messpunkte = session.query(Messpunkt).all()
        
        if not messpunkte:
            # Beispieldaten für Messpunkte erstellen, falls keine vorhanden
            messpunkte = Messpunkt.create_sample_data(session)
        
        verbrauchsdaten_list = []
        start_datum = datetime(2024, 1, 1, 0, 0, 0)
        
        for tag in range(anzahl_tage):
            aktuelles_datum = start_datum + timedelta(days=tag)
            periode = aktuelles_datum.strftime('%Y-%m')
            
            for messpunkt in messpunkte:
                # Zufällige Verbrauchsdaten generieren
                import random
                base_verbrauch = 20 + random.uniform(-5, 10)
                kosten = base_verbrauch * 0.25  # 0.25 CHF pro kWh
                
                verbrauch = cls(
                    zeitstempel=aktuelles_datum,
                    messpunkt_id=messpunkt.id,
                    verbrauch=round(base_verbrauch, 2),
                    kosten=round(kosten, 2),
                    periode=periode
                )
                
                session.add(verbrauch)
                verbrauchsdaten_list.append(verbrauch)
        
        session.commit()
        return verbrauchsdaten_list

