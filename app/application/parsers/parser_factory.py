import pandas as pd

def get_parser_for_supplier(supplier_id: str, df: pd.DataFrame, sheet_name: str, active_profile: dict):
    """
    Wzorzec Fabryki (Factory Pattern).
    Na podstawie nazwy dostawcy, importuje i zwraca jego DEDYKOWANY parser.
    """
    if supplier_id == "LENART":
        from app.application.parsers.lenart_row_parser import LenartRowParser

        return LenartRowParser(df, sheet_name, active_profile)

    elif supplier_id == "MLMEBLE":
        from app.application.parsers.ml_meble_block_parser import MLMebleBlockParser

        return MLMebleBlockParser(df, sheet_name, active_profile)

    # Tutaj w przyszłości dodasz kolejnych dostawców:

    else:
        # Gwarancja bezpieczeństwa: jeśli zapomnisz napisać parsera, system głośno o tym powie!
        raise NotImplementedError(
            f"Krytyczny błąd: Brak dedykowanego parsera dla dostawcy {supplier_id}!"
        )