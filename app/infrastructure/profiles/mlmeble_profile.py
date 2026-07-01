PROFILE = {
    "supplier_id": "MLMEBLE",
    "file_type": "excel",
    "allowed_sheets": "selected",
    "skip_guillotine": True,

    "excel_structure": {
        "parser_type": "ml_meble_block",
        "show_sheet_select": True,

        # Kolekcja jest w komórce A1, np. SANDRO.
        "collection_cell": "A1",

        # Kolorystyka jest w komórce A2.
        # Tam może być Korpus, Blat, Front.
        "color_cell": "A2",

        # Nazwa produktu typu SANDRO 01, SANDRO 02, SANDRO 30
        "product_name_pattern": r"^[A-ZĄĆĘŁŃÓŚŹŻ ]+\s\d{1,3}$",
        "product_name_search_columns": [2, 3],

        "dimension_label_column": 2,
        "dimension_value_column": 3,

        "dimension_labels": {
            "height_block": "WYSOKOŚĆ",
            "width_block": "SZEROKOŚĆ",
            "depth_block": "GŁĘBOKOŚĆ",
            "weight": "WAGA OGÓLNA"
        },

        "package_number_column": 5,
        # Nazwa produktu typu SANDRO 01, SANDRO 02, SANDRO 30
        "package_number_pattern": r"\d+\/(\d+)",

        "price_column": 12,
        "price_mode": "formula_result",
        "price_base_column": 10,
        "price_contains": "zł",

        "front_color_pattern": r"Front:\s*([^.;]+)"
    },

    "mapping": {
        "solid_index": "product_name_pattern",
        "collection": "collection",
        "color": "color",
        "front_color": "front_color",
        "height_block": "height_block",
        "width_block": "width_block",
        "depth_block": "depth_block",
        "weight": "weight",
        "number_packages": "number_packages",
        "base_price": "base_price"
    }
}