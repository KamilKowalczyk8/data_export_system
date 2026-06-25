import os
from app.infrastructure.importers.file_importer import FileImporter
from app.application.parsers.excel_parser import ExcelParser
from app.infrastructure.profiles.helvetica_profile import PROFILE as helvetica_prof

def process_helvetica():
    print("--- START DEDYKOWANEGO IMPORTU: HELVETICA ---")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", "input", "harmony.csv")

    if not os.path.exists(file_path):
        print(f"BŁAD: Brak pliku {file_path}")
        return

    importer = FileImporter(file_path)                              #tworzymy instacje klasy fileimporter zeby uzyc jej metod
    sheets_data = importer.load_csv(delimiter=helvetica_prof["delimiter"]) # uzywamy metody load_csv i kazemy pobrac delimiter z profilu dostawcy

    df = sheets_data.get("default_csv_data")                #wprowadzamy do zmiennej df naszą tabele z nazwa
    if df is None or df.empty:
        print("Plik jest pusty")
        return

    # odpalenie naszego czysczenia zbędnych wierszy w razie gdyby plik się różnił tak zapobiegawczo
    parser = ExcelParser(df, sheet_name="HELVETICA_CSV")    # sheet_name="HELVETICA_CSV" to sztuczna nazwa dla naszego parsera
    clean_df = parser.clean_dataframe()  # zmienna na czyste dane po pracy parsera

    if clean_df.empty:
        print("Nie udało się odzyskać danych.")  # sprawdzamy czy po czysczeniu jakieś dane zostały
        return

    print("Sukces! Pobrano dane Helveticy. Nazwy kolumn:")
    print(list(clean_df.columns))

    print("\nTrwa przygotowywanie danych do zapisu w bazie...")

    #
    # mapowanie na obiekt domeny i zapis do bazy w pętli przejdziemy przez clean_df i zapiszemy do bazy
    #

    print("Zakończono import do bazy danych.")

if __name__ == "__main__":
    process_helvetica()