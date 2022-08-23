# Flask IP Calculator

Based on http://jodies.de/ipcalc, I re-wrote it using Python and Flask with major lifting from the [ipaddress](https://docs.python.org/3/library/ipaddress.html) module.

## Docker-Compose Setup

So that my Caddy config below makes a little more sense, I'm going to post all the relevant services from my `docker-compose.yml` file. However, only the `ipcalc` service is necessary for this setup. If you want the service to be available by itself, make sure to uncomment the `ports` lines. If used in a `docker-compose.yml` with the reverse_proxy service, then the ports are not needed since the services will both see each other.

**Docker folder structure**
```bash
~/docker
  |-- config/
  |    |-- caddy/
  |         |-- Caddyfile
  |         |-- www/
  |              |-- tools.domain.tld/
  |                   |-- web files
  |-- flask_ipcalc/
  |    |-- git sync'd repo
  |-- docker-compose.yml
```


**docker-compose.yml**
```bash
version: "3.3"
services:
  # flask ipcalc
  ipcalc:
    build: ./flask_ipcalc
    image: drowland/ipcalc:latest
    container_name: ipcalc
    restart: unless-stopped
#    ports:
#      - "8100:8100"
  # Web Host
  webhost:
    image: caddy
    container_name: webhost
    restart: unless-stopped
    volumes:
      - caddy_data:/data
      - caddy_config:/config
      - ./config/caddy/www:/srv
      - ./config/caddy/Caddyfile:/etc/caddy/Caddyfile
    ports:
      - "80:80"
      - "443:443"
  # Web Host PHP-FPM
  phpfpm:
    image: php:fpm-alpine
    container_name: phpfpm
    restart: unless-stopped
    volumes:
      - ./config/caddy/www:/srv

volumes:
  caddy_data:
    external: true
  caddy_config:
```

## Reverse Proxy Setup

I used this app with my Caddy Server configuration, as a suffix on an existing site.

```bash
tools.domain.tld {
    root * /srv/tools.domain.tld
    php_fastcgi * phpfpm:9000
    file_server

    route /ipcalc {
        reverse_proxy ipcalc:8100
    }
}
```