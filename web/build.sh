#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "=== Pichi-Kulliñ — Build Web ==="

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 no encontrado"
    exit 1
fi

echo "[1/3] Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

echo "[2/3] Instalando dependencias..."
pip install -q -r requirements.txt

echo "[3/3] Build con pygbag..."
python3 -m pygbag --build .

echo ""
echo "Build completado. Los archivos estáticos están en: web/build/"
echo ""
echo "Para probar localmente:"
echo "  python3 -m pygbag ."
echo ""
echo "Para subir a GitHub Pages, sube el contenido de web/build/ a la branch gh-pages"
echo "o configura GitHub Pages para que sirva desde la carpeta web/build/ en tu branch main."
