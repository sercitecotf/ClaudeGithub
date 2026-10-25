#!/usr/bin/env python3
"""Genera las páginas HTML de imosinformatica.com.

Uso:  python3 build.py
Edita el contenido en ARTICLES y vuelve a ejecutar. No necesita dependencias.
"""
from pathlib import Path

SITE = "https://imosinformatica.com"
ROOT = Path(__file__).parent
UPDATED = "octubre de 2026"

NAV = [
    ("index.html", "Inicio"),
    ("b850-vs-a620.html", "B850 vs A620"),
    ("ddr5-para-ryzen-9000.html", "Qué DDR5"),
    ("pc-ryzen-9-9900x.html", "PC con 9900X"),
    ("comprar-informatica-canarias.html", "Comprar en Canarias"),
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
    <a class="logo" href="index.html">Imos<span>Informática</span></a>
    <nav class="main" aria-label="Principal">
{nav}
    </nav>
  </div>
</header>
{body}
<footer class="site">
  <div class="wrap">
    <div>© 2026 imosinformatica.com · Comparativas y guías de hardware</div>
    <div><a href="aviso-legal.html">Aviso legal</a> · <a href="privacidad.html">Privacidad</a> · <a href="afiliados.html">Enlaces de afiliado</a></div>
  </div>
</footer>
</body>
</html>
"""

AFFILIATE_NOTE = (
    '<p class="affiliate">Algunos enlaces son de afiliado: si compras a través de ellos, la web '
    'recibe una pequeña comisión sin coste extra para ti. <a href="afiliados.html">Más información</a>. '
    'Los precios son orientativos (' + UPDATED + ') y cambian a menudo: compruébalos en la tienda.</p>'
)


def nav_html(current):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        out.append(f'      <a href="{href}"{cur}>{label}</a>')
    return "\n".join(out)


def write(file, title, description, body):
    html = LAYOUT.format(title=title, description=description, file=file,
                         site=SITE, nav=nav_html(file), body=body)
    (ROOT / file).write_text(html, encoding="utf-8")


def article(h1, lead, content, crumb):
    return f"""<main>
  <div class="wrap">
    <article>
      <div class="breadcrumbs"><a href="index.html">Inicio</a> › {crumb}</div>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
{content}
      {AFFILIATE_NOTE}
    </article>
  </div>
</main>"""


HOME = """<section class="hero">
  <div class="wrap">
    <h1>Elige bien tu PC: comparativas claras de componentes</h1>
    <p>Guías y comparativas de procesadores, placas base y memoria, con precios reales y consejos para comprar desde Canarias.</p>
    <a class="btn" href="pc-ryzen-9-9900x.html">Monta un PC con Ryzen 9 9900X</a>
  </div>
</section>
<main>
  <div class="wrap">
    <h2 style="margin-top:0">Guías y comparativas</h2>
    <div class="grid">
      <a class="card" href="pc-ryzen-9-9900x.html"><h3>PC con Ryzen 9 9900X</h3><p>Qué componentes elegir y cuánto cuesta.</p></a>
      <a class="card" href="b850-vs-a620.html"><h3>B850 vs A620</h3><p>Qué placa AM5 te conviene y por qué.</p></a>
      <a class="card" href="ddr5-para-ryzen-9000.html"><h3>Qué DDR5 comprar</h3><p>Velocidad, latencia y capacidad ideales para Ryzen 9000.</p></a>
      <a class="card" href="comprar-informatica-canarias.html"><h3>Comprar en Canarias</h3><p>IGIC, envíos y qué comprobar antes de pagar.</p></a>
    </div>
  </div>
</main>"""

ARTICLES = {
    "b850-vs-a620.html": dict(
        title="Placa B850 vs A620 para AM5: diferencias y cuál elegir",
        description="Comparativa entre las placas AM5 ASUS TUF GAMING B850-PLUS WIFI y A620-PRO WIFI: formato, VRM, PCIe 5.0, overclock y cuál elegir con un Ryzen 9 9900X.",
        h1="Placa B850 vs A620 para AM5: cuál elegir",
        lead="Las dos aceptan procesadores Ryzen de AM5, pero no son para el mismo tipo de PC.",
        crumb="B850 vs A620",
        content="""
      <h2>Resumen</h2>
      <p>Con un procesador potente como el <strong>Ryzen 9 9900X</strong> (12 núcleos), la <strong>B850</strong> es la opción lógica. La A620 funciona, pero está pensada para procesadores más modestos y presupuestos ajustados.</p>

      <div class="tablewrap"><table class="cmp">
        <tr><th></th><th>ASUS TUF GAMING B850-PLUS WIFI</th><th>ASUS TUF GAMING A620-PRO WIFI</th></tr>
        <tr><td>Formato</td><td>ATX</td><td>mATX</td></tr>
        <tr><td>Gama</td><td>Media-alta</td><td>Básica</td></tr>
        <tr><td>Alimentación (VRM)</td><td>Más robusta</td><td>Más justa</td></tr>
        <tr><td>Overclock de CPU</td><td>Sí</td><td>No</td></tr>
        <tr><td>PCIe de la gráfica</td><td>5.0 x16</td><td>4.0 x16</td></tr>
        <tr><td>SSD M.2</td><td>Más ranuras, con PCIe 5.0</td><td>Menos, solo PCIe 4.0</td></tr>
        <tr><td>Wi-Fi</td><td>Wi-Fi 7</td><td>Wi-Fi 6</td></tr>
        <tr><td>Precio</td><td>Más cara</td><td>Más barata</td></tr>
      </table></div>

      <h2>Compatibilidad con el Ryzen 9 9900X</h2>
      <p>Ambas son socket AM5 con DDR5. La B850 salió pensada para la serie 9000. En la A620, comprueba en la web de ASUS la versión de BIOS mínima necesaria para tu procesador: si no la trae de fábrica, tendrías que actualizarla.</p>

      <h2>¿Cuál elegir?</h2>
      <ul>
        <li><strong>B850:</strong> juegos, edición de vídeo, trabajo pesado y si quieres poder ampliar después.</li>
        <li><strong>A620:</strong> equipo básico u ofimática con procesador económico.</li>
      </ul>
""",
    ),
    "ddr5-para-ryzen-9000.html": dict(
        title="Qué memoria DDR5 comprar para Ryzen 9000 (AM5)",
        description="Qué DDR5 elegir para un Ryzen 9000: DDR5-6000 CL30 con EXPO, 32 GB en 2 módulos y errores comunes al comprar un kit.",
        h1="Qué memoria DDR5 comprar para Ryzen 9000",
        lead="La combinación ideal para AM5 es DDR5-6000 con latencia baja y perfil EXPO.",
        crumb="Qué DDR5",
        content="""
      <h2>La receta</h2>
      <ul>
        <li><strong>Velocidad:</strong> 6000 MT/s. Más allá apenas ganas rendimiento en AM5.</li>
        <li><strong>Latencia:</strong> CL30 es el punto óptimo. CL36 funciona, pero es algo más lenta.</li>
        <li><strong>Perfil:</strong> EXPO (AMD), para activar la velocidad con un clic en la BIOS.</li>
        <li><strong>Capacidad:</strong> 32 GB (2x16 GB) para juegos y uso general; 64 GB (2x32 GB) para trabajo pesado.</li>
        <li><strong>Módulos:</strong> 2, no 4. Con 4 módulos en AM5 la memoria suele bajar de velocidad.</li>
      </ul>

      <h2>Error común: comprar "módulos" sin mirar si son kits</h2>
      <p>Muchas tiendas listan un kit como "módulo". La referencia suele indicarlo: por ejemplo, en Corsair <code>CMH16GX5M2...</code> es un kit de <strong>16 GB en total</strong> (2 módulos de 8 GB). Si compras 2 unidades, acabas con 4 módulos de 8 GB. Mira siempre la capacidad total y el número de módulos antes de pagar.</p>

      <h2>Marcas fiables</h2>
      <p>Corsair Vengeance, G.Skill Trident Z5 / Flare X5 y Kingston Fury (DDR5-6000 CL30, con EXPO).</p>
""",
    ),
    "pc-ryzen-9-9900x.html": dict(
        title="PC con Ryzen 9 9900X: componentes recomendados y precio",
        description="Guía para montar un PC con Ryzen 9 9900X: placa B850, DDR5-6000 CL30, disipador y qué más necesitas, con precios orientativos.",
        h1="PC con Ryzen 9 9900X: qué comprar y cuánto cuesta",
        lead="Un procesador de 12 núcleos para juegos, edición y trabajo exigente. Estos son los componentes que acompañan.",
        crumb="PC con 9900X",
        content="""
      <h2>Lista base</h2>
      <div class="tablewrap"><table class="cmp">
        <tr><th>Componente</th><th>Recomendación</th><th>Precio orientativo</th></tr>
        <tr><td>Procesador</td><td>AMD Ryzen 9 9900X (AM5)</td><td>343-370 €</td></tr>
        <tr><td>Placa base</td><td>ASUS TUF GAMING B850-PLUS WIFI</td><td>170-235 €</td></tr>
        <tr><td>Memoria</td><td>32 GB DDR5-6000 CL30 EXPO (2x16 GB)</td><td>Variable (precios altos en 2026)</td></tr>
        <tr><td>Disipador</td><td>Doble torre de 2x120 mm</td><td>30-50 €</td></tr>
        <tr><td>Almacenamiento</td><td>SSD NVMe (PCIe 4.0 va de sobra)</td><td>—</td></tr>
        <tr><td>Fuente</td><td>750 W o más con gráfica potente</td><td>—</td></tr>
        <tr><td>Gráfica</td><td>Imprescindible: el 9900X no es para gráficos integrados</td><td>—</td></tr>
      </table></div>

      <h2>Cosas a tener en cuenta</h2>
      <ul>
        <li>El 9900X <strong>no incluye disipador</strong>: hay que comprarlo.</li>
        <li>Con un procesador de este nivel, la placa B850 evita cuellos de botella y deja margen para ampliar.</li>
        <li>Los precios de la memoria han estado altos: compara entre tiendas.</li>
      </ul>
""",
    ),
    "comprar-informatica-canarias.html": dict(
        title="Comprar informática desde Canarias: IGIC y envíos",
        description="Qué tener en cuenta al comprar componentes de PC desde Canarias: IGIC en lugar de IVA, envíos, gastos y cómo comparar precios entre tiendas.",
        h1="Comprar informática desde Canarias: IGIC y envíos",
        lead="En Canarias los precios y los impuestos no se comparan igual que en la península.",
        crumb="Comprar en Canarias",
        content="""
      <h2>IGIC en lugar de IVA</h2>
      <p>En Canarias se aplica el <strong>IGIC</strong> (el tipo general es el 7 %) en lugar del IVA. Muchos distribuidores muestran el precio sin impuestos y lo añaden al final del pedido.</p>

      <h2>Cómo comparar bien</h2>
      <ol>
        <li>Mira si el precio de cada tienda <strong>incluye o no impuestos</strong>.</li>
        <li>Suma los <strong>gastos de envío</strong> a Canarias.</li>
        <li>Pregunta si hay <strong>gastos aduaneros o gestión adicional</strong>.</li>
        <li>Revisa las condiciones de <strong>garantía y devolución</strong> con envío a las islas.</li>
      </ol>

      <div class="note"><strong>Consejo:</strong> compara siempre el precio final con impuestos y envío, no el precio de la ficha.</div>
""",
    ),
    "afiliados.html": dict(
        title="Enlaces de afiliado | ImosInformática",
        description="Información sobre los enlaces de afiliado de imosinformatica.com.",
        h1="Enlaces de afiliado",
        lead="Cómo se financia esta web.",
        crumb="Enlaces de afiliado",
        content="""
      <p>Algunos enlaces de imosinformatica.com son de afiliado. Si compras a través de ellos, la web puede recibir una comisión, <strong>sin coste adicional para ti</strong>.</p>
      <p>Nuestras comparativas no dependen de esas comisiones.</p>
""",
    ),
    "aviso-legal.html": dict(
        title="Aviso legal | ImosInformática",
        description="Aviso legal de imosinformatica.com.",
        h1="Aviso legal",
        lead="Información del titular del sitio web (LSSI-CE).",
        crumb="Aviso legal",
        content="""
      <!-- TODO OBLIGATORIO: rellenar con los datos reales del titular antes de publicar -->
      <p><strong>Titular:</strong> [NOMBRE Y APELLIDOS O RAZÓN SOCIAL]</p>
      <p><strong>NIF/CIF:</strong> [NIF]</p>
      <p><strong>Domicilio:</strong> [DIRECCIÓN]</p>
      <p><strong>Correo de contacto:</strong> [EMAIL]</p>
      <p><strong>Sitio web:</strong> imosinformatica.com</p>
""",
    ),
    "privacidad.html": dict(
        title="Política de privacidad | ImosInformática",
        description="Política de privacidad de imosinformatica.com.",
        h1="Política de privacidad",
        lead="Qué datos tratamos y para qué.",
        crumb="Privacidad",
        content="""
      <!-- TODO: revisar según analítica/cookies que se usen -->
      <p>Esta web no recoge datos personales mediante formularios. Si se añade analítica, contacto o publicidad, esta política se actualizará.</p>
      <p>Los enlaces de afiliado llevan a tiendas de terceros con su propia política de privacidad.</p>
      <p><strong>Responsable:</strong> [NOMBRE] · <strong>Contacto:</strong> [EMAIL]</p>
""",
    ),
}


def main():
    write("index.html", "ImosInformática: comparativas y guías de componentes de PC",
          "Comparativas de procesadores, placas base y memoria, y consejos para comprar informática desde Canarias.", HOME)
    for file, a in ARTICLES.items():
        # las páginas legales/afiliados no repiten la nota de afiliado
        body = article(a["h1"], a["lead"], a["content"], a["crumb"])
        if file in ("afiliados.html", "aviso-legal.html", "privacidad.html"):
            body = body.replace(AFFILIATE_NOTE, "")
        write(file, a["title"], a["description"], body)

    urls = ["index.html"] + list(ARTICLES)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{SITE}/{u}</loc></url>" for u in urls]
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    (ROOT / "CNAME").write_text("imosinformatica.com\n", encoding="utf-8")
    print(f"Generadas {len(urls)} páginas.")


if __name__ == "__main__":
    main()
