import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL","postgresql://admin:adminhaslo@db:5432/product_data")  # bierzemy adres z docker compose a jesli cos nie wyjdzie to uzywamy tego drugiego który mamy wpisany

engine = create_engine(DATABASE_URL, echo=False)    # silnik który rozmawai z postgresql   echo dajemy na False poniewaz inaczej każde zapytanie SQL było by wypisuwane w konsoli

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)     # autocommit każe zapiysawć dane w bazie dopiero na polecenie programisty nie sama z siebie   bind=engine podłączamy sie do głównego silnika bazy

Base = declarative_base()   # klasa matka wszystkie tabele dziedzicza po niej       Base pusta inteligenta klasa w pythonie każda klasa go będzie miała i pozwala to SQLAlchemy nią zarządzać i że nie jest to zwykły obiekt w pythonie

def get_db():
    """
    Generator sesji bazy danych. Otwiera drzwi do magazynu,
    pozwala wstawić dane i ZAWSZE bezpiecznie zamyka drzwi na koniec.
    :return:
    """
    db = SessionLocal()     # tworzy połaczenie z bazą gdy chcemy np wysłąć dane
    try:
        yield db            # yield daje połączenie i zatrzymuje w czasie nie zamyka połaczenia (zamarza) i dopiero po wykonaniu zapytnaia przechodzi dalej i zamyka baze oraz połaczenie
    finally:
        db.close()          # odmraża funkcje i zamyka baze
