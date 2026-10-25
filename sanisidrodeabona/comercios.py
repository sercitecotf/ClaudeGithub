"""Directorio de comercios. Datos tomados de directorios públicos (oct. 2026),
SIN verificar con cada negocio: confirmar y completar teléfono/web antes de publicar.

category: food | stay | shop | services | activities
"""


def n(name, category, es, en, de, address=None):
    c = {"name": name, "category": category, "desc": {"es": es, "en": en, "de": de}}
    if address:
        c["address"] = address
    return c


COMERCIOS = [
    n("Cafetería Avenida San Isidro", "food", "Bar familiar con bocadillos y zumos naturales.",
      "Family-run bar with sandwiches and fresh juices.", "Familiengeführte Bar mit Sandwiches und frischen Säften.", "Avenida principal, San Isidro"),
    n("Centro Asturiano Tenerife Sur", "food", "Cafetería con variedad de desayunos.",
      "Café with a wide choice of breakfasts.", "Café mit großer Frühstücksauswahl.", "Avenida principal, San Isidro"),
    n("Bar Cafetería Extra", "food", "Bar cafetería conocido por sus bocadillos y tartas.",
      "Café-bar known for its sandwiches and cakes.", "Café-Bar, bekannt für Sandwiches und Kuchen.", "Avenida principal, San Isidro"),
    n("MiArepa San Isidro", "food", "Cocina venezolana: arepas y empanadas. Conviene reservar.",
      "Venezuelan cuisine: arepas and empanadas. Booking is advisable.", "Venezolanische Küche: Arepas und Empanadas. Reservierung empfohlen."),
    n("Selfie Pizza", "food", "Pizzería en San Isidro.", "Pizzeria in San Isidro.", "Pizzeria in San Isidro."),
    n("Coviran San Isidro", "shop", "Supermercado de barrio en San Isidro.",
      "Neighbourhood supermarket in San Isidro.", "Nachbarschaftssupermarkt in San Isidro.", "Calle Benedicto XVI 23, San Isidro"),
]
