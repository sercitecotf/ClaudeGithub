# Publicar las tres webs en el servidor (AlmaLinux 9 + CWP + Apache)

Datos del servidor (aportados por la sesión que lo gestiona): VPS Hetzner,
IP `188.245.197.101`, Apache de CWP en 80/443, vhosts gestionados por CWP,
docroot `/home/<usuario>/public_html`.

> **No instalar nada en el servidor** (ni Caddy ni nginx): chocaría con Apache.
> **No tocar el DNS** de ningún dominio sin que lo autorice el usuario.
> El correo de guiadeisora.net y sanisidrodeabona.com sigue en HostGator;
> sus DNS también. Hay una migración planificada: no cambiar MX/SPF/DKIM/DMARC.

| Dominio | Cuenta CWP | DNS | Correo |
|---|---|---|---|
| imosinformatica.com | `imos` (existe) | Hetzner DNS | En este servidor |
| guiadeisora.net | `guiadei` (existe) | HostGator | HostGator |
| sanisidrodeabona.com | **no existe aún** | HostGator | HostGator |

## ⚠️ Antes de subir: ya hay webs en `imos` y `guiadei`
Las cuentas tienen contenido en `public_html`. **No lo sobrescribas sin copia.**
Por SSH, para cada cuenta:
```bash
cp -a /home/imos/public_html /root/backup-imos-public_html-$(date +%F)
ls -la /home/imos/public_html     # mira qué hay antes de decidir
```
Decide si la web nueva sustituye a la actual. Si no estás seguro, súbela a un
subdirectorio de prueba o a un dominio de pruebas primero.

## Primero: subir a una carpeta de PRUEBAS (recomendado)
Así no se toca la web actual. La copia de pruebas lleva `noindex` y un
`robots.txt` que bloquea a los buscadores. Los enlaces son relativos, así que
funcionan dentro de una subcarpeta.

1. Empaqueta en modo prueba (en tu equipo):
   ```bash
   ./deploy/empaquetar.sh prueba      # genera dist/<web>-prueba.tar.gz
   ```
2. Sube cada `dist/<web>-prueba.tar.gz` a `/root/` por SFTP.
3. Por SSH, crea la carpeta de pruebas y descomprime (cambia `U` y el archivo):
   ```bash
   U=imos                              # imos | guiadei | (usuario nuevo)
   mkdir -p /home/$U/public_html/pruebas
   tar -xzf /root/imosinformatica-prueba.tar.gz -C /home/$U/public_html/pruebas/
   chown -R $U:$U /home/$U/public_html/pruebas
   find /home/$U/public_html/pruebas -type d -exec chmod 755 {} \;
   find /home/$U/public_html/pruebas -type f -exec chmod 644 {} \;
   ```
   (`public_html` no cambia de propietario: solo se toca `pruebas/`.)
4. Mira el resultado sin cambiar el DNS:
   ```bash
   curl -k --resolve imosinformatica.com:443:188.245.197.101 https://imosinformatica.com/pruebas/ | head
   ```
   O añade `188.245.197.101 imosinformatica.com` al fichero `hosts` de tu equipo y
   abre `https://imosinformatica.com/pruebas/` en el navegador (igual para los otros dominios).
5. Para quitarlo: `rm -rf /home/$U/public_html/pruebas`.

> `sanisidrodeabona.com` necesita primero la cuenta en CWP (paso 2 más abajo).
> Mientras el DNS siga en HostGator, solo se ve con `--resolve` o `hosts`.

## 1. Empaquetar (en tu equipo)
```bash
./deploy/empaquetar.sh      # genera dist/*.tar.gz
```

## 2. Crear la cuenta que falta
CWP > Cuentas de usuario > Nueva cuenta: dominio `sanisidrodeabona.com`,
un usuario nuevo (p. ej. `sanisi`).
Esto no cambia el DNS ni el correo; solo crea el vhost en el servidor.

## 3. Subir y desplegar (por SFTP/SSH, como root)
Sube `dist/<web>.tar.gz` a `/root/` y, por cada cuenta:
```bash
U=imos                                  # o guiadei / el usuario nuevo
tar -xzf /root/imosinformatica.tar.gz -C /home/$U/public_html/
chown -R $U:$U /home/$U/public_html
chgrp nobody /home/$U/public_html
find /home/$U/public_html -type d -exec chmod 755 {} \;
find /home/$U/public_html -type f -exec chmod 644 {} \;
```

## 4. Probar SIN cambiar el DNS
Desde tu equipo (fuerza el dominio a la IP del servidor):
```bash
curl -k --resolve guiadeisora.net:443:188.245.197.101 https://guiadeisora.net/ | head
```
O añade una línea al fichero `hosts` de tu equipo. Así revisas la web real antes
de tocar el DNS.

## 5. HTTPS
CWP > SSL Certificates > AutoSSL (Let's Encrypt). Requiere que el DNS del
dominio ya apunte a `188.245.197.101`; si no, falla la validación.

## 6. DNS (solo cuando el usuario lo autorice)
- **imosinformatica.com** (Hetzner DNS): cambiar solo el registro `A` de la web.
  Mantener TTL 3600 y no tocar MX/TXT. Los `MX`/`CNAME` llevan punto final.
- **guiadeisora.net / sanisidrodeabona.com** (HostGator): cambiar solo el `A`
  de la web, conservando MX/TXT. Mejor esperar a la migración de dominios.

## Antes de abrir al público
Rellenar datos legales y los TODO de cada `PENDIENTE.md`.
