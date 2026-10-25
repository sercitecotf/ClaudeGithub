#!/usr/bin/env bash
# Sube las tres webs al servidor Hetzner.
# Uso:  ./deploy/deploy.sh usuario@IP_DEL_SERVIDOR
set -euo pipefail

TARGET="${1:?Uso: $0 usuario@IP_DEL_SERVIDOR}"
cd "$(dirname "$0")/.."

declare -A SITES=(
  [guiadeisora]=guiadeisora.net
  [imosinformatica]=imosinformatica.com
  [sanisidrodeabona]=sanisidrodeabona.com
)

for dir in "${!SITES[@]}"; do
  domain="${SITES[$dir]}"
  echo ">> $dir -> /var/www/$domain"
  rsync -az --delete \
    --exclude 'build.py' --exclude 'PENDIENTE.md' --exclude 'CNAME' \
    "$dir/" "$TARGET:/var/www/$domain/"
done
echo "Listo."
