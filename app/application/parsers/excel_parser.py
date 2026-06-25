import pandas as pd
from typing import Optional

class ExcelParser:
    """
    Parser będzie odpowiadał za to aby usunąć zbędne smieci(obrazy graficzne których na razie nie jesteśmy w stanie odczytać) które są nam zbędne i przygotowanie czystej tabeli
    """

    def __init__(self, df: pd.DataFrame, sheet_name: str):  # konstruktor przy wywołaniu tej funkcji potrzebujemy df: pd.DataFrame czyli surowe dane,  sheet_name: str - nazwa arkusza "MOND J B"
        self.raw_df = df.copy()                             # przypisujmey ten obiekt który mam z zewnątrz do naszego klona (raw_df)
        self.sheet_name = sheet_name                        # przypisujemy nazwe arkusza żeby przy ewentualnym błedzie wypisać arkusz MOND znaleziono bład

    def find_header_row_index(self) -> Optional[int]:       # funkcja tam zwróci nam liczne całkowitą w którym wierszu leży nagłowek,
        """                                                 # Optional jesli będą puste zwróci None
        jest to funkcja która przeczyta nam początek pliku w celu znalezienia nagłówka żeby wiedzieć od którego pliku zaczynają się dane
        Działa jak radar - szuka wiersza z największą liczbą wpisanych danych.
        """
        max_non_empty_cells = 0                             # zmienna która będzie zliczać ilość danych w danym wierszu póki co na sztywno 0
        header_index = None                                 # numer wiersza od którego zaczynają się dane

        for index, row in self.raw_df.head(10).iterrows():  # skanuje tylko pierwsze 10 wierszy w celu znalezienia od którego wiersza zaczynają sie poprawne dane
            current_non_empty = row.count()                 # do zmiennej current_non_empty zliczamy ile ma danych

            #jeśli current_non_empty ma więcej danych niż nasz max max_non_empty_cells to zapisujemy go
            if current_non_empty > max_non_empty_cells:
                max_non_empty_cells = current_non_empty     # zapisujemy do naszego maxa ile danych ma
                header_index = index                        # zapisujemy index tego wiersza z największą ilością danych

        return header_index

    def clean_dataframe(self) -> pd.DataFrame:    # pd.DataFrame: Deklarujemy twardo: "Nieważne co się stanie w środku, ta funkcja na końcu ma "wypluć" obiekt w postaci tabeli".
        """
        Mechanizm czyszczący używa find_header_row_index żeby odciąć te dane które są nam zbędne
        """
        header_idx = self.find_header_row_index()     # wywołujemy naszą funkcje jesli liczba 6 to liczba w której znalazł najwiecej tekstu to ta jest zapisana do header_idx

        if header_idx is None:                                              # if na wypadek jakby nie udało się znaleźć nagłówków
            print(f"[{self.sheet_name}] BŁĄD: Nie odnaleziono nagłówków.")
            return pd.DataFrame()                                           # zwracamy pustą tabele jesli zeskanował arkusz i znalazł same puste pola

        # odcinanie wszystkiego powyżej naszego nagłówka
        cleaned_df = self.raw_df.iloc[header_idx:].copy()           # .iloc słuzy do namierzania wierszy po ich numerach(indeksach)
                                                                    # [header_idx:] oznacz "od - do"  czyli np od 6 [6:] do samego dołu
                                                                    # i używamy .copy()  kopiujemy i tworzymy odeseprowanego klona
        # ustawianie tego wiersza jako nazwy kolumn w pamięci ram
        cleaned_df.columns = cleaned_df.iloc[0]                     # tabela cleaned_df jest juz obcięta
                                                                    # Właściwość .columns to w pandas miejsce, gdzie przechowywane są oficjalne etykiety tabeli.
                                                # iloc[0] mówi weź pierwszy wiersz moich danych i wklej go jako tytuły kolumn

        cleaned_df = cleaned_df[1:]             # usuwamy wiersz 0 bo stał sie nagłówkiem i nadpisujemy tabele i zaczynamy ja od [1:]

        # mimo że obcieliśmy 6 pierwszych wierszy to tabele pamiętają stare numery ta linjka resetuje numeracje takżeby pierwszy mebel dostał 0 a drugi 1
        cleaned_df = cleaned_df.reset_index(drop=True)      # drop=True wyrzuca stare wiersze definitywnie do kosza

        return cleaned_df       # zwracany czystą poprawioną tabele
