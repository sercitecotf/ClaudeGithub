#!/usr/bin/env python3
"""Genera sanisidrodeabona.com en español (raíz), inglés (/en/) y alemán (/de/).

Uso:  python3 build.py
Edita el contenido aquí (y los negocios en comercios.py) y vuelve a ejecutar.
La estructura y las páginas legales viven en ../tools/tourism_lib.py.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent / "tools"))
sys.path.insert(0, str(ROOT))
from tourism_lib import build  # noqa: E402
from comercios import COMERCIOS  # noqa: E402

DOMAIN = "sanisidrodeabona.com"
LOGO = 'San Isidro <span>de Abona</span>'

ZONA = {"es": "San Isidro de Abona", "en": "San Isidro de Abona", "de": "San Isidro de Abona"}

TAGLINE = {
    "es": "Guía local de San Isidro de Abona, Tenerife",
    "en": "Local guide to San Isidro de Abona, Tenerife",
    "de": "Lokaler Reiseführer für San Isidro de Abona, Teneriffa",
}

NAV = {
    "es": [("index.html", "Inicio"), ("que-hacer.html", "Qué hacer"), ("comer.html", "Dónde comer"),
           ("dormir-cerca-aeropuerto.html", "Dormir cerca del aeropuerto"), ("como-llegar.html", "Cómo llegar"),
           ("comercios.html", "Comercios")],
    "en": [("index.html", "Home"), ("que-hacer.html", "Things to do"), ("comer.html", "Where to eat"),
           ("dormir-cerca-aeropuerto.html", "Stay near the airport"), ("como-llegar.html", "Getting here"),
           ("comercios.html", "Local businesses")],
    "de": [("index.html", "Startseite"), ("que-hacer.html", "Aktivitäten"), ("comer.html", "Essen"),
           ("dormir-cerca-aeropuerto.html", "Übernachten am Flughafen"), ("como-llegar.html", "Anreise"),
           ("comercios.html", "Geschäfte")],
}

HOME = {
    "es": dict(
        title="San Isidro de Abona: qué hacer, dónde comer y dormir cerca del aeropuerto",
        description="Guía local de San Isidro de Abona, Tenerife: qué hacer, dónde comer, alojamiento cerca del aeropuerto Tenerife Sur y cómo llegar.",
        body="""<section class="hero">
  <div class="wrap">
    <h1>San Isidro de Abona, el sur de Tenerife más auténtico</h1>
    <p>Guía práctica del pueblo y su entorno: qué hacer, dónde comer, dónde dormir cerca del aeropuerto Tenerife Sur y cómo moverte.</p>
    <a class="btn" href="dormir-cerca-aeropuerto.html">Dormir cerca del aeropuerto</a>
  </div>
</section>
<main>
  <div class="wrap">
    <h2 style="margin-top:0">Qué encontrarás aquí</h2>
    <div class="grid">
      <a class="card" href="que-hacer.html"><h3>Qué hacer</h3><p>Planes y rincones del pueblo y de los alrededores.</p></a>
      <a class="card" href="comer.html"><h3>Dónde comer</h3><p>Cocina canaria y sitios de la zona.</p></a>
      <a class="card" href="dormir-cerca-aeropuerto.html"><h3>Dormir cerca del aeropuerto</h3><p>Útil si llegas tarde o sales temprano.</p></a>
      <a class="card" href="como-llegar.html"><h3>Cómo llegar y moverse</h3><p>Aeropuerto, autopista, guagua y alquiler de coche.</p></a>
      <a class="card" href="comercios.html"><h3>Comercios de la zona</h3><p>Negocios locales: apoya el comercio de cercanía.</p></a>
    </div>
    <h2>Sobre San Isidro de Abona</h2>
    <p>San Isidro es un pueblo del sur de Tenerife, en la comarca de Abona, muy cerca del aeropuerto Tenerife Sur y de las principales vías de la isla. Es un buen punto de partida para conocer el sur sin las aglomeraciones de las zonas más turísticas.</p>
  </div>
</main>""",
    ),
    "en": dict(
        title="San Isidro de Abona: things to do, where to eat and stay near the airport",
        description="Local guide to San Isidro de Abona, Tenerife: things to do, where to eat, accommodation near Tenerife South airport and how to get here.",
        body="""<section class="hero">
  <div class="wrap">
    <h1>San Isidro de Abona, the most authentic south of Tenerife</h1>
    <p>A practical guide to the village and its surroundings: things to do, where to eat, where to stay near Tenerife South airport and how to get around.</p>
    <a class="btn" href="dormir-cerca-aeropuerto.html">Stay near the airport</a>
  </div>
</section>
<main>
  <div class="wrap">
    <h2 style="margin-top:0">What you will find here</h2>
    <div class="grid">
      <a class="card" href="que-hacer.html"><h3>Things to do</h3><p>Ideas and corners of the village and its surroundings.</p></a>
      <a class="card" href="comer.html"><h3>Where to eat</h3><p>Canarian cuisine and places in the area.</p></a>
      <a class="card" href="dormir-cerca-aeropuerto.html"><h3>Stay near the airport</h3><p>Handy if you arrive late or leave early.</p></a>
      <a class="card" href="como-llegar.html"><h3>Getting here and around</h3><p>Airport, motorway, bus and car rental.</p></a>
      <a class="card" href="comercios.html"><h3>Local businesses</h3><p>Local shops and services: support small, local trade.</p></a>
    </div>
    <h2>About San Isidro de Abona</h2>
    <p>San Isidro is a village in the south of Tenerife, in the Abona area, very close to Tenerife South airport and the island's main roads. It is a good starting point for discovering the south without the crowds of the most touristy areas.</p>
  </div>
</main>""",
    ),
    "de": dict(
        title="San Isidro de Abona: Aktivitäten, Essen und Übernachten am Flughafen",
        description="Lokaler Reiseführer für San Isidro de Abona, Teneriffa: Aktivitäten, Essen, Unterkunft in Flughafennähe (Teneriffa Süd) und Anreise.",
        body="""<section class="hero">
  <div class="wrap">
    <h1>San Isidro de Abona – der authentische Süden Teneriffas</h1>
    <p>Praktischer Reiseführer für das Dorf und seine Umgebung: Aktivitäten, Restaurants, Übernachten in der Nähe des Flughafens Teneriffa Süd und Mobilität.</p>
    <a class="btn" href="dormir-cerca-aeropuerto.html">Übernachten am Flughafen</a>
  </div>
</section>
<main>
  <div class="wrap">
    <h2 style="margin-top:0">Was dich hier erwartet</h2>
    <div class="grid">
      <a class="card" href="que-hacer.html"><h3>Aktivitäten</h3><p>Ideen und Ecken im Dorf und in der Umgebung.</p></a>
      <a class="card" href="comer.html"><h3>Essen</h3><p>Kanarische Küche und Lokale der Gegend.</p></a>
      <a class="card" href="dormir-cerca-aeropuerto.html"><h3>Übernachten am Flughafen</h3><p>Praktisch bei später Ankunft oder frühem Abflug.</p></a>
      <a class="card" href="como-llegar.html"><h3>Anreise und Mobilität</h3><p>Flughafen, Autobahn, Bus und Mietwagen.</p></a>
      <a class="card" href="comercios.html"><h3>Lokale Geschäfte</h3><p>Betriebe vor Ort: unterstütze den lokalen Handel.</p></a>
    </div>
    <h2>Über San Isidro de Abona</h2>
    <p>San Isidro ist ein Dorf im Süden Teneriffas, in der Region Abona, ganz in der Nähe des Flughafens Teneriffa Süd und der wichtigsten Straßen der Insel. Es ist ein guter Ausgangspunkt, um den Süden ohne den Trubel der touristischsten Gegenden kennenzulernen.</p>
  </div>
</main>""",
    ),
}

PAGES = {
    "que-hacer.html": {
        "es": dict(
            title="Qué hacer en San Isidro de Abona | San Isidro de Abona",
            description="Qué hacer en San Isidro de Abona, Tenerife: planes, paseos y excursiones cercanas en el sur de la isla.",
            h1="Qué hacer en San Isidro de Abona",
            lead="Un pueblo tranquilo del sur de Tenerife, bien situado para explorar la isla.",
            crumb="Qué hacer",
            content="""
      <h2>Pasear por el pueblo</h2>
      <p>San Isidro mantiene el ambiente de pueblo del sur: calles tranquilas, vida local y buena cocina canaria.</p>
      <!-- TODO: añadir lugares concretos (iglesia, plaza, miradores) con foto propia -->

      <h2>Fiestas</h2>
      <p>El pueblo celebra sus fiestas en honor a San Isidro Labrador.</p>
      <!-- TODO: confirmar fechas y programa actual con el ayuntamiento -->

      <h2>Excursiones desde aquí</h2>
      <p>Desde San Isidro se llega con facilidad a las playas del sur, al Teide y a otras zonas de la isla gracias a la autopista TF-1.</p>
      <!-- AFILIADO: excursiones desde el sur de Tenerife (sustituir href) -->
      <p><a class="btn" href="#" rel="sponsored nofollow">Ver excursiones en el sur de Tenerife</a></p>
      [[AFF]]
"""),
        "en": dict(
            title="Things to do in San Isidro de Abona | San Isidro de Abona",
            description="Things to do in San Isidro de Abona, Tenerife: ideas, walks and nearby trips in the south of the island.",
            h1="Things to do in San Isidro de Abona",
            lead="A quiet village in the south of Tenerife, well placed for exploring the island.",
            crumb="Things to do",
            content="""
      <h2>Stroll around the village</h2>
      <p>San Isidro keeps the feel of a southern village: quiet streets, local life and good Canarian food.</p>
      <!-- TODO: add specific places (church, square, viewpoints) with own photo -->

      <h2>Festivals</h2>
      <p>The village celebrates its festivities in honour of San Isidro Labrador (Saint Isidore the Farmer).</p>
      <!-- TODO: confirm current dates and programme with the town hall -->

      <h2>Trips from here</h2>
      <p>From San Isidro you can easily reach the southern beaches, Mount Teide and other parts of the island thanks to the TF-1 motorway.</p>
      <!-- AFFILIATE: tours from the south of Tenerife (replace href) -->
      <p><a class="btn" href="#" rel="sponsored nofollow">See tours in the south of Tenerife</a></p>
      [[AFF]]
"""),
        "de": dict(
            title="Aktivitäten in San Isidro de Abona | San Isidro de Abona",
            description="Aktivitäten in San Isidro de Abona, Teneriffa: Ideen, Spaziergänge und Ausflüge in der Nähe im Süden der Insel.",
            h1="Aktivitäten in San Isidro de Abona",
            lead="Ein ruhiges Dorf im Süden Teneriffas, gut gelegen, um die Insel zu erkunden.",
            crumb="Aktivitäten",
            content="""
      <h2>Spaziergang durchs Dorf</h2>
      <p>San Isidro hat sich das Flair eines Dorfes im Süden bewahrt: ruhige Gassen, lokales Leben und gute kanarische Küche.</p>
      <!-- TODO: konkrete Orte (Kirche, Platz, Aussichtspunkte) mit eigenem Foto ergänzen -->

      <h2>Feste</h2>
      <p>Das Dorf feiert seine Feste zu Ehren des heiligen Isidor, des Landmanns (San Isidro Labrador).</p>
      <!-- TODO: aktuelle Termine und Programm mit der Gemeinde bestätigen -->

      <h2>Ausflüge von hier aus</h2>
      <p>Von San Isidro aus erreichst du dank der Autobahn TF-1 leicht die Strände im Süden, den Teide und andere Teile der Insel.</p>
      <!-- AFFILIATE: Touren im Süden Teneriffas (href ersetzen) -->
      <p><a class="btn" href="#" rel="sponsored nofollow">Touren im Süden Teneriffas ansehen</a></p>
      [[AFF]]
"""),
    },
    "comer.html": {
        "es": dict(
            title="Dónde comer en San Isidro de Abona | San Isidro de Abona",
            description="Dónde comer en San Isidro de Abona, Tenerife: cocina canaria y restaurantes de la zona.",
            h1="Dónde comer en San Isidro de Abona",
            lead="Cocina canaria y sitios de la zona.",
            crumb="Dónde comer",
            content="""
      <h2>Qué probar</h2>
      <ul>
        <li><strong>Papas arrugadas con mojo.</strong></li>
        <li><strong>Queso asado.</strong></li>
        <li><strong>Carne de cabra y platos tradicionales.</strong></li>
      </ul>
      <!-- TODO: añadir 3-5 sitios reales visitados, con precio medio y reseña propia -->
      <div class="note"><strong>Importante:</strong> solo recomendamos sitios que hemos visitado. Esta sección se irá ampliando.</div>
"""),
        "en": dict(
            title="Where to eat in San Isidro de Abona | San Isidro de Abona",
            description="Where to eat in San Isidro de Abona, Tenerife: Canarian cuisine and restaurants in the area.",
            h1="Where to eat in San Isidro de Abona",
            lead="Canarian cuisine and places in the area.",
            crumb="Where to eat",
            content="""
      <h2>What to try</h2>
      <ul>
        <li><strong>Papas arrugadas with mojo</strong> (wrinkled potatoes with sauce).</li>
        <li><strong>Grilled cheese.</strong></li>
        <li><strong>Goat meat and traditional dishes.</strong></li>
      </ul>
      <!-- TODO: add 3-5 real places visited, with average price and own review -->
      <div class="note"><strong>Important:</strong> we only recommend places we have visited. This section will grow over time.</div>
"""),
        "de": dict(
            title="Essen gehen in San Isidro de Abona | San Isidro de Abona",
            description="Wo man in San Isidro de Abona, Teneriffa, essen kann: kanarische Küche und Restaurants der Gegend.",
            h1="Essen gehen in San Isidro de Abona",
            lead="Kanarische Küche und Lokale der Gegend.",
            crumb="Essen",
            content="""
      <h2>Was du probieren solltest</h2>
      <ul>
        <li><strong>Papas arrugadas mit Mojo</strong> (Runzelkartoffeln mit Sauce).</li>
        <li><strong>Gegrillter Käse.</strong></li>
        <li><strong>Ziegenfleisch und traditionelle Gerichte.</strong></li>
      </ul>
      <!-- TODO: 3-5 besuchte Lokale mit Durchschnittspreis und eigener Bewertung ergänzen -->
      <div class="note"><strong>Wichtig:</strong> Wir empfehlen nur Orte, die wir selbst besucht haben. Dieser Bereich wird nach und nach erweitert.</div>
"""),
    },
    "dormir-cerca-aeropuerto.html": {
        "es": dict(
            title="Dormir cerca del aeropuerto Tenerife Sur | San Isidro de Abona",
            description="Alojamiento cerca del aeropuerto Tenerife Sur: opciones en San Isidro de Abona para vuelos tempranos o llegadas tardías.",
            h1="Dormir cerca del aeropuerto Tenerife Sur",
            lead="Si llegas tarde o sales a primera hora, alojarte en San Isidro ahorra tiempo y estrés.",
            crumb="Dormir cerca del aeropuerto",
            content="""
      <h2>Por qué elegir esta zona</h2>
      <ul>
        <li>Muy cerca del aeropuerto Tenerife Sur (TFS).</li>
        <li>Acceso rápido a la autopista TF-1.</li>
        <li>Ambiente más tranquilo y normalmente más económico que las zonas turísticas de la costa.</li>
      </ul>
      <!-- AFILIADO: enlace Booking.com San Isidro / Granadilla de Abona (sustituir href) -->
      <p><a class="btn" href="#" rel="sponsored nofollow">Ver alojamientos cerca del aeropuerto</a></p>
      <!-- TODO: confirmar tiempos reales de trayecto y alojamientos concretos -->
      [[AFF]]
"""),
        "en": dict(
            title="Stay near Tenerife South airport | San Isidro de Abona",
            description="Accommodation near Tenerife South airport: options in San Isidro de Abona for early flights or late arrivals.",
            h1="Stay near Tenerife South airport",
            lead="If you arrive late or leave at first light, staying in San Isidro saves time and stress.",
            crumb="Stay near the airport",
            content="""
      <h2>Why choose this area</h2>
      <ul>
        <li>Very close to Tenerife South airport (TFS).</li>
        <li>Quick access to the TF-1 motorway.</li>
        <li>Quieter and usually cheaper than the touristy coastal areas.</li>
      </ul>
      <!-- AFFILIATE: Booking.com San Isidro / Granadilla de Abona link (replace href) -->
      <p><a class="btn" href="#" rel="sponsored nofollow">See accommodation near the airport</a></p>
      <!-- TODO: confirm real travel times and specific accommodation -->
      [[AFF]]
"""),
        "de": dict(
            title="Übernachten in der Nähe des Flughafens Teneriffa Süd | San Isidro de Abona",
            description="Unterkunft in der Nähe des Flughafens Teneriffa Süd: Optionen in San Isidro de Abona für frühe Flüge oder späte Ankünfte.",
            h1="Übernachten in der Nähe des Flughafens Teneriffa Süd",
            lead="Wenn du spät ankommst oder früh abfliegst, sparst du mit einer Unterkunft in San Isidro Zeit und Stress.",
            crumb="Übernachten am Flughafen",
            content="""
      <h2>Warum diese Gegend?</h2>
      <ul>
        <li>Sehr nah am Flughafen Teneriffa Süd (TFS).</li>
        <li>Schneller Zugang zur Autobahn TF-1.</li>
        <li>Ruhiger und meist günstiger als die touristischen Küstenorte.</li>
      </ul>
      <!-- AFFILIATE: Booking.com San Isidro / Granadilla de Abona (href ersetzen) -->
      <p><a class="btn" href="#" rel="sponsored nofollow">Unterkünfte in Flughafennähe ansehen</a></p>
      <!-- TODO: echte Fahrzeiten und konkrete Unterkünfte bestätigen -->
      [[AFF]]
"""),
    },
    "como-llegar.html": {
        "es": dict(
            title="Cómo llegar a San Isidro de Abona | San Isidro de Abona",
            description="Cómo llegar a San Isidro de Abona, Tenerife: desde el aeropuerto Tenerife Sur, en coche o en guagua.",
            h1="Cómo llegar y moverse",
            lead="San Isidro está en el sur de Tenerife, muy cerca del aeropuerto y de la autopista.",
            crumb="Cómo llegar",
            content="""
      <h2>Desde el aeropuerto Tenerife Sur</h2>
      <p>Es el aeropuerto más cercano y el trayecto es corto en coche.</p>
      <!-- TODO: confirmar minutos y distancia exactos -->

      <h2>En coche</h2>
      <p>La autopista TF-1 conecta la zona con el resto de la isla. Es la forma más cómoda de moverse.</p>

      <h2>En guagua</h2>
      <p>Hay conexiones de TITSA con otras zonas. Consulta horarios en su web, ya que cambian.</p>
"""),
        "en": dict(
            title="Getting to San Isidro de Abona | San Isidro de Abona",
            description="How to get to San Isidro de Abona, Tenerife: from Tenerife South airport, by car or by bus.",
            h1="Getting here and around",
            lead="San Isidro is in the south of Tenerife, very close to the airport and the motorway.",
            crumb="Getting here",
            content="""
      <h2>From Tenerife South airport</h2>
      <p>It is the nearest airport and the drive is short.</p>
      <!-- TODO: confirm exact minutes and distance -->

      <h2>By car</h2>
      <p>The TF-1 motorway links the area with the rest of the island. It is the most convenient way to get around.</p>

      <h2>By bus</h2>
      <p>There are TITSA bus connections (called "guagua" in the Canaries) to other areas. Check timetables on their website, as they change.</p>
"""),
        "de": dict(
            title="Anreise nach San Isidro de Abona | San Isidro de Abona",
            description="So kommst du nach San Isidro de Abona, Teneriffa: vom Flughafen Teneriffa Süd, mit dem Auto oder dem Bus.",
            h1="Anreise und Mobilität",
            lead="San Isidro liegt im Süden Teneriffas, ganz in der Nähe von Flughafen und Autobahn.",
            crumb="Anreise",
            content="""
      <h2>Vom Flughafen Teneriffa Süd</h2>
      <p>Es ist der nächstgelegene Flughafen und die Fahrt mit dem Auto ist kurz.</p>
      <!-- TODO: genaue Minuten und Entfernung bestätigen -->

      <h2>Mit dem Auto</h2>
      <p>Die Autobahn TF-1 verbindet die Gegend mit dem Rest der Insel. Sie ist die bequemste Art, unterwegs zu sein.</p>

      <h2>Mit dem Bus</h2>
      <p>Es gibt TITSA-Busverbindungen (auf den Kanaren „Guagua“ genannt) in andere Gebiete. Prüfe die Fahrpläne auf deren Website, da sie sich ändern.</p>
"""),
    },
}

if __name__ == "__main__":
    build(ROOT, dict(DOMAIN=DOMAIN, LOGO=LOGO, ZONA=ZONA, TAGLINE=TAGLINE, NAV=NAV, HOME=HOME,
                     PAGES=PAGES, COMERCIOS=COMERCIOS))
