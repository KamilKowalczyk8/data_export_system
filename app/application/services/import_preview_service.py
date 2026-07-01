import os
import uuid
from typing import Dict, Any

from app.infrastructure.importers.file_importer import FileImporter
from app.infrastructure.repositories.product_preview_repository import ProductPreviewRepository
from app.application.helpers.data_cleaner import clean_value, clean_field_value
from app.application.helpers.key_builder import build_product_key
from app.application.parsers.parser_factory import get_parser_for_supplier

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
                product_data["product_key"] = build_product_key(product_data)

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

    def _read_excel(self, importer: FileImporter, profil: dict) -> dict:
        """ Metoda dla odczytu plików Excel """
        return importer.load_all_sheets()

    def _read_csv(self, importer: FileImporter, profil: dict) -> dict:
        """ Metoda dla odczytu csv """
        return importer.load_csv(
            delimiter=profil.get("delimiter", ";"),         # jesli nie otrzyma dancyh z profilu to domślnie ustawaia  te dane ; i utf-8
            encoding=profil.get("encoding", "utf-8")
        )


    def _map_data(self, sheets_data: dict, active_profile: dict) -> list:   # _ prywatna metoda
        """
        Główna metoda dystrybucyjna. Wybiera odpowiedni parser na podstawie profilu,
        odbiera surowe dane i przepuszcza je przez logikę czyszczącą.
        """
        results = []
        if not sheets_data:                                                 # sprawdzenie czy otrzymaliśmy dane
            return results                                                  # jesli nie zwraca pustą liste

        supplier_id = active_profile.get("supplier_id")

        for sheet_name, df in sheets_data.items():
            parser = get_parser_for_supplier(
                supplier_id, df, sheet_name, active_profile
            )

            raw_parsed_data = parser.parse()

            for raw_product in raw_parsed_data:
                clean_product = {}

                raw_solid_index = raw_product.get("solid_index")
                solid_index = clean_value(raw_solid_index)

                if not solid_index:
                    continue

                clean_product["solid_index"] = solid_index

                for field_name, raw_value in raw_product.items():
                    if field_name == "solid_index":
                        continue

                    clean_product[field_name] = clean_field_value(
                        field_name, raw_value
                    )

                results.append(clean_product)  # dodaje gotowy produkt do listy wyników

        return results







