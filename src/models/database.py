"""
Datenbank-Konfiguration für STWEG
SQLAlchemy Setup und Session-Management
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Base-Klasse für alle Modelle
Base = declarative_base()

# Datenbank-URL (SQLite für lokale Entwicklung)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///stweg.db')

# Engine erstellen
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Setze auf True für SQL-Logging
    poolclass=StaticPool,  # Für SQLite
    connect_args={'check_same_thread': False}  # Für SQLite
)

# Session-Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """
    Dependency für Datenbank-Session
    Für Verwendung in FastAPI oder anderen Frameworks
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_tables():
    """Erstellt alle Tabellen in der Datenbank"""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Löscht alle Tabellen in der Datenbank (Vorsicht!)"""
    Base.metadata.drop_all(bind=engine)


def get_db_session():
    """Erstellt eine neue Datenbank-Session"""
    return SessionLocal()


# Datenbank-Initialisierung
if __name__ == "__main__":
    create_tables()
    print("Datenbank-Tabellen erstellt!")

