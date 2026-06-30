from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
import logging

from app.application.services.import_preview_service import ImportPreviewService
from app.infrastructure.profiles.profile_registry import get_active_profiles
from app.infrastructure.database.database import get_db

logger = logging.getLogger(__name__)                                # logger ustawiamy by widzieć błędy w konsoli

router = APIRouter(prefix="/api/import", tags=["Import danych"])    # router obsługuje wszystkie zapytania pod adresem api/import

configuration_profiles = get_active_profiles()                      #pobieramy słownik profili

@router.post("/preview", tags=["Import danych surowych do zatwierdzenia"])
async def data_import(
    file: UploadFile = File(..., description="Plik CSV lub Excel od dostawcy"),
    supplier: str = Form(..., description="Nazwa profilu dostawcy, np. LENART"),
    db: Session = Depends(get_db),                      # daje temu endpointowi połaczenie z bazą
):
    """
    Główny endpoint do importu plików produktowych.
    Odbiera plik, odczytuje go do pamięci i przekazuje do Warstwy Usług.
    """
    try:
        file_contents = await file.read()

        import_preview_service = ImportPreviewService(
            available_profiles=configuration_profiles,  # przekazujemy profile
            db = db                                     # przekazujemy to połączenie do serwisu importu, żeby mógł zapisywać dane do PostgreSQL.
        )

        result = await import_preview_service.process_preview_import(
            supplier=supplier,
            file_name=file.filename,
            file_content=file_contents
        )
        return result

    except ValueError as e:     #valueerror to bład biznesowy (np. zły dostawca, zły format)
        logger.warning(f"Błąd walidacji podczas importu: {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:      # wyjątki np błędy pydantica ,brak ramu przykłądowo
        logger.error(f"Krytyczny błąd serwera podczas importu: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Wystąpił nieoczekiwany błąd serwera. Skontaktuj się z administratorem."
        )

@router.get("/current")                 # metoda do importowanai danych które aktualnie są w tabeli
async def get_current_import_preview(
    db: Session = Depends(get_db),
):
    try:
        import_preview_service = ImportPreviewService(
            available_profiles=configuration_profiles,
            db=db
        )

        products = import_preview_service.get_current_preview_products()

        rows = []

        for product in products:
            rows.append({
                "id": product.id,
                "import_id": product.import_id,
                "supplier_id": product.supplier_id,
                "product_key": product.product_key,
                "solid_index": product.solid_index,
                "collection": product.collection,
                "color": product.color,
                "marking_fronts": product.marking_fronts,
                "solid_type": product.solid_type,
                "front_color": product.front_color,
                "weight": product.weight,
                "width_block": product.width_block,
                "height_block": product.height_block,
                "depth_block": product.depth_block,
                "number_doors": product.number_doors,
                "number_drawers": product.number_drawers,
                "handle_material": product.handle_material,
                "drawer_type": product.drawer_type,
                "hinge_type": product.hinge_type,
                "description_block": product.description_block,
                "number_packages": product.number_packages,
                "bed_frame_material": product.bed_frame_material,
                "shelf_material": product.shelf_material,
                "equipment_product": product.equipment_product,
                "status": product.status.value if hasattr(product.status, "value") else product.status,
                "created_at": product.created_at.strftime("%d.%m.%Y %H:%M") if product.created_at else None,
                "updated_at": product.updated_at.strftime("%d.%m.%Y %H:%M") if product.updated_at else None,
            })

        return {
            "status": "success",
            "count": len(rows),
            "rows": rows
        }

    except Exception as e:
        logger.error(f"Błąd pobierania aktualnych danych tymczasowych: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Nie udało się pobrać aktualnych danych tymczasowych."
        )





@router.get("/preview/{import_id}")
async def get_import_preview(               # asynchroniczna bo łatwiej obsugiwać wiele requestów
        import_id: str,                     # parametr wypełniany z adresu {import_id}
        db: Session = Depends(get_db),      # tworzymy sesje połączenia Session z sqlalchemy db-oznacza sesje połączenia z bazą danych    #daj tej funkcji dostęp do PostgreSQL
):
    try:
        import_preview_service = ImportPreviewService(
            available_profiles=configuration_profiles,
            db = db                                     # db po lewej to nazwa parametru a po prawej to sesja bazy danych
        )

        products = import_preview_service.get_preview_products(import_id)

        rows = []

        for product in products:
            rows.append({
                "id": product.id,
                "import_id": product.import_id,
                "supplier_id": product.supplier_id,
                "product_key": product.product_key,
                "solid_index": product.solid_index,
                "collection": product.collection,
                "color": product.color,
                "marking_fronts": product.marking_fronts,
                "solid_type": product.solid_type,
                "front_color": product.front_color,
                "weight": product.weight,
                "width_block": product.width_block,
                "height_block": product.height_block,
                "depth_block": product.depth_block,
                "number_doors": product.number_doors,
                "number_drawers": product.number_drawers,
                "handle_material": product.handle_material,
                "drawer_type": product.drawer_type,
                "hinge_type": product.hinge_type,
                "description_block": product.description_block,
                "number_packages": product.number_packages,
                "bed_frame_material": product.bed_frame_material,
                "shelf_material": product.shelf_material,
                "equipment_product": product.equipment_product,
                "status": product.status.value if hasattr(product.status, "value") else product.status,
                "created_at": product.created_at.isoformat() if product.created_at else None,
                "updated_at": product.updated_at.isoformat() if product.updated_at else None,
            })

        return {
            "status": "success",
            "import_id": import_id,
            "count": len(rows),
            "rows": rows
        }

    except Exception as e:
        logger.error(f"Błąd pobierania danych podglądu importu: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Nie udało się pobrać danych podglądu importu."
        )