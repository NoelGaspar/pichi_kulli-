#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "=== Pichi-Kulliñ — Setup ==="

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 no encontrado. Instálalo primero."
    exit 1
fi

echo "[1/3] Creando entorno virtual..."
python3 -m venv venv

echo "[2/3] Activando entorno e instalando dependencias..."
source venv/bin/activate
pip install -q -r requirements.txt

echo "[3/3] Listo!"
echo ""
echo "Para ejecutar el juego:"
echo "  cd software && source venv/bin/activate && python main.py"
echo ""
echo "Para generar un ejecutable con PyInstaller:"
echo "  cd software && source venv/bin/activate && pip install pyinstaller && pyinstaller --onefile main.py"
