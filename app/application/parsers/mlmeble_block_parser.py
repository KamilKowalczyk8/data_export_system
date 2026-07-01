import pandas as pd
import re


class MLMebleBlockParser:
    """
    Specjalistyczny parser do odczytu plików dostawcy ML Meble,
    gdzie jeden produkt zajmuje wiele wierszy (struktura blokowa).
    """

    def __init__(self, df: pd.DataFrame, sheet_name: str, active_profile: dict):
        self.df = df
        self.sheet_name = sheet_name
        self.profile = active_profile
        self.excel_structure = active_profile.get("excel_structure", {})
        self.mapping = active_profile.get("mapping", {})

    def parse(self) -> list:
        """
        Główna metoda wywoływana przez serwis.
        Zwraca listę wyciągniętych i zmapowanych produktów.
        """
        results = []


        # do wytłumnaczenia
        header_row = [
            str(c) if not str(c).startswith("Unnamed:") else "" for c in self.df.columns
        ]
        data_rows = self.df.fillna("").values.tolist()
        all_rows = [header_row] + data_rows

        # 2. Wyciąganie globalnych atrybutów z pierwszych komórek (Kolekcja, Kolor)
        collection_name = ""
        global_color = ""
        front_color = ""

        if len(all_rows) > 0 and len(all_rows[0]) > 0:
            collection_name = str(all_rows[0][0]).strip()

        if len(all_rows) > 1 and len(all_rows[1]) > 0:
            global_color = str(all_rows[1][0]).strip()

        # Wyciąganie koloru samego frontu z ciągu np. "Korpus: Cashmere; Blat: MDF...; Front: MDF Cashmere"
        front_color_pattern = self.excel_structure.get(
            "front_color_pattern", r"Front:\s*([^.;]+)"
        )
        if global_color:
            match = re.search(front_color_pattern, global_color)
            if match:
                front_color = match.group(1).strip()

        # Ustawienia kolumn i wyszukiwania z profilu
        product_pattern = self.excel_structure.get(
            "product_name_pattern", r"^[A-ZĄĆĘŁŃÓŚŹŻ ]+\s\d{1,3}$"
        )
        name_cols = self.excel_structure.get("product_name_search_columns", [2, 3])
        label_col = self.excel_structure.get("dimension_label_column", 2)
        val_col = self.excel_structure.get("dimension_value_column", 3)
        price_col = self.excel_structure.get("price_column", 12)
        pkg_col = self.excel_structure.get("package_number_column", 5)

        dim_labels = self.excel_structure.get("dimension_labels", {})
        pkg_pattern = self.excel_structure.get("package_number_pattern", r"\d+\/(\d+)")

        current_product = None

        # 3. Główna pętla przelatująca przez wszystkie wiersze (Skaner Blokowy)
        for row in all_rows:
            is_new_product = False
            found_sku = ""

            # Sprawdzamy, czy w tym wierszu w kolumnach 2 lub 3 jest nazwa pasująca do "SANDRO 01"
            for col_idx in name_cols:
                if col_idx < len(row):
                    cell_val = str(row[col_idx]).strip()
                    if re.match(product_pattern, cell_val):
                        is_new_product = True
                        found_sku = cell_val
                        break

            if is_new_product:
                # Jeśli natrafiliśmy na nowy produkt, a stary był już budowany, wrzucamy go do worka z wynikami
                if current_product:
                    raw_results.append(current_product)

                # Inicjujemy nowy słownik produktu (nagłówek bloku)
                current_product = {
                    "solid_index": found_sku,
                    "collection": collection_name,
                    "color": global_color,
                    "front_color": front_color,
                }

                # Cena zazwyczaj znajduje się w pierwszym wierszu bloku produktu (Kolumna M / N)
                if price_col < len(row):
                    current_product["base_price"] = row[price_col]

            elif current_product:
                # Jeśli NIE jest to nowy produkt, ale `current_product` istnieje, to znaczy że jesteśmy "wewnątrz" bloku

                # Pobieramy wymiary (np. Szukamy "WYSOKOŚĆ (cm):" i bierzemy wartość obok)
                if label_col < len(row) and val_col < len(row):
                    label_val = str(row[label_col]).strip().upper()
                    cell_val = row[val_col]

                    for system_key, expected_label in dim_labels.items():
                        if expected_label.upper() in label_val:
                            current_product[system_key] = cell_val

                # Sprawdzamy numerację paczek (np. "1/3", "2/3", "3/3")
                if pkg_col < len(row):
                    pkg_val = str(row[pkg_col]).strip()
                    match = re.search(pkg_pattern, pkg_val)
                    if match:
                        # Regex `\d+\/(\d+)` chwyta wartość po ukośniku.
                        # Nadpisując to w pętli, produkt dostanie wartość ostatniej paczki (czyli np. 3)
                        current_product["number_packages"] = match.group(1)

        # Na samym końcu pętli pliku, dodajemy do wyników ostatni zbudowany produkt
        if current_product:
            raw_results.append(current_product)

        print(f"Zakończono parsowanie bloku. Wyciągnięto {len(raw_results)} produktów.")

        return results