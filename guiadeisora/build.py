#!/usr/bin/env python3
"""Genera guiadeisora.net en español (raíz), inglés (/en/) y alemán (/de/).

Uso:  python3 build.py
Edita el contenido aquí y vuelve a ejecutar. Sin dependencias.
La estructura y las páginas legales viven en ../tools/tourism_lib.py.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent / "tools"))
sys.path.insert(0, str(ROOT))
from tourism_lib import build  # noqa: E402
from comercios import COMERCIOS  # noqa: E402

DOMAIN = "guiadeisora.net"
LOGO = 'Guía de <span>Isora</span>'

ZONA = {"es": "Guía de Isora", "en": "Guía de Isora", "de": "Guía de Isora"}

TAGLINE = {
    "es": "Guía local de Guía de Isora, Tenerife",
    "en": "Local guide to Guía de Isora, Tenerife",
    "de": "Lokaler Reiseführer für Guía de Isora, Teneriffa",
}

NAV = {
    "es": [("index.html", "Inicio"), ("playas.html", "Playas"), ("excursiones.html", "Excursiones"),
           ("comer.html", "Dónde comer"), ("dormir.html", "Dónde dormir"), ("como-llegar.html", "Cómo llegar"), ("comercios.html", "Comercios")],
    "en": [("index.html", "Home"), ("playas.html", "Beaches"), ("excursiones.html", "Tours"),
           ("comer.html", "Where to eat"), ("dormir.html", "Where to stay"), ("como-llegar.html", "Getting here"), ("comercios.html", "Local businesses")],
    "de": [("index.html", "Startseite"), ("playas.html", "Strände"), ("excursiones.html", "Ausflüge"),
           ("comer.html", "Essen"), ("dormir.html", "Unterkunft"), ("como-llegar.html", "Anreise"), ("comercios.html", "Geschäfte")],
}

HOME = {
    "es": dict(
        title="Guía de Isora: playas, excursiones y dónde comer y dormir en Tenerife",
        description="Guía local de Guía de Isora, Tenerife: playas, excursiones, dónde comer, dónde dormir y cómo llegar.",
        body="""<section class="hero">
  <div class="wrap">
    <h1>Guía de Isora, el suroeste de Tenerife con calma</h1>
    <p>Playas, calas, excursiones, dónde comer y dónde dormir. Una guía local, práctica y sin prisas del municipio de Guía de Isora.</p>
    <a class="btn" href="playas.html">Descubre las playas</a>
  </div>
</section>
<main>
  <div class="wrap">
    <h2 style="margin-top:0">Qué encontrarás aquí</h2>
    <div class="grid">
      <a class="card" href="playas.html"><h3>Playas y calas</h3><p>San Juan, Alcalá, Abama y otros rincones de costa.</p></a>
      <a class="card" href="excursiones.html"><h3>Excursiones</h3><p>Avistamiento de cetáceos, rutas y salidas por la zona.</p></a>
      <a class="card" href="comer.html"><h3>Dónde comer</h3><p>Cocina canaria, pescado fresco y sitios con encanto.</p></a>
      <a class="card" href="dormir.html"><h3>Dónde dormir</h3><p>Qué zona elegir según el viaje que quieras hacer.</p></a>
      <a class="card" href="como-llegar.html"><h3>Cómo llegar y moverse</h3><p>Aeropuerto, coche, guagua y consejos prácticos.</p></a>
    </div>
    <h2>Sobre Guía de Isora</h2>
    <p>Guía de Isora es un municipio de la costa suroeste de Tenerife. Combina pueblos de medianías con núcleos costeros tranquilos como Playa San Juan y Alcalá, con muy buen clima durante casi todo el año y una ubicación cómoda para moverse hacia Los Gigantes, el Teide y el sur de la isla.</p>
    <p>Esta guía la escribimos desde Tenerife, para que organices tu visita con información clara y útil.</p>
  </div>
</main>""",
    ),
    "en": dict(
        title="Guía de Isora: beaches, tours, where to eat and stay in Tenerife",
        description="Local guide to Guía de Isora, Tenerife: beaches, tours, where to eat, where to stay and how to get here.",
        body="""<section class="hero">
  <div class="wrap">
    <h1>Guía de Isora, Tenerife's southwest at an easy pace</h1>
    <p>Beaches, coves, tours, where to eat and where to stay. A practical, unhurried local guide to the municipality of Guía de Isora.</p>
    <a class="btn" href="playas.html">Discover the beaches</a>
  </div>
</section>
<main>
  <div class="wrap">
    <h2 style="margin-top:0">What you will find here</h2>
    <div class="grid">
      <a class="card" href="playas.html"><h3>Beaches and coves</h3><p>San Juan, Alcalá, Abama and other corners of the coast.</p></a>
      <a class="card" href="excursiones.html"><h3>Tours</h3><p>Whale and dolphin watching, hikes and trips around the area.</p></a>
      <a class="card" href="comer.html"><h3>Where to eat</h3><p>Canarian cuisine, fresh fish and charming places.</p></a>
      <a class="card" href="dormir.html"><h3>Where to stay</h3><p>Which area to choose depending on the trip you want.</p></a>
      <a class="card" href="como-llegar.html"><h3>Getting here and around</h3><p>Airport, car, bus and practical tips.</p></a>
    </div>
    <h2>About Guía de Isora</h2>
    <p>Guía de Isora is a municipality on the southwest coast of Tenerife. It combines mid-altitude villages with quiet coastal spots such as Playa San Juan and Alcalá, enjoys great weather almost all year round and is a convenient base for Los Gigantes, Mount Teide and the south of the island.</p>
    <p>We write this guide from Tenerife, so you can plan your visit with clear and useful information.</p>
  </div>
</main>""",
    ),
    "de": dict(
        title="Guía de Isora: Strände, Ausflüge, Essen und Unterkunft auf Teneriffa",
        description="Lokaler Reiseführer für Guía de Isora, Teneriffa: Strände, Ausflüge, Essen, Unterkunft und Anreise.",
        body="""<section class="hero">
  <div class="wrap">
    <h1>Guía de Isora – der Südwesten Teneriffas in Ruhe entdecken</h1>
    <p>Strände, Buchten, Ausflüge, Restaurants und Unterkünfte. Ein praktischer, entspannter Reiseführer für die Gemeinde Guía de Isora.</p>
    <a class="btn" href="playas.html">Strände entdecken</a>
  </div>
</section>
<main>
  <div class="wrap">
    <h2 style="margin-top:0">Was dich hier erwartet</h2>
    <div class="grid">
      <a class="card" href="playas.html"><h3>Strände und Buchten</h3><p>San Juan, Alcalá, Abama und weitere Küstenorte.</p></a>
      <a class="card" href="excursiones.html"><h3>Ausflüge</h3><p>Wal- und Delfinbeobachtung, Wanderungen und Touren in der Umgebung.</p></a>
      <a class="card" href="comer.html"><h3>Essen</h3><p>Kanarische Küche, frischer Fisch und schöne Lokale.</p></a>
      <a class="card" href="dormir.html"><h3>Unterkunft</h3><p>Welche Gegend passt zu deiner Reise?</p></a>
      <a class="card" href="como-llegar.html"><h3>Anreise und Mobilität</h3><p>Flughafen, Auto, Bus und praktische Tipps.</p></a>
    </div>
    <h2>Über Guía de Isora</h2>
    <p>Guía de Isora ist eine Gemeinde an der Südwestküste Teneriffas. Sie verbindet Dörfer in mittlerer Höhenlage mit ruhigen Küstenorten wie Playa San Juan und Alcalá, hat fast das ganze Jahr über ein angenehmes Klima und ist ein praktischer Ausgangspunkt für Los Gigantes, den Teide und den Süden der Insel.</p>
    <p>Wir schreiben diesen Reiseführer auf Teneriffa, damit du deinen Besuch mit klaren und nützlichen Informationen planen kannst.</p>
  </div>
</main>""",
    ),
}

PAGES = {
    "playas.html": {
        "es": dict(
            title="Playas y calas de Guía de Isora | Guía de Isora",
            description="Guía de las playas y calas de Guía de Isora, Tenerife: Playa San Juan, Alcalá, Abama y consejos para ir.",
            h1="Playas y calas de Guía de Isora",
            lead="La costa del municipio es de piedra volcánica, con pequeñas playas, charcos y puertos de pescadores.",
            crumb="Playas",
            content="""
      <h2>Playa San Juan</h2>
      <p>Pueblo pesquero con su puerto, paseo marítimo y una buena oferta de restaurantes. Es un buen punto de partida si buscas ambiente local y servicios cerca del mar.</p>
      <!-- TODO: añadir tipo de arena, accesos, aparcamiento, foto propia -->

      <h2>Alcalá</h2>
      <p>Núcleo costero pequeño y tranquilo, conocido por sus zonas de baño entre rocas. Ideal para quien prefiere un ambiente más sosegado.</p>
      <!-- TODO: añadir zonas de baño recomendadas, seguridad y mareas, foto propia -->

      <h2>Playa de Abama</h2>
      <p>Playa de la zona de Abama, en la costa del municipio. Consulta antes de ir el estado del acceso y las condiciones del mar.</p>
      <!-- TODO: confirmar acceso público actual y servicios -->

      <div class="note"><strong>Consejo:</strong> el Atlántico en esta costa puede tener oleaje y corrientes. Mira siempre las banderas y el parte del mar antes de bañarte.</div>
"""),
        "en": dict(
            title="Beaches and coves in Guía de Isora | Guía de Isora",
            description="Guide to the beaches and coves of Guía de Isora, Tenerife: Playa San Juan, Alcalá, Abama and tips before you go.",
            h1="Beaches and coves in Guía de Isora",
            lead="The municipality's coastline is volcanic rock, with small beaches, natural pools and fishing harbours.",
            crumb="Beaches",
            content="""
      <h2>Playa San Juan</h2>
      <p>A fishing village with its harbour, seafront promenade and a good choice of restaurants. A great starting point if you want local atmosphere and services close to the sea.</p>
      <!-- TODO: add sand type, access, parking, own photo -->

      <h2>Alcalá</h2>
      <p>A small, quiet coastal village known for its bathing spots among the rocks. Ideal if you prefer a calmer atmosphere.</p>
      <!-- TODO: add recommended bathing spots, safety and tides, own photo -->

      <h2>Playa de Abama</h2>
      <p>A beach in the Abama area on the municipality's coast. Check the state of access and the sea conditions before you go.</p>
      <!-- TODO: confirm current public access and facilities -->

      <div class="note"><strong>Tip:</strong> the Atlantic on this coast can have swell and currents. Always check the flags and the sea forecast before swimming.</div>
"""),
        "de": dict(
            title="Strände und Buchten in Guía de Isora | Guía de Isora",
            description="Übersicht der Strände und Buchten in Guía de Isora, Teneriffa: Playa San Juan, Alcalá, Abama und Tipps für den Besuch.",
            h1="Strände und Buchten in Guía de Isora",
            lead="Die Küste der Gemeinde besteht aus Vulkangestein, mit kleinen Stränden, Naturbecken und Fischerhäfen.",
            crumb="Strände",
            content="""
      <h2>Playa San Juan</h2>
      <p>Ein Fischerdorf mit Hafen, Uferpromenade und einer guten Auswahl an Restaurants. Ein idealer Ausgangspunkt, wenn du lokales Flair und Service in Meeresnähe suchst.</p>
      <!-- TODO: Sandart, Zugang, Parkplätze, eigenes Foto ergänzen -->

      <h2>Alcalá</h2>
      <p>Ein kleiner, ruhiger Küstenort, bekannt für seine Badestellen zwischen den Felsen. Ideal für alle, die es gelassener mögen.</p>
      <!-- TODO: empfohlene Badestellen, Sicherheit und Gezeiten, eigenes Foto ergänzen -->

      <h2>Playa de Abama</h2>
      <p>Ein Strand im Gebiet von Abama an der Küste der Gemeinde. Informiere dich vor dem Besuch über den Zugang und die Meeresbedingungen.</p>
      <!-- TODO: aktuellen öffentlichen Zugang und Ausstattung bestätigen -->

      <div class="note"><strong>Tipp:</strong> Der Atlantik kann an dieser Küste Wellengang und Strömungen haben. Beachte vor dem Baden immer die Flaggen und den Wellenbericht.</div>
"""),
    },
    "excursiones.html": {
        "es": dict(
            title="Excursiones y actividades cerca de Guía de Isora | Guía de Isora",
            description="Excursiones desde Guía de Isora, Tenerife: avistamiento de cetáceos, rutas de senderismo y salidas al Teide y a Los Gigantes.",
            h1="Excursiones y actividades",
            lead="Guía de Isora está bien situada para moverse por el oeste y el sur de Tenerife.",
            crumb="Excursiones",
            content="""
      <h2>Avistamiento de cetáceos</h2>
      <p>La costa suroeste de Tenerife es una de las zonas más conocidas de España para ver delfines y calderones. Hay salidas en barco desde puertos cercanos; elige operadores con certificación de turismo responsable.</p>
      <!-- AFILIADO: enlace GetYourGuide / Civitatis avistamiento de cetáceos (sustituir href) -->
      <p><a class="btn" href="#" rel="sponsored nofollow">Ver excursiones de avistamiento</a></p>

      <h2>Los Gigantes y los acantilados</h2>
      <p>A poca distancia en coche se encuentran los acantilados de Los Gigantes, con miradores y excursiones en barco.</p>

      <h2>Teide</h2>
      <p>Desde la zona puedes organizar una jornada al Parque Nacional del Teide. Recuerda que para subir a la cima por encima del refugio se necesita permiso.</p>

      <h2>Senderismo por las medianías</h2>
      <p>Los caminos de las medianías del municipio ofrecen paisajes distintos al de la costa. Pendiente de añadir rutas concretas con distancia y dificultad.</p>
      <!-- TODO: añadir 2-3 rutas con mapa (wikiloc o gpx propio) -->
      [[AFF]]
"""),
        "en": dict(
            title="Tours and activities near Guía de Isora | Guía de Isora",
            description="Tours from Guía de Isora, Tenerife: whale and dolphin watching, hiking routes and trips to Mount Teide and Los Gigantes.",
            h1="Tours and activities",
            lead="Guía de Isora is well placed for exploring the west and south of Tenerife.",
            crumb="Tours",
            content="""
      <h2>Whale and dolphin watching</h2>
      <p>Tenerife's southwest coast is one of the best-known areas in Spain for spotting dolphins and pilot whales. Boat trips leave from nearby harbours; choose operators with a responsible-tourism certification.</p>
      <!-- AFFILIATE: GetYourGuide / Civitatis whale watching link (replace href) -->
      <p><a class="btn" href="#" rel="sponsored nofollow">See whale-watching tours</a></p>

      <h2>Los Gigantes and the cliffs</h2>
      <p>A short drive away you will find the Los Gigantes cliffs, with viewpoints and boat trips.</p>

      <h2>Mount Teide</h2>
      <p>From here you can organise a day trip to Teide National Park. Remember that a permit is required to climb to the summit beyond the refuge.</p>

      <h2>Hiking in the mid-altitude villages</h2>
      <p>The paths through the municipality's mid-altitude villages offer very different scenery from the coast. Specific routes with distance and difficulty are still to be added.</p>
      <!-- TODO: add 2-3 routes with a map (Wikiloc or own GPX) -->
      [[AFF]]
"""),
        "de": dict(
            title="Ausflüge und Aktivitäten rund um Guía de Isora | Guía de Isora",
            description="Ausflüge ab Guía de Isora, Teneriffa: Wal- und Delfinbeobachtung, Wanderungen sowie Touren zum Teide und nach Los Gigantes.",
            h1="Ausflüge und Aktivitäten",
            lead="Guía de Isora liegt günstig, um den Westen und Süden Teneriffas zu erkunden.",
            crumb="Ausflüge",
            content="""
      <h2>Wal- und Delfinbeobachtung</h2>
      <p>Die Südwestküste Teneriffas gehört zu den bekanntesten Gebieten Spaniens, um Delfine und Grindwale zu beobachten. Bootsausflüge starten von nahegelegenen Häfen; wähle Anbieter mit Zertifikat für verantwortungsvollen Tourismus.</p>
      <!-- AFFILIATE: GetYourGuide / Civitatis Walbeobachtung (href ersetzen) -->
      <p><a class="btn" href="#" rel="sponsored nofollow">Touren zur Walbeobachtung ansehen</a></p>

      <h2>Los Gigantes und die Steilklippen</h2>
      <p>Nur eine kurze Autofahrt entfernt liegen die Steilklippen von Los Gigantes mit Aussichtspunkten und Bootsausflügen.</p>

      <h2>Teide</h2>
      <p>Von hier aus lässt sich ein Tagesausflug in den Teide-Nationalpark organisieren. Beachte: Für den Aufstieg zum Gipfel oberhalb der Schutzhütte ist eine Genehmigung erforderlich.</p>

      <h2>Wandern in den Mittellagen</h2>
      <p>Die Wege durch die Dörfer in mittlerer Höhenlage bieten ganz andere Landschaften als die Küste. Konkrete Routen mit Entfernung und Schwierigkeit folgen noch.</p>
      <!-- TODO: 2-3 Routen mit Karte ergänzen (Wikiloc oder eigene GPX) -->
      [[AFF]]
"""),
    },
    "comer.html": {
        "es": dict(
            title="Dónde comer en Guía de Isora | Guía de Isora",
            description="Dónde comer en Guía de Isora, Tenerife: cocina canaria, pescado fresco y restaurantes de la costa y las medianías.",
            h1="Dónde comer en Guía de Isora",
            lead="Cocina canaria, pescado del día y sitios tranquilos con vistas al mar.",
            crumb="Dónde comer",
            content="""
      <h2>Qué probar</h2>
      <ul>
        <li><strong>Papas arrugadas con mojo</strong> (rojo y verde).</li>
        <li><strong>Pescado fresco</strong> del día, sobre todo en la costa.</li>
        <li><strong>Queso asado con mojo.</strong></li>
        <li><strong>Carne de cabra</strong> y platos de las medianías.</li>
      </ul>

      <h2>Playa San Juan</h2>
      <p>Zona con varios restaurantes junto al puerto, especializada en pescado y marisco.</p>
      <!-- TODO: añadir 3-5 sitios reales con nombre, precio medio, y reseña propia -->

      <h2>Medianías y pueblos</h2>
      <p>En los pueblos del interior encontrarás cocina tradicional a precios más ajustados.</p>
      <!-- TODO: añadir sitios reales -->

      <div class="note"><strong>Importante:</strong> sólo recomendamos sitios que hemos visitado. Esta sección se irá ampliando con reseñas propias.</div>
"""),
        "en": dict(
            title="Where to eat in Guía de Isora | Guía de Isora",
            description="Where to eat in Guía de Isora, Tenerife: Canarian cuisine, fresh fish and restaurants on the coast and in the mid-altitude villages.",
            h1="Where to eat in Guía de Isora",
            lead="Canarian cuisine, catch of the day and quiet places with sea views.",
            crumb="Where to eat",
            content="""
      <h2>What to try</h2>
      <ul>
        <li><strong>Papas arrugadas with mojo</strong> (wrinkled potatoes with red and green sauce).</li>
        <li><strong>Fresh fish</strong> of the day, especially on the coast.</li>
        <li><strong>Grilled cheese with mojo.</strong></li>
        <li><strong>Goat meat</strong> and traditional dishes from the mid-altitude villages.</li>
      </ul>

      <h2>Playa San Juan</h2>
      <p>An area with several restaurants by the harbour, specialising in fish and seafood.</p>
      <!-- TODO: add 3-5 real places with name, average price and own review -->

      <h2>Inland villages</h2>
      <p>In the inland villages you will find traditional cooking at more moderate prices.</p>
      <!-- TODO: add real places -->

      <div class="note"><strong>Important:</strong> we only recommend places we have visited. This section will grow with our own reviews.</div>
"""),
        "de": dict(
            title="Essen gehen in Guía de Isora | Guía de Isora",
            description="Wo man in Guía de Isora, Teneriffa, gut essen kann: kanarische Küche, frischer Fisch und Restaurants an der Küste und im Landesinneren.",
            h1="Essen gehen in Guía de Isora",
            lead="Kanarische Küche, Fisch des Tages und ruhige Lokale mit Meerblick.",
            crumb="Essen",
            content="""
      <h2>Was du probieren solltest</h2>
      <ul>
        <li><strong>Papas arrugadas mit Mojo</strong> (Runzelkartoffeln mit roter und grüner Sauce).</li>
        <li><strong>Frischer Fisch</strong> des Tages, vor allem an der Küste.</li>
        <li><strong>Gegrillter Käse mit Mojo.</strong></li>
        <li><strong>Ziegenfleisch</strong> und traditionelle Gerichte aus den Dörfern im Landesinneren.</li>
      </ul>

      <h2>Playa San Juan</h2>
      <p>Ein Bereich mit mehreren Restaurants am Hafen, spezialisiert auf Fisch und Meeresfrüchte.</p>
      <!-- TODO: 3-5 echte Lokale mit Name, Durchschnittspreis und eigener Bewertung ergänzen -->

      <h2>Dörfer im Landesinneren</h2>
      <p>In den Dörfern im Landesinneren findest du traditionelle Küche zu günstigeren Preisen.</p>
      <!-- TODO: echte Lokale ergänzen -->

      <div class="note"><strong>Wichtig:</strong> Wir empfehlen nur Orte, die wir selbst besucht haben. Dieser Bereich wird mit eigenen Bewertungen erweitert.</div>
"""),
    },
    "dormir.html": {
        "es": dict(
            title="Dónde dormir en Guía de Isora | Guía de Isora",
            description="Qué zona elegir para alojarte en Guía de Isora, Tenerife: costa, medianías, apartamentos, hoteles y casas rurales.",
            h1="Dónde dormir en Guía de Isora",
            lead="Qué zona elegir según el tipo de viaje que quieras hacer.",
            crumb="Dónde dormir",
            content="""
      <h2>Costa: Playa San Juan y Alcalá</h2>
      <p>Para estar cerca del mar, de los restaurantes y de los puertos. Muchos apartamentos y alojamientos vacacionales.</p>

      <h2>Zona de Abama</h2>
      <p>Complejos turísticos y alojamiento de categoría alta.</p>

      <h2>Medianías</h2>
      <p>Para un viaje más tranquilo y rural, con casas rurales y vistas.</p>

      <!-- AFILIADO: enlace Booking.com Guía de Isora (sustituir href) -->
      <p><a class="btn" href="#" rel="sponsored nofollow">Ver alojamientos en Guía de Isora</a></p>
      [[AFF]]
"""),
        "en": dict(
            title="Where to stay in Guía de Isora | Guía de Isora",
            description="Which area to choose when staying in Guía de Isora, Tenerife: coast, mid-altitude villages, apartments, hotels and country houses.",
            h1="Where to stay in Guía de Isora",
            lead="Which area to choose depending on the kind of trip you want.",
            crumb="Where to stay",
            content="""
      <h2>Coast: Playa San Juan and Alcalá</h2>
      <p>To be close to the sea, restaurants and harbours. Plenty of apartments and holiday rentals.</p>

      <h2>Abama area</h2>
      <p>Resorts and high-end accommodation.</p>

      <h2>Mid-altitude villages</h2>
      <p>For a quieter, more rural trip, with country houses and views.</p>

      <!-- AFFILIATE: Booking.com Guía de Isora link (replace href) -->
      <p><a class="btn" href="#" rel="sponsored nofollow">See accommodation in Guía de Isora</a></p>
      [[AFF]]
"""),
        "de": dict(
            title="Unterkunft in Guía de Isora | Guía de Isora",
            description="Welche Gegend für deine Unterkunft in Guía de Isora, Teneriffa, passt: Küste, Mittellagen, Apartments, Hotels und Landhäuser.",
            h1="Unterkunft in Guía de Isora",
            lead="Welche Gegend zu welcher Art von Reise passt.",
            crumb="Unterkunft",
            content="""
      <h2>Küste: Playa San Juan und Alcalá</h2>
      <p>Um nah am Meer, an Restaurants und Häfen zu sein. Viele Apartments und Ferienunterkünfte.</p>

      <h2>Gebiet Abama</h2>
      <p>Resorts und Unterkünfte der gehobenen Kategorie.</p>

      <h2>Mittellagen</h2>
      <p>Für eine ruhigere, ländlichere Reise mit Landhäusern und Aussicht.</p>

      <!-- AFFILIATE: Booking.com Guía de Isora (href ersetzen) -->
      <p><a class="btn" href="#" rel="sponsored nofollow">Unterkünfte in Guía de Isora ansehen</a></p>
      [[AFF]]
"""),
    },
    "como-llegar.html": {
        "es": dict(
            title="Cómo llegar a Guía de Isora y moverse | Guía de Isora",
            description="Cómo llegar a Guía de Isora, Tenerife: desde el aeropuerto Tenerife Sur, en coche o en guagua, y consejos para moverse.",
            h1="Cómo llegar y moverse",
            lead="Guía de Isora está en la costa suroeste de Tenerife, bien conectada por carretera.",
            crumb="Cómo llegar",
            content="""
      <h2>Desde el aeropuerto</h2>
      <p>El aeropuerto más cercano es el de <strong>Tenerife Sur (TFS)</strong>, a unos 30-40 minutos en coche. Desde Tenerife Norte el trayecto es bastante más largo.</p>

      <h2>En coche</h2>
      <p>Es la opción más cómoda para moverse entre playas, miradores y pueblos. Reserva con antelación en temporada alta.</p>

      <h2>En guagua</h2>
      <p>Hay conexiones de guagua (TITSA) con otras zonas de la isla. Consulta horarios y líneas en su web antes de viajar, ya que cambian.</p>

      <div class="note"><strong>Consejo:</strong> las carreteras de la zona tienen curvas y desniveles; calcula siempre más tiempo del que marca el GPS.</div>
"""),
        "en": dict(
            title="Getting to and around Guía de Isora | Guía de Isora",
            description="How to get to Guía de Isora, Tenerife: from Tenerife South airport, by car or by bus, plus tips for getting around.",
            h1="Getting here and around",
            lead="Guía de Isora is on Tenerife's southwest coast, well connected by road.",
            crumb="Getting here",
            content="""
      <h2>From the airport</h2>
      <p>The nearest airport is <strong>Tenerife South (TFS)</strong>, about 30-40 minutes by car. From Tenerife North the journey is considerably longer.</p>

      <h2>By car</h2>
      <p>This is the most convenient way to move between beaches, viewpoints and villages. Book ahead in high season.</p>

      <h2>By bus</h2>
      <p>There are bus connections (called "guagua" in the Canaries, operated by TITSA) to other parts of the island. Check timetables and routes on their website before travelling, as they change.</p>

      <div class="note"><strong>Tip:</strong> roads in the area are winding and hilly; always allow more time than your GPS says.</div>
"""),
        "de": dict(
            title="Anreise nach Guía de Isora und Mobilität | Guía de Isora",
            description="So kommst du nach Guía de Isora, Teneriffa: vom Flughafen Teneriffa Süd, mit dem Auto oder dem Bus, plus Tipps zur Fortbewegung.",
            h1="Anreise und Mobilität",
            lead="Guía de Isora liegt an der Südwestküste Teneriffas und ist gut per Straße angebunden.",
            crumb="Anreise",
            content="""
      <h2>Vom Flughafen</h2>
      <p>Der nächstgelegene Flughafen ist <strong>Teneriffa Süd (TFS)</strong>, etwa 30-40 Minuten mit dem Auto. Von Teneriffa Nord aus dauert die Fahrt deutlich länger.</p>

      <h2>Mit dem Auto</h2>
      <p>Das ist die bequemste Möglichkeit, zwischen Stränden, Aussichtspunkten und Dörfern unterwegs zu sein. In der Hochsaison rechtzeitig reservieren.</p>

      <h2>Mit dem Bus</h2>
      <p>Es gibt Busverbindungen (auf den Kanaren „Guagua“ genannt, Betreiber TITSA) in andere Teile der Insel. Prüfe Fahrpläne und Linien vor der Reise auf deren Website, da sie sich ändern.</p>

      <div class="note"><strong>Tipp:</strong> Die Straßen in der Gegend sind kurvig und hügelig; plane immer mehr Zeit ein, als das Navi anzeigt.</div>
"""),
    },
}

if __name__ == "__main__":
    build(ROOT, dict(DOMAIN=DOMAIN, LOGO=LOGO, ZONA=ZONA, TAGLINE=TAGLINE, NAV=NAV, HOME=HOME,
                     PAGES=PAGES, COMERCIOS=COMERCIOS))
