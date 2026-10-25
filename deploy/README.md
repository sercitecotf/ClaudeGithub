# Publicar las tres webs en Hetzner (Ubuntu + Caddy)

Dominios: guiadeisora.net · imosinformatica.com · sanisidrodeabona.com

## 0. Antes de tocar nada: ¿qué usa ya los puertos 80/443?
El servidor ya tiene otras webs. Dos servidores web no pueden usar el mismo puerto.
```bash
sudo ss -tlnp | grep -E ':80 |:443 '
systemctl is-active nginx apache2 caddy
```
Según el resultado:

| Resultado | Qué hacer |
|---|---|
| **Ya hay Caddy** | Añade `caddy/sites.caddy` a su Caddyfile (paso 3). Lo más fácil. |
| **Hay nginx o Apache** y quieres mantenerlo | No instales Caddy. Usa `alternativa-nginx/` con certbot (HTTPS automático también, vía certbot). |
| **Hay nginx/Apache** y aceptas migrar todo a Caddy | Migrar las otras webs a Caddy. Hazlo con cuidado: no lo hagas sin copia de seguridad. |
| **Docker/Traefik/otro proxy** | Pásame la salida y lo adapto. |

> No instales ni pares nada en el servidor hasta saber qué hay: podrías tirar las otras webs.

## 1. DNS (en el proveedor de cada dominio)
Por dominio: `A` `@` → IPv4 del servidor, `AAAA` `@` → IPv6 (opcional), y `www` apuntando igual.

> **sanisidrodeabona.com también es tu correo.** NO borres ni cambies los
> registros `MX`, `TXT` (SPF), DKIM ni DMARC. Solo `A`/`AAAA` y `www`.

## 2. Instalar Caddy (solo si no existe; Ubuntu)
```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update && sudo apt install -y caddy
```

## 3. Añadir las webs
```bash
sudo mkdir -p /etc/caddy/sites
sudo cp caddy/sites.caddy /etc/caddy/sites/estaticas.caddy
# Añade UNA línea al final de /etc/caddy/Caddyfile (conserva lo que ya haya):
echo 'import /etc/caddy/sites/*.caddy' | sudo tee -a /etc/caddy/Caddyfile
for d in guiadeisora.net imosinformatica.com sanisidrodeabona.com; do
  sudo mkdir -p /var/www/$d && sudo chown "$USER": /var/www/$d
done
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```
Firewall de Hetzner: abre 80 y 443 (y 22 para SSH).

## 4. Subir las webs
```bash
./deploy/deploy.sh usuario@IP_DEL_SERVIDOR
```
Cuando el DNS ya apunte al servidor, Caddy pide los certificados la primera vez que se visita cada dominio.

## Antes de abrir al público
Rellena los datos legales y los TODO de cada `PENDIENTE.md`.
