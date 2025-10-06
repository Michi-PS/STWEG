"""
Zentrale Modelle-Datei für STWEG
Importiert alle Modelle und löst zirkuläre Import-Probleme
"""

# Alle Modelle importieren
from .database import Base
from .eigentuemer import Eigentuemer
from .messpunkt import Messpunkt
from .verbrauchsdaten import Verbrauchsdaten
from .rechnung import Rechnung

# Alle Modelle für einfachen Import
__all__ = [
    'Base',
    'Eigentuemer', 
    'Messpunkt',
    'Verbrauchsdaten',
    'Rechnung'
]

