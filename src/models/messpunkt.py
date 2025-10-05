"""
Messpunkt-Datenmodell für STWEG
Repräsentiert die Messpunkte aus dem Excel-File vom ZEV-Server
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Messpunkt(Base):
    """
    Messpunkt-Datenmodell
    
    Repräsentiert einen Messpunkt aus dem Excel-File.
    Kann individual (Eigentümer-spezifisch) oder gemeinschaft (für alle) sein.
    """
    
    __tablename__ = 'messpunkte'
    
    # Primärschlüssel
    id = Column(Integer, primary_key=True, index=True)
    
    # Grunddaten
    name = Column(String(50), nullable=False, index=True)  # z.B. "Eigentümer_1", "Gemeinschaft"
    typ = Column(String(20), nullable=False, index=True)  # "individual" oder "gemeinschaft"
    
    # Verknüpfung zu Eigentümer (nur bei individual-Messpunkten)
    eigentuemer_id = Column(Integer, ForeignKey('eigentuemer.id'), nullable=True, index=True)
    
    # Status
    aktiv = Column(Boolean, default=True, nullable=False)
    
    # Zeitstempel
    erstellt_am = Column(DateTime(timezone=True), server_default=func.now())
    aktualisiert_am = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Beziehungen
    eigentuemer = relationship("Eigentuemer", back_populates="messpunkte")
    verbrauchsdaten = relationship("Verbrauchsdaten", back_populates="messpunkt")
    
    def __init__(self, **kwargs):
        """Initialisierung mit Validierung"""
        # Typ validieren
        if 'typ' in kwargs:
            typ = kwargs['typ']
            if typ not in ['individual', 'gemeinschaft']:
                raise ValueError(f"Typ muss 'individual' oder 'gemeinschaft' sein, erhalten: {typ}")
            
            # Bei gemeinschaft-Messpunkten darf eigentuemer_id nicht gesetzt sein
            if typ == 'gemeinschaft' and kwargs.get('eigentuemer_id') is not None:
                raise ValueError("Gemeinschafts-Messpunkte dürfen keinen eigentuemer_id haben")
            
            # Bei individual-Messpunkten muss eigentuemer_id gesetzt sein
            if typ == 'individual' and kwargs.get('eigentuemer_id') is None:
                raise ValueError("Individual-Messpunkte müssen einen eigentuemer_id haben")
        
        super().__init__(**kwargs)
    
    def __repr__(self):
        """String-Repräsentation für Debugging"""
        eigentuemer_info = f", eigentuemer_id={self.eigentuemer_id}" if self.eigentuemer_id else ""
        return f"<Messpunkt(id={self.id}, name='{self.name}', typ='{self.typ}'{eigentuemer_info})>"
    
    def __str__(self):
        """Benutzerfreundliche String-Darstellung"""
        if self.eigentuemer:
            return f"Messpunkt({self.name} - {self.eigentuemer.wohnung})"
        else:
            return f"Messpunkt({self.name} - {self.typ})"
    
    @property
    def is_individual(self):
        """Prüft, ob es sich um einen Individual-Messpunkt handelt"""
        return self.typ == 'individual'
    
    @property
    def is_gemeinschaft(self):
        """Prüft, ob es sich um einen Gemeinschafts-Messpunkt handelt"""
        return self.typ == 'gemeinschaft'
    
    @classmethod
    def get_by_type(cls, session, typ):
        """Gibt alle Messpunkte eines bestimmten Typs zurück"""
        return session.query(cls).filter(cls.typ == typ, cls.aktiv == True).all()
    
    @classmethod
    def get_individual_messpunkte(cls, session):
        """Gibt alle Individual-Messpunkte zurück"""
        return cls.get_by_type(session, 'individual')
    
    @classmethod
    def get_gemeinschaft_messpunkte(cls, session):
        """Gibt alle Gemeinschafts-Messpunkte zurück"""
        return cls.get_by_type(session, 'gemeinschaft')
    
    @classmethod
    def get_by_name(cls, session, name):
        """Findet Messpunkt anhand des Namens"""
        return session.query(cls).filter(cls.name == name).first()
    
    @classmethod
    def get_by_eigentuemer(cls, session, eigentuemer_id):
        """Gibt alle Messpunkte eines Eigentümers zurück"""
        return session.query(cls).filter(
            cls.eigentuemer_id == eigentuemer_id,
            cls.aktiv == True
        ).all()
    
    def to_dict(self):
        """Konvertiert den Messpunkt zu einem Dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'typ': self.typ,
            'eigentuemer_id': self.eigentuemer_id,
            'eigentuemer_name': self.eigentuemer.name if self.eigentuemer else None,
            'eigentuemer_wohnung': self.eigentuemer.wohnung if self.eigentuemer else None,
            'aktiv': self.aktiv,
            'erstellt_am': self.erstellt_am.isoformat() if self.erstellt_am else None,
            'aktualisiert_am': self.aktualisiert_am.isoformat() if self.aktualisiert_am else None
        }
    
    def update_from_dict(self, data):
        """Aktualisiert den Messpunkt aus einem Dictionary"""
        allowed_fields = ['name', 'typ', 'eigentuemer_id', 'aktiv']
        
        for field, value in data.items():
            if field in allowed_fields and hasattr(self, field):
                setattr(self, field, value)
    
    @classmethod
    def create_sample_data(cls, session):
        """
        Erstellt Beispieldaten für Messpunkte
        Für Tests und Entwicklung
        """
        # Zuerst Eigentümer laden
        from .eigentuemer import Eigentuemer
        eigentuemer = session.query(Eigentuemer).all()
        
        if not eigentuemer:
            # Beispieldaten für Eigentümer erstellen, falls keine vorhanden
            eigentuemer = Eigentuemer.create_sample_data(session)
        
        messpunkte_data = []
        
        # Individual-Messpunkte für jeden Eigentümer
        for i, eig in enumerate(eigentuemer, 1):
            messpunkte_data.append({
                'name': f'Eigentümer_{i}',
                'typ': 'individual',
                'eigentuemer_id': eig.id
            })
        
        # Gemeinschafts-Messpunkt
        messpunkte_data.append({
            'name': 'Gemeinschaft',
            'typ': 'gemeinschaft',
            'eigentuemer_id': None
        })
        
        # Gesamtverbrauch-Messpunkt
        messpunkte_data.append({
            'name': 'Gesamtverbrauch',
            'typ': 'gemeinschaft',
            'eigentuemer_id': None
        })
        
        messpunkte_list = []
        for data in messpunkte_data:
            messpunkt = cls(**data)
            session.add(messpunkt)
            messpunkte_list.append(messpunkt)
        
        session.commit()
        return messpunkte_list


# Import für Beziehungen (wird nach der Definition der anderen Modelle importiert)
# from .verbrauchsdaten import Verbrauchsdaten  # Wird zur Laufzeit importiert
