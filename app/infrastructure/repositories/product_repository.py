from sqlalchemy.orm import Session
from sqlalchemy.orm.sync import update

from app.infrastructure.database.db_models.product_model import ProductModel

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_products(self, products_data: list[dict]) -> dict:
        saved_count = 0         # zlicza zapisane elementy
        updated_count = 0       # zlicza aktualizowane elementy
        skipped_count = 0       # zlicza pominięte elementy

        for products_data in products_data:     # robimy pętle która wykona się tyle razy ile mamy produktów
            solid_index = products_data.get("solid_index")

            if not solid_index:                 # pomija ten produkt jesli nie ma w nim indeksu bo to główny identyfiaktor
                skipped_count += 1
                continue

            existing_product = (                # spradzamy czy produkt istnieje o takim solid_index
                self.db.query(ProductModel)
                .filter(ProductModel.solid_index == solid_index)
                .first()                        # pobiera pierwszy znaleziony rekord. Jeśli produkt istnieje, existing_product będzie obiektem produktu. Jeśli nie istnieje, existing_product będzie None.
            )

            if existing_product:
                for field_name, value in products_data.items():     # pętla przechodzi po każdym elemencie np field_name=color i value= wartość tego pola kaszmir
                    if hasattr(existing_product, field_name):       # sprwadza nasz ProductModel czy posiada takie pole. na taki wypadek "smieci":"abc" to sprawdzi nasz modal i zobaczy że nie ma takiego pola i nie zapisze tego
                        setattr(existing_product, field_name, value)# to dynamiczny zapis do aktualizacji naszego pola w istniejącym produkcie

                updated_count += 1

            else:                                           # jesli nie znaleziono takiego produktu to dodaje nowy
                product = ProductModel(**products_data)     # tworzy nowy obiekt
                self.db.add(product)                        # dodajemy nowy produkt do sesji bazy przygotowuje zapis
                saved_count += 1
        self.db.commit()                                    # zatwierdza nasze zmiany w bazie

        return {
            "saved_count": saved_count,
            "updated_count": updated_count,
            "skipped_count": skipped_count
        }


