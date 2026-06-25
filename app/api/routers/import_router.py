from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
import logging

from app.application.services.import_service import ImportService
from app.infrastructure.profiles.profile_registry import get_active_profiles
from app.infrastructure.database.database import get_db

logger = logging.getLogger(__name__)                                # logger ustawiamy by widzieć błędy w konsoli

router = APIRouter(prefix="/api/import", tags=["Import danych"])    # router obsługuje wszystkie zapytania pod adresem api/import

configuration_profiles = get_active_profiles()                      #pobieramy słownik profili

@router.post("")
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

        import_service = ImportService(
            available_profiles=configuration_profiles,  # przekazujemy profile
            db = db                                     # przekazujemy to połączenie do serwisu importu, żeby mógł zapisywać dane do PostgreSQL.
        )

        result = await import_service.process_import(
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

