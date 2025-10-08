"""
Eigentümer-Datenmodell für STWEG
Repräsentiert die 7 Eigentümer der Stockwerkeigentümergesellschaft
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Eigentuemer(Base):
    """
    Eigentümer-Datenmodell
    
    Repräsentiert einen Eigentümer der Stockwerkeigentümergesellschaft.
    Jeder Eigentümer hat eine Wohnung und einen Anteil an den Gesamtkosten.
    """
    
    __tablename__ = 'eigentuemer'
    
    # Primärschlüssel
    id = Column(Integer, primary_key=True, index=True)
    
    # Grunddaten
    name = Column(String(100), nullable=False, index=True)
    wohnung = Column(String(10), nullable=False, unique=True, index=True)  # z.B. "1A", "2B"
    anteil = Column(Float, nullable=False)  # Anteil an Gesamtkosten (0.0 - 1.0)
    
    # Kontaktdaten
    email = Column(String(150), nullable=True)
    telefon = Column(String(20), nullable=True)
    
    # Status
    aktiv = Column(Boolean, default=True, nullable=False)
    
    # Zeitstempel
    erstellt_am = Column(DateTime(timezone=True), server_default=func.now())
    aktualisiert_am = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Beziehungen
    messpunkte = relationship("Messpunkt", back_populates="eigentuemer")
    # zaehler = relationship("Zaehler", back_populates="eigentuemer")  # Temporär auskommentiert
    
    @property
    def verbrauchsdaten(self):
        """Gibt alle Verbrauchsdaten des Eigentümers zurück"""
        verbrauchsdaten = []
        for messpunkt in self.messpunkte:
            verbrauchsdaten.extend(messpunkt.verbrauchsdaten)
        return verbrauchsdaten
    
    def __init__(self, **kwargs):
        """Initialisierung mit Validierung"""
        # Anteil validieren
        if 'anteil' in kwargs:
            anteil = kwargs['anteil']
            if not (0.0 <= anteil <= 1.0):
                raise ValueError(f"Anteil muss zwischen 0.0 und 1.0 liegen, erhalten: {anteil}")
        
        super().__init__(**kwargs)
    
    def __repr__(self):
        """String-Repräsentation für Debugging"""
        return f"<Eigentuemer(id={self.id}, wohnung='{self.wohnung}', name='{self.name}')>"
    
    def __str__(self):
        """Benutzerfreundliche String-Darstellung"""
        return f"Eigentuemer({self.wohnung} - {self.name})"
    
    @property
    def anteil_prozent(self):
        """Anteil als Prozent (z.B. 14.0 für 14%)"""
        return round(self.anteil * 100, 2)
    
    @classmethod
    def get_all_active(cls, session):
        """Gibt alle aktiven Eigentümer zurück"""
        return session.query(cls).filter(cls.aktiv == True).all()
    
    @classmethod
    def get_by_wohnung(cls, session, wohnung):
        """Findet Eigentümer anhand der Wohnung"""
        return session.query(cls).filter(cls.wohnung == wohnung).first()
    
    @classmethod
    def get_total_anteil(cls, session):
        """Berechnet die Summe aller Anteile"""
        result = session.query(func.sum(cls.anteil)).filter(cls.aktiv == True).scalar()
        return result or 0.0
    
    def validate_anteil_sum(self, session):
        """
        Validiert, dass die Summe aller Anteile nicht größer als 1.0 ist
        (wird beim Speichern aufgerufen)
        """
        if not self.aktiv:
            return True
        
        # Summe aller aktiven Anteile außer diesem
        other_anteil = session.query(func.sum(Eigentuemer.anteil)).filter(
            Eigentuemer.aktiv == True,
            Eigentuemer.id != self.id
        ).scalar() or 0.0
        
        total_anteil = other_anteil + self.anteil
        
        if total_anteil > 1.0:
            raise ValueError(
                f"Summe aller Anteile ({total_anteil:.3f}) darf nicht größer als 1.0 sein. "
                f"Dieser Eigentümer hat Anteil {self.anteil:.3f}, andere haben zusammen {other_anteil:.3f}"
            )
        
        return True
    
    def to_dict(self):
        """Konvertiert den Eigentümer zu einem Dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'wohnung': self.wohnung,
            'anteil': self.anteil,
            'anteil_prozent': self.anteil_prozent,
            'email': self.email,
            'telefon': self.telefon,
            'aktiv': self.aktiv,
            'erstellt_am': self.erstellt_am.isoformat() if self.erstellt_am else None,
            'aktualisiert_am': self.aktualisiert_am.isoformat() if self.aktualisiert_am else None
        }
    
    def update_from_dict(self, data):
        """Aktualisiert den Eigentümer aus einem Dictionary"""
        allowed_fields = ['name', 'wohnung', 'anteil', 'email', 'telefon', 'aktiv']
        
        for field, value in data.items():
            if field in allowed_fields and hasattr(self, field):
                setattr(self, field, value)
    
    @classmethod
    def create_sample_data(cls, session):
        """
        Erstellt Beispieldaten für 7 Eigentümer
        Für Tests und Entwicklung
        """
        sample_eigentuemer = [
            {'name': 'Max Mustermann', 'wohnung': '1A', 'anteil': 0.14, 'email': 'max@example.com'},
            {'name': 'Anna Schmidt', 'wohnung': '1B', 'anteil': 0.14, 'email': 'anna@example.com'},
            {'name': 'Peter Weber', 'wohnung': '2A', 'anteil': 0.14, 'email': 'peter@example.com'},
            {'name': 'Lisa Fischer', 'wohnung': '2B', 'anteil': 0.14, 'email': 'lisa@example.com'},
            {'name': 'Tom Wagner', 'wohnung': '3A', 'anteil': 0.14, 'email': 'tom@example.com'},
            {'name': 'Maria Becker', 'wohnung': '3B', 'anteil': 0.15, 'email': 'maria@example.com'},
            {'name': 'Hans Schulz', 'wohnung': '4A', 'anteil': 0.15, 'email': 'hans@example.com'},
        ]
        
        eigentuemer_list = []
        for data in sample_eigentuemer:
            eigentuemer = cls(**data)
            session.add(eigentuemer)
            eigentuemer_list.append(eigentuemer)
        
        session.commit()
        return eigentuemer_list


# Import für Beziehungen (wird nach der Definition der anderen Modelle importiert)
# from .messpunkt import Messpunkt  # Wird zur Laufzeit importiert
