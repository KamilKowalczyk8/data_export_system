import pandas as pd
from typing import Dict

class FileImporter:
    """
    Klasa która będzie tlyko i wyłącznie odpowiedzialna za fizyczny odczyt danych z pliku .xlsx
    Jej zadaniem jest wczytanie plików do pamięci RAM przy użyciu biblioteki pandas
    """

    def __init__(self, file_path: str):         # Konstruktor klasy uruchamia się automatycznie (self to odpowiednik this w javie oznacza ten konkretny obiekt)
        self.file_path = file_path              # zapisuje scieżkę do pliku do zmiennej file_path po to aby inne metody w tym pliku mogły korzystać z tej scieżki używając aby zmiennej

    def load_all_sheets(self) -> Dict[str, pd.DataFrame]:
        """
        Odczytuje plik .xlsx i zwraca słownik (klucz -> wartość)
        Klucz: nazwa arkusza (Mond J Black)
        Wartość: pd.DataFrame (magiczna tabela z biblioteki pandas która jest gotowa do obróbki)
        """
        print(f"Rozpoczynam odczyt pliku: {self.file_path} ...")

        try:
                                                                                            # engine='openpyxl' to silnik który będzie sobie radził z naszym plikiem .xlsx
            sheets = pd.read_excel(self.file_path, sheet_name=None, engine="openpyxl")      #pd skrót od pandas read_excel gotowa funkcja od pandas na czytanie plików excelowych.
                                                                                            # self.file_path pierwszy argument scieżka
                                                                                            # sheet_name=None nie wskazje konkretnego tylko oznacza "wczytaj wszystkie arkusze z pliku"
            print(f"Sukces! Odczytano {len(sheets)} arkuszy.")
            return sheets

        except Exception as e:
            print(f"Błąd krytyczny podczas odczytu pliku nie powiodło się przez: {e}")
            return {}

    def load_csv(self, delimiter: str = ";", encoding: str = "utf-8") -> Dict[str, pd.DataFrame]:
        """
        -> Dict[str, pd.DataFrame] obiecujemy że na koncu zwrocimy słownik str - to nazwa zakładki a pd.DataFrame tabela z danymi
        Otwiera plik CSV i pakuje go w słownik symulując jedną zakładke dzieki temu excel i csv są traktowane identycznie
        :param delimiter: to separator między kolumnami
        :return:
        """
        try:
            df = pd.read_csv(self.file_path, delimiter=delimiter, encoding=encoding)     # pd.read_csv(...) to biblioteka do czytania plików tekstowych
                                                                                        # delimiter to jak dostawca oddzielił kolumny między sobą ;
            return {"default_csv_data": df}                 # oszukujemy nasz system tworzymy zakładke gdyż system oczekuje zakładki i nazywamy ją default_csv_data i podpinamy pod nią tabele (df)
        except Exception as e:
            print(f"Błąd odczytania pliku CSV: {e}")
            return {}                                       # zwracamy pusty słownik aby nie wywaliło nam krytycznego błedu error gdyż obiecujemy zwrócic słownik