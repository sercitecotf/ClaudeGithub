#!/usr/bin/env python3
"""Genera las páginas HTML de sanisidrodeabona.com.

Uso:  python3 build.py
Edita el contenido en PAGES y vuelve a ejecutar. No necesita dependencias.
"""
from pathlib import Path

SITE = "https://sanisidrodeabona.com"
ROOT = Path(__file__).parent

NAV = [
    ("index.html", "Inicio"),
    ("que-hacer.html", "Qué hacer"),
    ("comer.html", "Dónde comer"),
    ("dormir-cerca-aeropuerto.html", "Dormir cerca del aeropuerto"),
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
    <a class="logo" href="index.html">San Isidro <span>de Abona</span></a>
    <nav class="main" aria-label="Principal">
{nav}
    </nav>
  </div>
</header>
{body}
<footer class="site">
  <div class="wrap">
    <div>© {year} sanisidrodeabona.com · Guía local de San Isidro de Abona, Tenerife</div>
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
    </div>

    <h2>Sobre San Isidro de Abona</h2>
    <p>San Isidro es un pueblo del sur de Tenerife, en la comarca de Abona, muy cerca del aeropuerto Tenerife Sur y de las principales vías de la isla. Es un buen punto de partida para conocer el sur sin las aglomeraciones de las zonas más turísticas.</p>
  </div>
</main>"""

PAGES = {
    "que-hacer.html": dict(
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
""" + "      " + AFFILIATE_NOTE,
    ),
    "comer.html": dict(
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
""",
    ),
    "dormir-cerca-aeropuerto.html": dict(
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
""" + "      " + AFFILIATE_NOTE,
    ),
    "como-llegar.html": dict(
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
""",
    ),
    "afiliados.html": dict(
        title="Enlaces de afiliado | San Isidro de Abona",
        description="Información sobre los enlaces de afiliado de sanisidrodeabona.com.",
        h1="Enlaces de afiliado",
        lead="Cómo se financia esta web.",
        crumb="Enlaces de afiliado",
        content="""
      <p>Algunos enlaces de sanisidrodeabona.com son de afiliado. Si reservas a través de ellos, la web puede recibir una comisión, <strong>sin coste adicional para ti</strong>.</p>
""",
    ),
    "aviso-legal.html": dict(
        title="Aviso legal | San Isidro de Abona",
        description="Aviso legal de sanisidrodeabona.com.",
        h1="Aviso legal",
        lead="Información del titular del sitio web (LSSI-CE).",
        crumb="Aviso legal",
        content="""
      <!-- TODO OBLIGATORIO: rellenar con los datos reales del titular antes de publicar -->
      <p><strong>Titular:</strong> [NOMBRE Y APELLIDOS O RAZÓN SOCIAL]</p>
      <p><strong>NIF/CIF:</strong> [NIF]</p>
      <p><strong>Domicilio:</strong> [DIRECCIÓN]</p>
      <p><strong>Correo de contacto:</strong> [EMAIL]</p>
      <p><strong>Sitio web:</strong> sanisidrodeabona.com</p>
""",
    ),
    "privacidad.html": dict(
        title="Política de privacidad | San Isidro de Abona",
        description="Política de privacidad de sanisidrodeabona.com.",
        h1="Política de privacidad",
        lead="Qué datos tratamos y para qué.",
        crumb="Privacidad",
        content="""
      <!-- TODO: revisar según analítica/cookies que se usen -->
      <p>Esta web no recoge datos personales mediante formularios. Si se añade analítica, contacto o publicidad, esta política se actualizará.</p>
      <p><strong>Responsable:</strong> [NOMBRE] · <strong>Contacto:</strong> [EMAIL]</p>
""",
    ),
}


def main():
    page(
        "index.html",
        "San Isidro de Abona: qué hacer, dónde comer y dormir cerca del aeropuerto",
        "Guía local de San Isidro de Abona, Tenerife: qué hacer, dónde comer, alojamiento cerca del aeropuerto Tenerife Sur y cómo llegar.",
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
    (ROOT / "CNAME").write_text("sanisidrodeabona.com\n", encoding="utf-8")
    print(f"Generadas {len(urls)} páginas.")


if __name__ == "__main__":
    main()
