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

# 📦 Instalación Rápida

Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/network-scanner.git
cd network-scanner
```

Da permisos de ejecución al script:

```bash
chmod +x start.sh
```

Ejecuta la aplicación:

```bash
./start.sh
```

Abre en tu navegador:

```
http://localhost:5000
```

---

## 📄 Archivos Clave

### ✅ `requirements.txt`

```txt
Flask
requests
nmap
speedtest-cli
```

Instalación manual:

```bash
pip install -r requirements.txt
```

### ✅ `start.sh`

```bash
#!/bin/bash
echo "🚀 Activando entorno virtual y ejecutando Network Scanner..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
python app.py
```

---

## 📂 Estructura del Proyecto

```
network-scanner/
├── app.py                   # Backend Flask
├── templates/
│   └── index.html           # Interfaz web
├── static/
│   └── style.css            # Estilo oscuro pro
├── requirements.txt         # Dependencias
├── start.sh                 # Script de ejecución
└── README.md
```

---

## 🧪 Casos de Uso

- 🔐 Auditoría de red interna sin privilegios elevados  
- 🛠️ Diagnóstico de conectividad y dispositivos  
- 📡 Identificación de dispositivos sospechosos  
- 📊 Exportación de datos para análisis en Excel  

---

## 📊 Exportación CSV Inteligente

1. Ejecuta un escaneo.
2. Aplica los filtros deseados.
3. Haz clic en 📥 **Descargar CSV**.

El archivo se descargará automáticamente con un nombre como:

```
scan_2024-05-12_15-30.csv
```

