#!/usr/bin/env python3
"""Genera las páginas HTML de guiadeisora.net.

Uso:  python3 build.py
Edita el contenido en PAGES y vuelve a ejecutar. No necesita dependencias.
"""
from pathlib import Path

SITE = "https://guiadeisora.net"
ROOT = Path(__file__).parent

NAV = [
    ("index.html", "Inicio"),
    ("playas.html", "Playas"),
    ("excursiones.html", "Excursiones"),
    ("comer.html", "Dónde comer"),
    ("dormir.html", "Dónde dormir"),
    ("como-llegar.html", "Cómo llegar"),
]

LAYOUT = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{site}/{file}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{site}/{file}">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<header class="site">
  <div class="wrap">
    <a class="logo" href="index.html">Guía de <span>Isora</span></a>
    <nav class="main" aria-label="Principal">
{nav}
    </nav>
  </div>
</header>
{body}
<footer class="site">
  <div class="wrap">
    <div>© {year} guiadeisora.net · Guía local de Guía de Isora, Tenerife</div>
    <div><a href="aviso-legal.html">Aviso legal</a> · <a href="privacidad.html">Privacidad</a> · <a href="afiliados.html">Enlaces de afiliado</a></div>
  </div>
</footer>
</body>
</html>
"""

AFFILIATE_NOTE = (
    '<p class="affiliate">Algunos enlaces de esta página son de afiliado: si reservas '
    'a través de ellos, la web recibe una pequeña comisión sin coste extra para ti. '
    '<a href="afiliados.html">Más información</a>.</p>'
)


def nav_html(current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'      <a href="{href}"{cur}>{label}</a>')
    return "\n".join(items)


def page(file, title, description, body, year=2026):
    html = LAYOUT.format(
        title=title, description=description, file=file, site=SITE,
        nav=nav_html(file), body=body, year=year,
    )
    (ROOT / file).write_text(html, encoding="utf-8")


def article(h1, lead, content, crumb):
    return f"""<main>
  <div class="wrap">
    <article>
      <div class="breadcrumbs"><a href="index.html">Inicio</a> › {crumb}</div>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
{content}
    </article>
  </div>
</main>"""


# --------------------------------------------------------------------------
# Inicio
# --------------------------------------------------------------------------
HOME = """<section class="hero">
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
</main>"""

# --------------------------------------------------------------------------
# Páginas de contenido
# --------------------------------------------------------------------------
PAGES = {
    "playas.html": dict(
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
""",
    ),
    "excursiones.html": dict(
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
""" + "      " + AFFILIATE_NOTE,
    ),
    "comer.html": dict(
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
""",
    ),
    "dormir.html": dict(
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
""" + "      " + AFFILIATE_NOTE,
    ),
    "como-llegar.html": dict(
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
""",
    ),
    "afiliados.html": dict(
        title="Enlaces de afiliado | Guía de Isora",
        description="Información sobre los enlaces de afiliado de guiadeisora.net.",
        h1="Enlaces de afiliado",
        lead="Cómo se financia esta web.",
        crumb="Enlaces de afiliado",
        content="""
      <p>Algunos enlaces de guiadeisora.net son de afiliado. Si reservas una excursión o un alojamiento a través de ellos, la web puede recibir una comisión, <strong>sin ningún coste adicional para ti</strong>.</p>
      <p>Esa comisión nos ayuda a mantener la web. Nuestras recomendaciones no dependen de ella: sólo recomendamos lo que consideramos útil para quien visita Guía de Isora.</p>
""",
    ),
    "aviso-legal.html": dict(
        title="Aviso legal | Guía de Isora",
        description="Aviso legal de guiadeisora.net.",
        h1="Aviso legal",
        lead="Información del titular del sitio web (LSSI-CE).",
        crumb="Aviso legal",
        content="""
      <!-- TODO OBLIGATORIO: rellenar con los datos reales del titular antes de publicar -->
      <p><strong>Titular:</strong> [NOMBRE Y APELLIDOS O RAZÓN SOCIAL]</p>
      <p><strong>NIF/CIF:</strong> [NIF]</p>
      <p><strong>Domicilio:</strong> [DIRECCIÓN]</p>
      <p><strong>Correo de contacto:</strong> [EMAIL]</p>
      <p><strong>Sitio web:</strong> guiadeisora.net</p>
      <p>Los contenidos de esta web tienen carácter informativo. Aunque procuramos que la información sea correcta, no garantizamos que esté siempre actualizada.</p>
""",
    ),
    "privacidad.html": dict(
        title="Política de privacidad | Guía de Isora",
        description="Política de privacidad de guiadeisora.net.",
        h1="Política de privacidad",
        lead="Qué datos tratamos y para qué.",
        crumb="Privacidad",
        content="""
      <!-- TODO: revisar según las herramientas finales (analítica, cookies, formularios) -->
      <p>Esta web no recoge datos personales mediante formularios. Si en el futuro se añade analítica, un formulario de contacto o publicidad, esta política se actualizará.</p>
      <p>Los enlaces de afiliado llevan a sitios de terceros (por ejemplo, plataformas de reservas) que tienen su propia política de privacidad.</p>
      <p><strong>Responsable:</strong> [NOMBRE] · <strong>Contacto:</strong> [EMAIL]</p>
""",
    ),
}


def main():
    page(
        "index.html",
        "Guía de Isora: playas, excursiones y dónde comer y dormir en Tenerife",
        "Guía local de Guía de Isora, Tenerife: playas, excursiones, dónde comer, dónde dormir y cómo llegar.",
        HOME,
    )
    for file, p in PAGES.items():
        page(file, p["title"], p["description"], article(p["h1"], p["lead"], p["content"], p["crumb"]))

    urls = ["index.html"] + list(PAGES)
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{SITE}/{u}</loc></url>" for u in urls]
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    (ROOT / "CNAME").write_text("guiadeisora.net\n", encoding="utf-8")
    print(f"Generadas {len(urls)} páginas.")


if __name__ == "__main__":
    main()
