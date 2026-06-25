from sqlalchemy import Column, Integer, String, Float
from app.infrastructure.database.database import Base

class ProductModel(Base):
    """
    Model SQLAlchemy odzwierdziedlająca tabele w bazie postgresql
    """
    __tablename__ = "products"                  # nazwa tabeli w bazie

    id = Column(Integer, primary_key=True, index=True)

    solid_index = Column(String, unique=True, index=True, nullable=False)   # indeks bryły

    collection = Column(String)                 # nazwa kolekcji
    color = Column(String)                      # kolor kolekcji
    marking_fronts = Column(String)             # oznaczenie frontów czy np 3 drzwi i 2 szuflady
    solid_type = Column(String)                 # rodzaj czy łóżko czy szafa
    front_color = Column(String)                # kolor frontów

    weight = Column(Float)                      # waga
    width_block = Column(Float)                 # szerokość
    height_block = Column(Float)                # wysokość
    depth_block = Column(Float)                 # głębokość

    number_doors = Column(Float)                # liczba drzwi
    number_drawers = Column(Float)              # liczba szuflad

    handle_material = Column(String)            # materiał uchwytów
    drawer_type = Column(String)                # prowadnica szuflad np kulkowe
    hinge_type = Column(String)                 # rodzaj zawiasu
    description_block = Column(String)          # opis bryły
    number_packages = Column(Float)             # liczba paczek

    bed_frame_material = Column(String)         # materiał stelaż łóżka
    shelf_material = Column(String)             # materiał szafki ewentualnie z grubością
    equipment_product = Column(String)          # wyposażenie produktu

