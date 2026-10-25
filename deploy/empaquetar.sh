#!/usr/bin/env bash
# Crea un .tar.gz por web en dist/, listo para subir por SFTP a CWP.
# No usa rsync ni toca el servidor: solo empaqueta en local.
# Uso:  ./deploy/empaquetar.sh
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p dist
for dir in guiadeisora imosinformatica sanisidrodeabona; do
  tar -czf "dist/$dir.tar.gz" -C "$dir" \
    --exclude=build.py --exclude=PENDIENTE.md --exclude=CNAME \
    --exclude='__pycache__' .
  echo "dist/$dir.tar.gz"
done
