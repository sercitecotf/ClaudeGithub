#!/usr/bin/env bash
# Crea un .tar.gz por web en dist/, listo para subir por SFTP a CWP.
# No usa rsync ni toca el servidor: solo empaqueta en local.
#
# Uso:
#   ./deploy/empaquetar.sh            # versión final
#   ./deploy/empaquetar.sh prueba     # copia de pruebas: con noindex y robots que bloquea todo
set -euo pipefail
cd "$(dirname "$0")/.."
MODO="${1:-final}"
mkdir -p dist
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

for dir in guiadeisora imosinformatica sanisidrodeabona; do
  mkdir -p "$TMP/$dir"
  tar -C "$dir" --exclude=build.py --exclude=PENDIENTE.md --exclude=CNAME \
      --exclude='__pycache__' -cf - . | tar -C "$TMP/$dir" -xf -

  if [ "$MODO" = "prueba" ]; then
    # Evita que Google indexe la copia de pruebas
    for f in "$TMP/$dir"/*.html; do
      sed -i 's|<meta charset="utf-8">|<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">|' "$f"
    done
    printf 'User-agent: *\nDisallow: /\n' > "$TMP/$dir/robots.txt"
    rm -f "$TMP/$dir/sitemap.xml"
    out="dist/$dir-prueba.tar.gz"
  else
    out="dist/$dir.tar.gz"
  fi
  tar -czf "$out" -C "$TMP/$dir" .
  echo "$out"
done
