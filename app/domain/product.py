from typing import Any, List, Optional
from pydantic import BaseModel, Field

class ProductParameter(BaseModel):      # BaseModel jego funkcje: nie trzeba pisać konstruktora, walidacja danych według tego co jest zadeklarowane,
                                        # oraz wykonuje Serializacje na JSONa (model_dump_json())
                                        # oraz Deserializacje czyli odbieranie obiektu JSON i przerabianie go na nasz inteligetny obiekt (model_validate_json())
                                        # odpowiednikiem w javie jest mapper który mapuje obiekt na różne formaty

    """
    To jest reprezentacja jednego parametru (np. grubość blatu, materiał frontu).
    Zawiera nie tylko samą wartość, ale też dowód na to, skąd ta wartość pochodzi surowa wartość oraz jak wygląda po normalizacji.
    """
    field_code: str                 # Nazwa naszego znormalizowanego paramateru np grubosc blatu
    raw_name: str                   # Dokładna nazwa kolumny u dostawcy, np. "Grubość blatu [mm]"
    raw_value: Any                  # Surowa wartość prosto z komórki od dostawcy, np. "16 mm"
    value: Any = None               # Wartość po naszej normalizacji, np. 16
    status: str = "extracted"       # status pola np extracted_from_suppiler

    # Metadane źródła pliku od dostawcy     Przykładowy Plik: "dostawca.xlsx" | Arkusz: "MOND J CZ" | Kolumna: "Cena" | Wiersz: 10
    source_file: Optional[str] = None       # Nazwa pliku ciąg znaków dlatego string np "MEBLEOSIEK_cennik_2026.xlsx"
    source_sheet: Optional[str] = None      # Nazwa konkretnego arkusza np MOND J CZ czyli kolekcja Mond-Jadalnia-Czarna
    source_column: Optional[str] = None     # Konkretna kolumna A,B,C
    source_row: Optional[int] = None        # wierz liczba całkowita 1,2,3,4

class Product(BaseModel):
    """
    GŁówny produkt w tym wypadku mebel
    """
    supplier_id: str                        # np "MEBLOSIEK" nazwa producenta
    supplier_index: str                     # unikalny kod producenta danego produktu
    collection_name: Optional[str] = None   # Nazwa kolekcji do której należy produkt

    parameters: List[ProductParameter] = Field(default_factory=list)    # Lista wszystkich parametrów  (default_factory odpowiada za stworzenie zupełnie nowej listy dla kazdego podanego produktu
                                                                        # bo w innym wypadku ta lista była by wspólna dla wszyskich produktów
    status: str = "new"                     # np "gotowy" albo "brakuje danych"