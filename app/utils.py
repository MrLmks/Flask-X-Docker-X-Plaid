
def mapping_logos(billing_entity):
    logos_mapping = {
        "McDonald's": "img/mcdonalds.png",
        "Starbucks": "img/Starbucks.png",
        "Uber": "img/uber.webp",
        "United Airlines": "img/unitedairlines.jpeg"
    }
    return logos_mapping.get(billing_entity, "/img/FUN.jpg")