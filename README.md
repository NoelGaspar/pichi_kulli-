# Pichi-Kulliñ

Simulador de crianza de fauna nativa chilena. Cuida un animal hasta que esté listo para ser liberado.En desarrollo 


## Versiones

### Desktop (`software/`)
Juego nativo desarrollado con **Pygame**. Corre en Linux, Windows y macOS con Python 3.10+.

```bash
cd software
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Para generar un ejecutable con PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

### Web (`web/`)
Versión para navegador compilada con **Pygbag** a WebAssembly. No requiere instalación.

```bash
cd web
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m pygbag --build .
```

El build genera una carpeta `build/` con contenido estático servible desde GitHub Pages, Netlify o cualquier hosting estático.

### Firmware (próximamente)
Versión embebida para hardware físico con pantalla propia. En desarrollo.
