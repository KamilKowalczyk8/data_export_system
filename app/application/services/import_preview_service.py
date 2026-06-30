import os
import re
import uuid
from typing import Dict, Any

from app.infrastructure.importers.file_importer import FileImporter
from app.application.parsers.excel_parser import ExcelParser
from app.infrastructure.repositories.product_preview_repository import ProductPreviewRepository
from app.application.config.field_types import FLOAT_FIELDS

class ImportPreviewService:
    """
    Warstwa logiki bizensowej odpowiedzialna za całe przeprowadzenie procesu
    """

    def __init__(self, available_profiles: dict, db):                   # konstruktor klasy dostaje db oraz profile
        self.available_profiles = available_profiles                    # profile dostawców dostarczane z zewnątrz
        self.db = db
        self.product_preview_repository = ProductPreviewRepository(db)
        self._readers = {                                               # podkreślnik oznacza prywatną metode i można jej używać tylko tutaj
            "excel": self._read_excel,
            "csv": self._read_csv
        }

    async def process_preview_import(self, supplier: str, file_name: str, file_content: bytes) -> Dict[str, Any]:
        """
        Asynchroniczna pozwala na to że metoda nam się nie zawiesi
        Metoda realizująca import pliku wraz z jego danymi
        :param supplier:
        :param file_name:
        :param file_content:
        :return:
        """
        if supplier not in self.available_profiles:
            raise ValueError(f"Nieznany dostawca: {supplier}")

        active_profile = self.available_profiles[supplier]
        file_type = active_profile.get("file_type")         # z profilu danego dostawcy wyciągamy typ danego pliku

        read_method = self._readers.get(file_type)          # następnie wyciągamy nasze narzędzie readers przypisane do formatu
        if not read_method:
            raise ValueError(f"Brak metod do odczytu tego foramtu pliku: {file_type}")

        temp_file_path = f"temp_{file_name}"

        try:
            with open(temp_file_path, "wb") as buffer:      # zapisujemy plik tymczasowo na dysku "wb" oznacza Write Binary
                buffer.write(file_content)                  # with gwarantuje że plik na dysku zostanie zamknięty przez system po zakończeniu bloku kodu.

            importer = FileImporter(temp_file_path)
            sheets_data = read_method(importer, active_profile)
            processed_data = self._map_data(sheets_data, active_profile)

            import_id = str(uuid.uuid4())                   # nadajemy numer z uuid dla import_id
            supplier_id = active_profile["supplier_id"]     # nazwa dostawcy z konstruktora

            for product_data in processed_data:
                product_data["import_id"] = import_id
                product_data["supplier_id"] = supplier_id
                product_data["product_key"] = self._build_product_key(product_data)

            save_result = self.product_preview_repository.save_products(processed_data) # zapisuejmy do zmiennej nasz wynik

            collections = sorted({
                product.get("collection")
                for product in processed_data
                if product.get("collection")
            })

            return {                        # wypisujemy dane naszego importu
                "status": "success",
                "message": f"Wczytano dane do podglądu dla profilu {supplier}",
                "import_id": import_id,
                "supplier_id": supplier_id,
                "saved_count": save_result["saved_count"],
                "skipped_count": save_result["skipped_count"],
                "preview": [
                    f"Znalazłem kolekcje: {', '.join(collections) if collections else 'Nieznana kolekcja'}"
                ]
            }

        finally:
            if os.path.exists(temp_file_path):              # usuwamy tymczasowy plik aby zwolnic miejsce na dysku
                os.remove(temp_file_path)


    def get_preview_products(self, import_id: str):         # metoda do wyświetlanai danych przed zaakceptowaniem
        return self.product_preview_repository.get_product_by_import_id(import_id)

    def get_current_preview_products(self):                 # metoda która wyświetla dane które są aktuakne w bazie zeby uzytkownik nie musiał za kazdym razem importować
        return self.product_preview_repository.get_current_preview_products()

    # Prywatne metody używane zaczynają się od _nazwa metody

    def _build_product_key(self, product_data: dict) -> str:    # funkcja budująća nasz product_key
        parts = [                                               # częsci z jakich będzie sie składał
            product_data.get("supplier_id"),
            product_data.get("collection"),
            product_data.get("solid_index"),
            product_data.get("solid_type"),
            product_data.get("marking_fronts"),
            product_data.get("color"),
        ]
        clean_parts = []

        for part in parts:
            if part is None:
                part = "brak"

            part = str(part).strip().upper()            # bierzemy stringi z danymi i zmieniamy na DUŻA LITERE

            if part == "":
                part = "brak"

            part = part.replace(" ", "_")
            part = part.replace(",", "_")
            part = part.replace("\\", "_")

            clean_parts.append(part)                    # dodajemy na koniec czystej listy kazdy przetworzony element

        return " - ".join(clean_parts)

    def _read_excel(self, importer: FileImporter, profil: dict) -> dict:
        """ Metoda dla odczytu plików Excel """
        return importer.load_all_sheets()

    def _read_csv(self, importer: FileImporter, profil: dict) -> dict:
        """ Metoda dla odczytu csv """
        return importer.load_csv(
            delimiter=profil.get("delimiter", ";"),         # jesli nie otrzyma dancyh z profilu to domślnie ustawaia  te dane ; i utf-8
            encoding=profil.get("encoding", "utf-8")
        )

    def _clean_value(self, value):          # ta metoda czyści nie zapisuje wartosci jesli któres z tych warunków sie zdarzy np będzie puste pole
        """
        Czyści pojedynczą wartośc String z pliku puste wartosci zamienai na None
        """

        if value is None:
            return None

        value = str(value).strip()

        if value == "":
            return None

        if value.lower() in ["nan", "none", "null"]:
            return None

        return value

    def _clean_float_value(self, value):    # odpowiednik tej funkcji wyżej ale dla floatów
        """
        Czyści wartości liczbowe
        obsługuje:
            - "44.0 kg"
            - "79,5 kg"
            - "209 cm -> 209 -> 209.0"
            - "3"
            - "1,0"
        Jeśli nie da się odczytać liczby, zwraca None.
        """

        if value is None:
            return None

        value = str(value).strip()                      # zamienia wartosc na tekst i usuwa spacje z przodu i z tyłu

        if value == "":
            return None

        if value.lower() in ["nan", "none", "null"]:    # jesli plik lub pandas zwróci któryś z tych wartosci to traktujemy to jako brak wartosci
            return None

        value = value.lower()                             # zamieniamy tekst na małe litery
        value = value.replace(",", ".")          # zamieniamy , na . gdyż python potrzebuje kroppki do zrobienia wartosci float

        match = re.search(r"\d+(\.\d+)?", value)   #słuzy do znajdowanai cyfry w teksice \d+ to zajduje np 10 a \.(\d+ znajduje 0.5 co daje nam całośc 10.5

        if not match:                                     # jesli nie znaleziono liczby wyrzyca None
            return None

        return float(match.group())                       # zwracasz znalezioną liczbe float

    def _clean_field_value(self, field_name, value):
        """
        czysci pola zaleznie od pola modeli string lub flaot
        pola z FLOAT_FIELDS czsyci jako float
        a pozostałe jako string
        """
        if field_name in FLOAT_FIELDS:
            return self._clean_float_value(value)

        return self._clean_value(value)


    def _map_data(self, sheets_data: dict, active_profile: dict) -> list:   # _ prywatna metoda
        """ Prywatna metoda pomocznicza do mapowania danych """
        results = []
        if not sheets_data:                                                 # sprawdzenie czy otrzymaliśmy dane
            return results                                                  # jesli nie zwraca pustą liste

        mapping = active_profile.get("mapping")                             # pobiera z profilu słownik mapowania

        for sheet_name, df in sheets_data.items():                          # przechodzi przez arkusze każde w excelu
            if active_profile.get("skip_guillotine", False):    # sprawdza flage czy jest do skipowania gilotyny
                clean_df = df                                               # ta metoda bierze dane takie jakie przyszły
            else:
                parser = ExcelParser(df, sheet_name)                        # powołuje do zycia nasza gilotyne która obcina zbędne dane
                clean_df = parser.clean_dataframe()

            if clean_df.empty:                                              # sprwadza czy plik po czysczeniu jesli jest pusty pomijam ten arkusz i ide dalej
                continue

            print("Prawdziwa nazwa kolumny po odczycie:", [repr(col) for col in clean_df.columns], flush=True) # logi diagnostyczne
            print("Profil dostawcy:", mapping, flush=True)                                                     # flush=True wymaga pokazanie logu w dockerze
            print("Pierwsze wiersze pliku:", clean_df.head().to_string(), flush=True)

            solid_index_source_column = mapping.get("solid_index")          # pobieramy z mapingu pole solid_index

            if not solid_index_source_column:
                raise ValueError("Profil dostawcy nie ma mapowania dla pola solid_index.")

            if solid_index_source_column not in clean_df.columns:           # obsługa błędu jesli brakuje indeksu bryły
                raise ValueError(
                    f"Brakuje kolumny z indeksem bryły: {solid_index_source_column}. "
                    f"Dostępne kolumny: {list(clean_df.columns)}"
                )

            for _, row in clean_df.iterrows():                              # przechodzimy po kazdym wierszu tabeli _ oznacza indeks wiersza a row oznacza dane jednego produktu
                raw_solid_index = row[solid_index_source_column]            # pobieramy z wiersz surowy indeks bryły
                solid_index = self._clean_value(raw_solid_index)            # czyscimy surowa wartość z pustych poł np spacji przed po

                if not solid_index:                                         # jesli nie mamy indeksu bryły pomijamy taki wiersz
                    continue

                product_data = {                                            # tworzymy słownik produktu i wpisujemy do niego indeks bryły bo juz go pobralismy i wyczyscilismy ze smieci
                    "solid_index": solid_index
                }

                for model_field, source_name in mapping.items():            # przechodzisz po kazdym elemmencie mapingu dla kazdego pola modelu szuka odpowiedniego pola w pliku dostawcy
                    if model_field == "solid_index":                        # przez to że juz solid_index przerobilismy pomijamy go bo juz go mamy
                        continue

                    if source_name not in clean_df.columns:                 # sprawdzamy  czy kolumna z profilu fakytycznie istnieje
                        product_data[model_field] = None                    # jesli nie ma zapisujesz none
                        continue                                            # przechodzisz dalej

                    raw_value = row[source_name]                                            # pobierasz surową wartość z pliku
                    product_data[model_field] = self._clean_field_value(model_field, raw_value)   # czyscimy nasza wartość np z pustych pól

                results.append(product_data)                                # dodaje gotowy produkt do listy wyników

        return results







