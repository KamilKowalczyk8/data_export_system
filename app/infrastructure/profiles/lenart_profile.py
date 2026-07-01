PROFILE = {
    "supplier_id": "LENART",        # nazwa kolekcji
    "file_type": "csv",             # typ pliku
    "delimiter": ";",               # CSV polskich dostawców najczęściej używa średnika
    "encoding": "utf-16",
    "allowed_sheets": [None],
    "skip_guillotine": True,
    "mapping": {
        "solid_index": "indeks bryly",

        "collection": "nazwa kolekcji",
        "color": "kolorystyka",
        "marking_fronts": "oznaczenie frontow",
        "solid_type": "typ bryly",
        "front_color": "front kolorystyka",
        "weight": "waga netto bryly",
        "width_block": "szerokosc bryly",
        "height_block": "wysokosc bryly",
        "depth_block": "glebokosc bryly",
        
        "number_doors": "ilosc drzwi",
        "number_drawers": "ilosc szuflad",

        "handle_material": "uchwyt material",
        "drawer_type": "prowadnica szuflady rodzaj",
        "hinge_type": "zawias rodzaj",
        "description_block": "opis bryly",
        "number_packages": "ilosc paczek",

        "bed_frame_material": "stelaz material typ",
        "shelf_material": "polka rodzaj grubosc materialu",
        "equipment_product": "wyposazenie bryl"

    }
}