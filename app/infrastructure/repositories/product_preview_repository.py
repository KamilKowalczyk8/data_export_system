from sqlalchemy.orm import Session

from app.infrastructure.database.db_models.product_preview_model import ProductPreviewModel


class ProductPreviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_products(self, product_preview_data: list[dict]) -> dict:
        saved_count = 0  # zlicza zapisane elementy
        #updated_count = 0  # zlicza aktualizowane elementy
        skipped_count = 0  # zlicza pominięte elementy

        self.db.query(ProductPreviewModel).delete(synchronize_session=False)    # czyscimy baze z starych danych gdy importujemy nowy plik

        for product_preview_data in product_preview_data:  # robimy pętle która wykona się tyle razy ile mamy produktów
            solid_index = product_preview_data.get("solid_index")
            supplier_id = product_preview_data.get("supplier_id")
            import_id = product_preview_data.get("import_id")  # paramettr importu konkretnego id

            if not solid_index:  # pomija ten produkt jesli nie ma w nim indeksu bo to główny identyfiaktor
                skipped_count += 1
                continue

            if not import_id:
                skipped_count += 1
                continue

            if not supplier_id:
                skipped_count += 1
                continue

            product = ProductPreviewModel(**product_preview_data) # tworzy nowy obiekt
            self.db.add(product)                    # dodajemy nowy produkt do sesji bazy przygotowuje zapis
            saved_count += 1

        self.db.commit()                            # zatwierdza nasze zmiany w bazie

        return {
            "saved_count": saved_count,
            "skipped_count": skipped_count
        }

    def get_product_by_import_id(self, import_id: str) -> list[ProductPreviewModel]:
        return (
            self.db.query(ProductPreviewModel)
            .filter(ProductPreviewModel.import_id == import_id)
            .order_by(ProductPreviewModel.id.asc())
            .all()
        )

    def get_current_preview_products(self) -> list[ProductPreviewModel]:
        return (
            self.db.query(ProductPreviewModel)
            .order_by(ProductPreviewModel.id.asc())
            .all()
        )