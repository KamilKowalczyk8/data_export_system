PROFILE = {
    "supplier_id": "MEBLEOSIEK",    # dostawca
    "file_type": "excel",           # typ pliku
    "allowed_sheets": ["MOND"],     # nazwa kolekcji
    "skip_guillotine": False,
    "mapping": {
        "supplier_index": "INDEKS\nARTICLE NUMBER",
        "description": "OPIS \nDESCRIPTION",
        "base_price": "CENA BAZOWA/SZT\nBASE PRICE/PC",
        "box_quantity": "ILOŚĆ PACZEK\nBOX QUANTITY"
    }
}