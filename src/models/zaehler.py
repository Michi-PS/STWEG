"""
Zähler-Modell für STWEG

Repräsentiert Zähler aus dem ZEV-File, die später Eigentümern zugeordnet werden können.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Zaehler(Base):
    """Zähler-Modell für Messpunkte"""
    
    __tablename__ = 'zaehler'
    __table_args__ = {'extend_existing': True}
    
    # Primärschlüssel
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Zähler-Identifikation
    zaehler_nr = Column(String(50), nullable=False, unique=True, comment="Zähler-Nummer (z.B. 24P1)")
    bezeichnung = Column(String(100), nullable=False, comment="Zähler-Bezeichnung (z.B. Wohnung 0.1)")
    
    # Zähler-Typ
    typ = Column(String(20), nullable=False, comment="Zähler-Typ (warmwasser, heizung, strom, gas)")
    
    # Status
    aktiv = Column(Boolean, default=True, nullable=False, comment="Zähler aktiv")
    
    # Zuordnung
    eigentuemer_id = Column(Integer, ForeignKey('eigentuemer.id'), nullable=True, comment="Zugeordneter Eigentümer")
    
    # Zusätzliche Informationen
    beschreibung = Column(Text, nullable=True, comment="Zusätzliche Beschreibung")
    einheit = Column(String(10), nullable=True, comment="Mess-Einheit (kWh, m³, etc.)")
    
    # Zeitstempel
    erstellt_am = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    aktualisiert_am = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Beziehungen
    eigentuemer = relationship("Eigentuemer", back_populates="zaehler")
    
    def __repr__(self):
        return f"<Zaehler(id={self.id}, nr='{self.zaehler_nr}', bezeichnung='{self.bezeichnung}', typ='{self.typ}')>"
    
    def __str__(self):
        return f"{self.zaehler_nr} - {self.bezeichnung} ({self.typ})"
    
    @property
    def ist_zugeordnet(self):
        """Prüft ob der Zähler einem Eigentümer zugeordnet ist"""
        return self.eigentuemer_id is not None
    
    @property
    def eigentuemer_name(self):
        """Name des zugeordneten Eigentümers"""
        return self.eigentuemer.name if self.eigentuemer else "Nicht zugeordnet"
    
    @property
    def status_text(self):
        """Status als Text"""
        if not self.aktiv:
            return "Inaktiv"
        elif self.ist_zugeordnet:
            return f"Zugeordnet ({self.eigentuemer_name})"
        else:
            return "Verfügbar"
    
    def to_dict(self):
        """Konvertiert Zähler zu Dictionary"""
        return {
            'id': self.id,
            'zaehler_nr': self.zaehler_nr,
            'bezeichnung': self.bezeichnung,
            'typ': self.typ,
            'aktiv': self.aktiv,
            'eigentuemer_id': self.eigentuemer_id,
            'beschreibung': self.beschreibung,
            'einheit': self.einheit,
            'erstellt_am': self.erstellt_am.isoformat() if self.erstellt_am else None,
            'aktualisiert_am': self.aktualisiert_am.isoformat() if self.aktualisiert_am else None,
            'ist_zugeordnet': self.ist_zugeordnet,
            'eigentuemer_name': self.eigentuemer_name,
            'status_text': self.status_text
        }
