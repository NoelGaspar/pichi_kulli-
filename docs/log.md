# Historial de cambios — Pichi-Kulliñ

## 2026-06-02

### docs: documentación inicial del proyecto
- Creación de `docs/idea.md` con la idea conceptual del proyecto (especies, mecánicas, hardware, etapas).
- Creación de `docs/agents.md`: guía del agente con estructura de carpetas, convenciones y flujo de trabajo.
- Creación de `docs/FSD.md`: especificación funcional detallada con arquitectura, mecánicas, UI, hardware y estrategia de migración.
- Creación de `docs/log.md`: este archivo de registro histórico.

### feat: implementsación inicial del simulador (Etapa 1)
- Creación de `software/` con estructura de proyecto Python.
- Creación de entorno virtual en `software/venv/` con dependencia `pygame`.
- Implementación del módulo `game/`:
  - `animal.py`: clase `Animal` con estadísticas y etapas de vida.
  - `actions.py`: enum `Action` y tabla de efectos.
  - `time_system.py`: conversión tiempo real → tiempo de juego (factor 10×).
  - `stats.py`: decaimiento de estadísticas, efectos críticos y transición de etapas.
  - `species.py`: datos de las 4 especies nativas.
- Implementación del módulo `ui/`:
  - `widgets.py`: clases `Button` y `ProgressBar` reutilizables.
  - `assets.py`: generación de sprites placeholder.
  - `hud.py`: HUD de juego con barras de estadísticas y botones de acción.
  - `screens.py`: máquina de estados (título, selección, juego, final).
- Implementación de `main.py`: bucle principal con escalado 2× (560×480).
- Archivo `data/species.json` con datos extensos de cada especie.
- Tests de integración validando mecánicas y render.

### refac: sistema de input simulado con 3 botones físicos
- Todas las pantallas ahora navegables con ← → (navegar) y ENTER (aceptar).
- `TitleScreen`: ENTER para comenzar.
- `SelectScreen`: ← → para elegir especie, ENTER para confirmar.
- `GameScreen`: ← → para seleccionar acción, ENTER para ejecutar.
- `GameHUD`: nuevo `selected_idx` con métodos `navigate_left/right`.
- `Button.draw()`: nuevo parámetro `selected` que pinta borde amarillo.
- Mouse sigue siendo funcional como alternativa.

### ui: HUD rediseñado — más espacio para sprite, barras compactas con íconos
- Sprite aumentado de 64×64 a 80×80 para mejor visibilidad.
- Barras de estadísticas reducidas de 12px a 8px de alto con 4px de separación.
- Layout a 2 columnas: hambre/energía (fila 1), felicidad/higiene (fila 2), salud centrado (fila 3).
- Etiquetas de texto reemplazadas por íconos de color (cuadro coloreado + letra): H rojo, E amarillo, F rosado, G cian, S verde.
- Mensaje de feedback movido a la posición correcta (y=107) entre sprite y stats.

### ui: ajustes de layout finales
- `SelectScreen`: cuadrícula de especies subida a `start_y=42` para que el hint de navegación (← → ENTER) sea visible.
- `GameScreen`: stats pegados al menú de acciones (`STATS_Y=178`, `actions_y=214`) para maximizar el área del sprite (80×80 centrado en y=62).
- Liberar: botón ahora se muestra en gris cuando `liberable=False` y cambia a verde solo cuando está disponible.

### feat: sistema de guardado persistente (simulación de memoria no volátil)
- Creación de `game/save_manager.py`: funciones `save_game()`, `load_game()`, `reset_save()`, `has_save()`.
- El estado se persiste en `pichi_kulli_save.json` (formato ligero legible).
- `GameScreen` guarda automáticamente tras cada acción, al salir con ESC, al completar el juego, y cada 10 segundos como respaldo.
- `GameScreen.__init__` acepta `save_data` opcional para restaurar estado previo (animal, tiempo de juego, contadores de decaimiento).
- `main.py --reset`: elimina la partida guardada e inicia desde cero.
- `main.py` detecta si hay partida guardada al iniciar y la carga automáticamente, saltando la pantalla de título.

### feat: componente educativo con acción Aprender
- Nueva acción `Action.APRENDER`: +10 felicidad y muestra un dato educativo aleatorio de la especie.
- Seis datos breves por especie (biología, hábitat, conservación) en `game/species.py`.
- Botón 6 dinámico: muestra "Info" (azul) para Aprender; cuando `liberable=True` cambia a "Lib" (verde) para Liberar.
- Mensajes largos (facts) con word-wrap automático y font-size adaptativo.
- Documentación actualizada en `docs/idea.md` y `docs/FSD.md`.

### feat: restricciones de jugabilidad — dormir como estado, límite a jugar
- Dormir ahora es un estado: al activarlo el animal entra en sueño por 120 min de juego (~12 min reales).
- Durante el sueño: todas las acciones están bloqueadas (botones grises), el decaimiento de energía se pausa, y el botón Dormir cambia a "Desp" (Despertar).
- Al despertar (manual o automático): se aplican los efectos completos (+30 energía, +5 felicidad, +5 hambre).
- Jugar: bloqueado si energía < 15, muestra mensaje "está muy cansado para jugar".
- Nuevos campos en `Animal`: `durmiendo`, `sleep_start_min`. Persistidos en save/load.
