import datetime

from sqlalchemy import Column, Integer, String, Float,  Enum as SqlEnum
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.sql import func
from app.infrastructure.database.database import Base
from app.domain.enums.product_preview_status import ProductPreviewStatus

class ProductPreviewModel(Base):
    """
    Tabela tymczasowa produktów po imporcie z pliku.
    Dane trafiają tutaj najpierw, są pokazywane na froncie,
    a dopiero po zatwierdzeniu mogą trafić do tabeli docelowej dostawcy.
    """
    __tablename__ = "import_preview_products"   # nazwa tabeli w bazie

    id = Column(Integer, primary_key=True, index=True)

    import_id = Column(String, nullable=False, index=True)
    supplier_id = Column(String, nullable=False, index=True)
    product_key = Column(String, unique=False, index=True, nullable=False)  # dostawca-kolekcja-indeks-rodzaj bryły-oznaczenie frontów-kolor

    solid_index = Column(String, unique=False, index=True, nullable=False)  # indeks bryły
    #product_type = Column(SqlEnum(ProductType, name="product_type_enum", native_enum="False", nullable="False", index="True"))  # Twarde(szafa) czy miekkie(wersalka)

    collection = Column(String, index=True)     # nazwa kolekcji
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

    status = Column(
            SqlEnum(
                ProductPreviewStatus,
                name="product_preview_status",
                values_callable=lambda enum_class: [item.value for item in enum_class],
                native_enum=False,
            ),
            nullable=False,
            index=True,
            default=ProductPreviewStatus.PREVIEW.value
    )

    created_at = Column(
        TIMESTAMP(timezone=True, precision=0),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        TIMESTAMP(timezone=True, precision=0),
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc).replace(microsecond=0),
        nullable=False
    )

