#!/usr/bin/env bash
# Script de inicio rápido del Laboratorio de XSS - UNICAES
# Gestión de Seguridad en Sistemas Informáticos

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=========================================================="
echo "   LABORATORIO DE SEGURIDAD INFORMÁTICA - UNICAES"
echo "   Taller: Demostración y Mitigación de XSS (CWE-79)"
echo "   Autores: Dennis Guevara | Mario Villeda | Luis Balcaceres"
echo "=========================================================="

# Comprobar python3
if ! command -v python3 &>/dev/null; then
    echo "[-] Error: python3 no está instalado en el sistema."
    exit 1
fi

# Instalar dependencias si no existen
echo "[*] Verificando dependencias necesarias (Flask)..."
python3 -c "import flask" 2>/dev/null || {
    echo "[*] Instalando Flask..."
    python3 -m pip install flask --break-system-packages --user 2>/dev/null || python3 -m pip install flask
}

echo "[+] Entorno preparado exitosamente."
echo "[*] Iniciando servidor web de demostración en http://localhost:5000"
echo "[*] Presiona CTRL+C para detener el laboratorio."
echo "=========================================================="

python3 app.py

