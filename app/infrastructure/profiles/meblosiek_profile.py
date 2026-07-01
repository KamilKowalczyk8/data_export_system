PROFILE = {
    "supplier_id": "MEBLOSIEK",    # dostawca
    "file_type": "excel",           # typ pliku
    "allowed_sheets": ["MOND"],     # nazwa kolekcji
    "skip_guillotine": False,
    "mapping": {
        "solid_index": "INDEKS\nARTICLE NUMBER",
        "opis": "OPIS \nDESCRIPTION",
        "base_price": "CENA BAZOWA/SZT\nBASE PRICE/PC",
        "box_quantity": "ILOŚĆ PACZEK\nBOX QUANTITY"
    }
}