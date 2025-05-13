# 🛰️ Network Scanner Pro -(sin root)

Una aplicación web profesional tipo  para escanear tu red local desde el navegador. Permite detectar todos los dispositivos activos, estimar su sistema operativo, puertos abiertos, latencia, fabricante y más — sin necesidad de privilegios `sudo`.

---

## 🚀 Características

- Escaneo avanzado de red local sin root (Nmap `-sn`)
- Información por dispositivo:
  - IP, MAC y hostname
  - TTL y estimación del sistema operativo
  - Latencia (`ping`)
  - Fabricante (por MAC)
  - Puertos abiertos comunes (22, 80, 443, 8080)
- IP pública y local
- WHOIS y DNS Lookup
- Traceroute hacia cualquier destino
- Filtros interactivos:
  - Buscar por IP, hostname o vendor
  - Filtro por TTL (Windows, Linux/macOS, IoT)
  - Filtro por puertos abiertos
- Exportación directa a **CSV** con nombre automático

---

## 🛠️ Requisitos

- Python 3.8 o superior
- `nmap` instalado en el sistema

```bash
sudo apt install nmap
