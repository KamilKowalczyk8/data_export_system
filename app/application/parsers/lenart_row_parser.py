import pandas as pd
from app.application.parsers.excel_parser import ExcelParser

class LenartRowParser:
    """
    Parser obsługujący klasyczne pliki e-commerce o strukturze płaskiej tabeli (wiersz = produkt).
    Dla plilków od LENARTA
    """
    def __init__(self, df: pd.DataFrame, sheet_name: str, active_profile: dict):
        self.df = df
        self.sheet_name = sheet_name
        self.mapping = active_profile.get("mapping", {})
        self.skip_guillotine = active_profile.get("skip_guillotine", False)

    def parse(self) -> list:
        """
        Zwraca listę SUROWYCH (nieoczyszczonych) produktów zmapowanych
        na klucze systemowe od dostawcy LENART.
        """
        raw_results = []

        clean_df = self.df

        if clean_df.empty:
            return raw_results

        solid_index_source_column = self.mapping.get("solid_index")
        if (
            not solid_index_source_column
            or solid_index_source_column not in clean_df.columns
        ):
            raise ValueError(
                f"Brakuje kolumny z indeksem bryły: {solid_index_source_column}. "
                f"Dostępne kolumny: {list(clean_df.columns)}"
            )

        # Chodzenie po wierszach za pomocą iterrows()
        for _, row in clean_df.iterrows():          # przechodzimy po kazdym wierszu tabeli _ oznacza indeks wiersza a row oznacza dane jednego produktu
            raw_product = {}

            # Pobieramy surowy indeks
            raw_product["solid_index"] = row[solid_index_source_column]

            # Mapowanie kolumn z Excela na klucze systemu
            for model_field, source_name in self.mapping.items():
                if model_field == "solid_index":
                    continue

                if source_name not in clean_df.columns:
                    raw_product[model_field] = None
                else:
                    raw_product[model_field] = row[source_name]

            raw_results.append(raw_product)

        return raw_results