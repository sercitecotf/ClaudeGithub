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
    n("La Boca Rie", "food", "Restaurante de cocina francesa con vistas al mar en Playa San Juan.",
      "French restaurant with sea views in Playa San Juan.", "Französisches Restaurant mit Meerblick in Playa San Juan."),
    n("San Juan Creativo", "food", "Restaurante que combina cocina española y danesa en Playa San Juan.",
      "Restaurant combining Spanish and Danish cuisine in Playa San Juan.", "Restaurant mit spanischer und dänischer Küche in Playa San Juan."),
    n("Las Estrellas", "food", "Restaurante de cocina local en Playa San Juan.",
      "Local cuisine restaurant in Playa San Juan.", "Restaurant mit lokaler Küche in Playa San Juan."),
    n("Bar-Restaurante Brisa Marina", "food", "Bar-restaurante en Playa San Juan, valorado por su pescado fresco.",
      "Bar-restaurant in Playa San Juan, praised for its fresh fish.", "Bar-Restaurant in Playa San Juan, geschätzt für seinen frischen Fisch."),
    n("La Bodeguita", "food", "Tapas canarias y platos ucranianos en Playa San Juan.",
      "Canarian tapas and Ukrainian dishes in Playa San Juan.", "Kanarische Tapas und ukrainische Gerichte in Playa San Juan."),
    n("Las Parrillitas Bar Restaurante", "food", "Bar-restaurante en Playa San Juan.",
      "Bar-restaurant in Playa San Juan.", "Bar-Restaurant in Playa San Juan.", "Calle Marejada 21, Playa San Juan"),
    n("Bar Restaurante Antonio", "food", "Bar-restaurante en Playa San Juan.",
      "Bar-restaurant in Playa San Juan.", "Bar-Restaurant in Playa San Juan.", "Avenida El Emigrante 38, Playa San Juan"),
    n("Sesto Senso Restaurant", "food", "Restaurante en Playa San Juan.", "Restaurant in Playa San Juan.", "Restaurant in Playa San Juan."),
    n("La Luna en Playa San Juan", "food", "Restaurante en Playa San Juan.", "Restaurant in Playa San Juan.", "Restaurant in Playa San Juan."),
    n("Restaurante La Lonja", "food", "Restaurante en la zona de Playa San Juan.", "Restaurant in the Playa San Juan area.", "Restaurant in der Gegend von Playa San Juan."),
    n("Taberna Marinera Agua y Sal", "food", "Taberna en la zona de Playa San Juan.", "Tavern in the Playa San Juan area.", "Taverne in der Gegend von Playa San Juan."),
    n("Kabuki (Abama)", "food", "Restaurante con estrella Michelin en el hotel de Abama.",
      "Michelin-starred restaurant in the Abama hotel.", "Restaurant mit Michelin-Stern im Hotel Abama."),
    n("Supermercado 5 Océanos", "shop", "Supermercado en el centro de Guía de Isora.",
      "Supermarket in the centre of Guía de Isora.", "Supermarkt im Zentrum von Guía de Isora.", "Avenida Juan Carlos I, 7, Guía de Isora"),
    n("Guía de Isora Cooperativa Agrícola", "shop", "Cooperativa de comercialización de frutas y hortalizas.",
      "Cooperative marketing fruit and vegetables.", "Genossenschaft für den Vertrieb von Obst und Gemüse.", "Carretera General de Tejina de Guía, 20"),
]
