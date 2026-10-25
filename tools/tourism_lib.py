"""Generador compartido de webs turísticas multilingües (es raíz, /en/, /de/).

Cada web define en su build.py: DOMAIN, NAV, TAGLINE, LOGO, HOME y PAGES,
y llama a build(ROOT, cfg). Sin dependencias.
"""
from pathlib import Path

LANGS = ["es", "en", "de"]
LANG_LABEL = {"es": "ES", "en": "EN", "de": "DE"}
LANG_NAME = {"es": "Español", "en": "English", "de": "Deutsch"}

UI = {
    "es": dict(home="Inicio", legal="Aviso legal", privacy="Privacidad", aff="Enlaces de afiliado",
               main_nav="Principal", lang_nav="Idioma",
               affnote='Algunos enlaces de esta página son de afiliado: si reservas a través de ellos, '
                       'la web recibe una pequeña comisión sin coste extra para ti. '
                       '<a href="{p}afiliados.html">Más información</a>.'),
    "en": dict(home="Home", legal="Legal notice", privacy="Privacy", aff="Affiliate links",
               main_nav="Main", lang_nav="Language",
               affnote='Some links on this page are affiliate links: if you book through them, the site '
                       'earns a small commission at no extra cost to you. '
                       '<a href="{p}afiliados.html">More information</a>.'),
    "de": dict(home="Startseite", legal="Impressum", privacy="Datenschutz", aff="Affiliate-Links",
               main_nav="Hauptmenü", lang_nav="Sprache",
               affnote='Einige Links auf dieser Seite sind Affiliate-Links: Wenn du darüber buchst, erhält die '
                       'Website eine kleine Provision – für dich entstehen keine Mehrkosten. '
                       '<a href="{p}afiliados.html">Mehr erfahren</a>.'),
}

# Páginas comunes (afiliados, aviso legal, privacidad): {d} = dominio
COMMON = {
    "afiliados.html": {
        "es": dict(title="Enlaces de afiliado | {d}", description="Información sobre los enlaces de afiliado de {d}.",
                   h1="Enlaces de afiliado", lead="Cómo se financia esta web.", crumb="Enlaces de afiliado",
                   content="<p>Algunos enlaces de {d} son de afiliado. Si reservas una excursión o un alojamiento a través de ellos, la web puede recibir una comisión, <strong>sin ningún coste adicional para ti</strong>.</p>\n<p>Esa comisión nos ayuda a mantener la web. Nuestras recomendaciones no dependen de ella.</p>"),
        "en": dict(title="Affiliate links | {d}", description="Information about the affiliate links on {d}.",
                   h1="Affiliate links", lead="How this website is funded.", crumb="Affiliate links",
                   content="<p>Some links on {d} are affiliate links. If you book a tour or accommodation through them, the site may receive a commission, <strong>at no additional cost to you</strong>.</p>\n<p>This commission helps us keep the site running. Our recommendations do not depend on it.</p>"),
        "de": dict(title="Affiliate-Links | {d}", description="Informationen zu den Affiliate-Links auf {d}.",
                   h1="Affiliate-Links", lead="Wie diese Website finanziert wird.", crumb="Affiliate-Links",
                   content="<p>Einige Links auf {d} sind Affiliate-Links. Wenn du darüber eine Tour oder eine Unterkunft buchst, kann die Website eine Provision erhalten, <strong>ohne dass dir zusätzliche Kosten entstehen</strong>.</p>\n<p>Diese Provision hilft uns, die Website zu betreiben. Unsere Empfehlungen hängen nicht davon ab.</p>"),
    },
    "aviso-legal.html": {
        "es": dict(title="Aviso legal | {d}", description="Aviso legal de {d}.", h1="Aviso legal",
                   lead="Información del titular del sitio web (LSSI-CE).", crumb="Aviso legal",
                   content="<!-- TODO OBLIGATORIO: rellenar con los datos reales del titular antes de publicar -->\n<p><strong>Titular:</strong> [NOMBRE Y APELLIDOS O RAZÓN SOCIAL]</p>\n<p><strong>NIF/CIF:</strong> [NIF]</p>\n<p><strong>Domicilio:</strong> [DIRECCIÓN]</p>\n<p><strong>Correo de contacto:</strong> [EMAIL]</p>\n<p><strong>Sitio web:</strong> {d}</p>"),
        "en": dict(title="Legal notice | {d}", description="Legal notice of {d}.", h1="Legal notice",
                   lead="Information about the website owner (Spanish LSSI-CE).", crumb="Legal notice",
                   content="<!-- TODO REQUIRED: fill in the real owner details before publishing -->\n<p><strong>Owner:</strong> [FULL NAME OR COMPANY NAME]</p>\n<p><strong>Tax ID (NIF/CIF):</strong> [NIF]</p>\n<p><strong>Address:</strong> [ADDRESS]</p>\n<p><strong>Contact email:</strong> [EMAIL]</p>\n<p><strong>Website:</strong> {d}</p>"),
        "de": dict(title="Impressum | {d}", description="Impressum von {d}.", h1="Impressum",
                   lead="Angaben zum Betreiber der Website (spanisches LSSI-CE).", crumb="Impressum",
                   content="<!-- TODO PFLICHT: vor der Veröffentlichung die echten Betreiberdaten eintragen -->\n<p><strong>Betreiber:</strong> [NAME ODER FIRMA]</p>\n<p><strong>Steuernummer (NIF/CIF):</strong> [NIF]</p>\n<p><strong>Anschrift:</strong> [ADRESSE]</p>\n<p><strong>Kontakt-E-Mail:</strong> [E-MAIL]</p>\n<p><strong>Website:</strong> {d}</p>"),
    },
    "privacidad.html": {
        "es": dict(title="Política de privacidad | {d}", description="Política de privacidad de {d}.", h1="Política de privacidad",
                   lead="Qué datos tratamos y para qué.", crumb="Privacidad",
                   content="<!-- TODO: revisar según analítica/cookies que se usen -->\n<p>Esta web no recoge datos personales mediante formularios. Si en el futuro se añade analítica, contacto o publicidad, esta política se actualizará.</p>\n<p>Los enlaces de afiliado llevan a sitios de terceros con su propia política de privacidad.</p>\n<p><strong>Responsable:</strong> [NOMBRE] · <strong>Contacto:</strong> [EMAIL]</p>"),
        "en": dict(title="Privacy policy | {d}", description="Privacy policy of {d}.", h1="Privacy policy",
                   lead="What data we process and why.", crumb="Privacy",
                   content="<!-- TODO: review according to the analytics/cookies actually used -->\n<p>This website does not collect personal data through forms. If analytics, a contact form or advertising are added in the future, this policy will be updated.</p>\n<p>Affiliate links lead to third-party sites that have their own privacy policies.</p>\n<p><strong>Controller:</strong> [NAME] · <strong>Contact:</strong> [EMAIL]</p>"),
        "de": dict(title="Datenschutzerklärung | {d}", description="Datenschutzerklärung von {d}.", h1="Datenschutzerklärung",
                   lead="Welche Daten wir verarbeiten und warum.", crumb="Datenschutz",
                   content="<!-- TODO: je nach verwendeter Analyse/Cookies prüfen -->\n<p>Diese Website erhebt keine personenbezogenen Daten über Formulare. Falls künftig Analyse, ein Kontaktformular oder Werbung hinzukommen, wird diese Erklärung aktualisiert.</p>\n<p>Affiliate-Links führen zu Seiten Dritter mit eigener Datenschutzerklärung.</p>\n<p><strong>Verantwortlicher:</strong> [NAME] · <strong>Kontakt:</strong> [E-MAIL]</p>"),
    },
}


COMERCIOS_UI = {
    "es": dict(file_label="Comercios", title="Comercios de {zona} | {d}",
               description="Directorio de comercios y negocios locales de {zona}: restaurantes, alojamientos, tiendas, servicios y actividades.",
               h1="Comercios y negocios de {zona}", crumb="Comercios",
               lead="Negocios locales de la zona: apoya el comercio de cercanía.",
               empty="Estamos preparando el directorio. Pronto encontrarás aquí los comercios y negocios de {zona}.",
               cta_h="¿Tienes un negocio en {zona}?",
               cta="Escríbenos para aparecer en este directorio: [EMAIL]",
               addr="Dirección", phone="Teléfono", web="Web", noverify="",
               cats=dict(food="Comer y beber", stay="Alojamiento", shop="Tiendas y supermercados",
                         services="Servicios", activities="Actividades y excursiones")),
    "en": dict(file_label="Local businesses", title="Local businesses in {zona} | {d}",
               description="Directory of local shops and businesses in {zona}: restaurants, accommodation, shops, services and activities.",
               h1="Local shops and businesses in {zona}", crumb="Local businesses",
               lead="Local businesses in the area: support small, local trade.",
               empty="We are preparing the directory. Soon you will find the local shops and businesses of {zona} here.",
               cta_h="Do you run a business in {zona}?",
               cta="Get in touch to be listed in this directory: [EMAIL]",
               addr="Address", phone="Phone", web="Website", noverify="",
               cats=dict(food="Food and drink", stay="Accommodation", shop="Shops and supermarkets",
                         services="Services", activities="Activities and tours")),
    "de": dict(file_label="Lokale Geschäfte", title="Lokale Geschäfte in {zona} | {d}",
               description="Verzeichnis lokaler Geschäfte und Betriebe in {zona}: Restaurants, Unterkünfte, Läden, Dienstleistungen und Aktivitäten.",
               h1="Lokale Geschäfte und Betriebe in {zona}", crumb="Lokale Geschäfte",
               lead="Lokale Betriebe der Gegend: unterstütze den Handel vor Ort.",
               empty="Wir bereiten das Verzeichnis vor. Bald findest du hier die lokalen Geschäfte und Betriebe in {zona}.",
               cta_h="Hast du einen Betrieb in {zona}?",
               cta="Schreib uns, um in diesem Verzeichnis zu erscheinen: [E-MAIL]",
               addr="Adresse", phone="Telefon", web="Website", noverify="",
               cats=dict(food="Essen und Trinken", stay="Unterkunft", shop="Läden und Supermärkte",
                         services="Dienstleistungen", activities="Aktivitäten und Touren")),
}


def _esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def comercios_page(lang, domain, zona, items):
    u = COMERCIOS_UI[lang]
    fmt = lambda t: t.replace("{zona}", zona).replace("{d}", domain)
    out = []
    if not items:
        out.append('      <p>' + fmt(u["empty"]) + "</p>")
    else:
        for cat, label in u["cats"].items():
            group = [c for c in items if c.get("category") == cat]
            if not group:
                continue
            out.append("      <h2>" + label + "</h2>")
            out.append('      <div class="grid">')
            for c in group:
                rows = []
                desc = c.get("desc", {}).get(lang) or c.get("desc", {}).get("es", "")
                if desc:
                    rows.append("<p>" + _esc(desc) + "</p>")
                if c.get("address"):
                    rows.append("<p><strong>" + u["addr"] + ":</strong> " + _esc(c["address"]) + "</p>")
                if c.get("phone"):
                    tel = "".join(ch for ch in c["phone"] if ch.isdigit() or ch == "+")
                    rows.append('<p><strong>' + u["phone"] + ':</strong> <a href="tel:' + tel + '">' + _esc(c["phone"]) + "</a></p>")
                if c.get("web"):
                    rows.append('<p><strong>' + u["web"] + ':</strong> <a href="' + _esc(c["web"]) + '" rel="noopener nofollow">' + _esc(c["web"]) + "</a></p>")
                out.append('        <div class="card"><h3>' + _esc(c["name"]) + "</h3>" + "".join(rows) + "</div>")
            out.append("      </div>")
    out.append('      <div class="note"><strong>' + fmt(u["cta_h"]) + "</strong> " + fmt(u["cta"]) + "</div>")
    return dict(title=fmt(u["title"]), description=fmt(u["description"]), h1=fmt(u["h1"]),
                lead=fmt(u["lead"]), crumb=u["crumb"], content="\n".join(out))


LAYOUT = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
{hreflang}
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<link rel="stylesheet" href="{p}css/style.css">
</head>
<body>
<header class="site">
  <div class="wrap">
    <a class="logo" href="index.html">{logo}</a>
    <nav class="main" aria-label="{main_nav}">
{nav}
    </nav>
    <nav class="lang" aria-label="{lang_nav}">{switcher}</nav>
  </div>
</header>
{body}
<footer class="site">
  <div class="wrap">
    <div>© {year} {domain} · {tagline}</div>
    <div><a href="aviso-legal.html">{legal}</a> · <a href="privacidad.html">{privacy}</a> · <a href="afiliados.html">{aff}</a></div>
  </div>
</footer>
</body>
</html>
"""


def _prefix(lang):
    return "" if lang == "es" else "../"


def _url(site, lang, file):
    return f"{site}/{file}" if lang == "es" else f"{site}/{lang}/{file}"


def build(root: Path, cfg: dict, year: int = 2026):
    domain = cfg["DOMAIN"]
    site = f"https://{domain}"
    root = Path(root)
    pages_common = {
        f: {l: {k: v.replace("{d}", domain) for k, v in d.items()} for l, d in langs.items()}
        for f, langs in COMMON.items()
    }
    zonas = cfg["ZONA"]
    comercios = {"comercios.html": {
        l: comercios_page(l, domain, zonas[l], cfg.get("COMERCIOS", [])) for l in LANGS}}
    all_pages = {**cfg["PAGES"], **comercios, **pages_common}
    files = ["index.html"] + list(all_pages)

    for lang in LANGS:
        p = _prefix(lang)
        ui = UI[lang]
        outdir = root if lang == "es" else root / lang
        outdir.mkdir(parents=True, exist_ok=True)
        affnote = '<p class="affiliate">' + ui["affnote"].format(p="") + "</p>"

        def render(file, title, desc, body):
            hreflang = "\n".join(
                f'<link rel="alternate" hreflang="{l}" href="{_url(site, l, file)}">' for l in LANGS
            ) + f'\n<link rel="alternate" hreflang="x-default" href="{_url(site, "es", file)}">'
            cur_true = ' aria-current="true"'
            cur_page = ' aria-current="page"'
            sw_items = []
            for l in LANGS:
                href = ("" if lang == "es" else "../") + ("" if l == "es" else l + "/") + file
                cur = cur_true if l == lang else ""
                sw_items.append(
                    '<a href="' + href + '" hreflang="' + l + '" lang="' + l +
                    '" title="' + LANG_NAME[l] + '"' + cur + ">" + LANG_LABEL[l] + "</a>"
                )
            switcher = " ".join(sw_items)
            nav_items = []
            for href, label in cfg["NAV"][lang]:
                cur = cur_page if href == file else ""
                nav_items.append('      <a href="' + href + '"' + cur + ">" + label + "</a>")
            nav = "\n".join(nav_items)
            html = LAYOUT.format(
                lang=lang, title=title, description=desc, canonical=_url(site, lang, file),
                hreflang=hreflang, p=p, logo=cfg["LOGO"], nav=nav, switcher=switcher, body=body,
                year=year, domain=domain, tagline=cfg["TAGLINE"][lang],
                main_nav=ui["main_nav"], lang_nav=ui["lang_nav"],
                legal=ui["legal"], privacy=ui["privacy"], aff=ui["aff"],
            )
            (outdir / file).write_text(html, encoding="utf-8")

        h = cfg["HOME"][lang]
        render("index.html", h["title"], h["description"], h["body"])

        for file, langs in all_pages.items():
            pg = langs[lang]
            content = pg["content"].replace("[[AFF]]", affnote)
            body = f"""<main>
  <div class="wrap">
    <article>
      <div class="breadcrumbs"><a href="index.html">{ui["home"]}</a> › {pg["crumb"]}</div>
      <h1>{pg["h1"]}</h1>
      <p class="lead">{pg["lead"]}</p>
{content}
    </article>
  </div>
</main>"""
            render(file, pg["title"], pg["description"], body)

    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for f in files:
        for lang in LANGS:
            sm.append(f"  <url><loc>{_url(site, lang, f)}</loc>")
            for l in LANGS:
                sm.append(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{_url(site, l, f)}"/>')
            sm.append("  </url>")
    sm.append("</urlset>")
    (root / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    (root / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {site}/sitemap.xml\n", encoding="utf-8")
    (root / "CNAME").write_text(domain + "\n", encoding="utf-8")
    print(f"{domain}: {len(files)} páginas x {len(LANGS)} idiomas")
