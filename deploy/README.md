# Publicar las tres webs en Hetzner

Dominios: guiadeisora.net · imosinformatica.com · sanisidrodeabona.com

## 1. DNS (en el proveedor de cada dominio)
Crea para cada dominio:
- `A`    `@`   → IPv4 del servidor
- `AAAA` `@`   → IPv6 del servidor (opcional)
- `CNAME` `www` → el propio dominio (o un `A` igual al de `@`)

> **sanisidrodeabona.com también es tu correo.** NO borres ni cambies los
> registros `MX`, `TXT` (SPF), DKIM ni DMARC. Solo añade/edita `A` y `www`.

## 2. Servidor (una sola vez, Debian/Ubuntu)
```bash
sudo apt update && sudo apt install -y nginx certbot python3-certbot-nginx rsync
for d in guiadeisora.net imosinformatica.com sanisidrodeabona.com; do
  sudo mkdir -p /var/www/$d
  sudo chown "$USER": /var/www/$d
done
```
Copia las configuraciones y actívalas:
```bash
sudo cp deploy/nginx/*.conf /etc/nginx/sites-available/
for d in guiadeisora.net imosinformatica.com sanisidrodeabona.com; do
  sudo ln -sf /etc/nginx/sites-available/$d.conf /etc/nginx/sites-enabled/$d.conf
done
sudo nginx -t && sudo systemctl reload nginx
```
Firewall de Hetzner: permite los puertos 80 y 443 (y 22 para SSH).

## 3. Subir las webs
```bash
./deploy/deploy.sh usuario@IP_DEL_SERVIDOR
```

## 4. HTTPS (cuando el DNS ya apunte al servidor)
```bash
sudo certbot --nginx -d guiadeisora.net -d www.guiadeisora.net
sudo certbot --nginx -d imosinformatica.com -d www.imosinformatica.com
sudo certbot --nginx -d sanisidrodeabona.com -d www.sanisidrodeabona.com
```
Certbot renueva los certificados solo.

## Antes de publicar
Rellena los datos legales y los TODO de cada `PENDIENTE.md`.
