#!/bin/bash
echo "🚀 Activando entorno virtual y ejecutando Network Scanner..."

# Crear entorno si no existe
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activar entorno
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py
