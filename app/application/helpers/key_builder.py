def build_product_key(product_data: dict) -> str:
    """Buduje unikalny klucz produktu na podstawie jego atrybutów."""
    parts = [
        product_data.get("supplier_id"),
        product_data.get("collection"),
        product_data.get("solid_index"),
        product_data.get("solid_type"),
        product_data.get("marking_fronts"),
        product_data.get("color"),
    ]
    clean_parts = []

    for part in parts:
        if part is None:
            part = " "

        part = str(part).strip().upper()

        part = part.replace(" ", "_")
        part = part.replace(",", "_")
        part = part.replace("\\", "_")

        clean_parts.append(part)

    return " - ".join(clean_parts)