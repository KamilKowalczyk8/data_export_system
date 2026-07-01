import re

from app.application.config.field_types import FLOAT_FIELDS

def clean_value(value):  # ta metoda czyści nie zapisuje wartosci jesli któres z tych warunków sie zdarzy np będzie puste pole
    """
    Czyści pojedynczą wartośc String z pliku puste wartosci zamienai na None
    """
    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    if value.lower() in ["nan", "none", "null"]:
        return None

    return value


def clean_float_value(value):  # odpowiednik tej funkcji wyżej ale dla floatów
    """
    Czyści wartości liczbowe
    obsługuje:
        - "44.0 kg"
        - "79,5 kg"
        - "209 cm -> 209 -> 209.0"
        - "3"
        - "1,0"
    Jeśli nie da się odczytać liczby, zwraca None.
    """
    if value is None:
        return None

    value = str(value).strip()  # zamienia wartosc na tekst i usuwa spacje z przodu i z tyłu
    if value == "":
        return None

    if (value.lower() in ["nan", "none", "null"]):  # jesli plik lub pandas zwróci któryś z tych wartosci to traktujemy to jako brak wartosci
        return None

    value = value.lower()  # zamieniamy tekst na małe litery
    value = value.replace(",", ".")  # zamieniamy , na . gdyż python potrzebuje kroppki do zrobienia wartosci float

    match = re.search(r"\d+(\.\d+)?", value)  # słuzy do znajdowanai cyfry w teksice \d+ to zajduje np 10 a \.(\d+ znajduje 0.5 co daje nam całośc 10.5

    if not match:  # jesli nie znaleziono liczby wyrzyca None
        return None

    return float(match.group())  # zwracasz znalezioną liczbe float


def clean_field_value(field_name, value):
    """
    czysci pola zaleznie od pola modeli string lub flaot
    pola z FLOAT_FIELDS czsyci jako float
    a pozostałe jako string
    """
    if field_name in FLOAT_FIELDS:
        return clean_float_value(value)

    return clean_value(value)