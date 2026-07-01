from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import import_router
from app.infrastructure.database.database import Base, engine

def create_app() -> FastAPI:
    """
    (Application Factory).
    To wzorzec projektowy, który czysto inicjalizuje nasz serwer.
    """
    app = FastAPI(
        title="Enterprise Data Export System",
        description="System integracji i standaryzacji danych produktowych",
        version="1.0.0"
    )

    Base.metadata.create_all(bind=engine)

    # CORS - Kluczowe zabezpieczenie. Zezwala naszemu interfejsowi Nginx
    # (działającemu w przeglądarce) na wysyłanie plików do tego API.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(import_router.router)

    return app
app = create_app()