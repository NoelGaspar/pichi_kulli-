# Especificación Funcional del Sistema (FSD) — Pichi-Kulliñ

## 1. Introducción

### 1.1 Propósito
Este documento define las especificaciones técnicas del tamagochi educativo **Pichi-Kulliñ**, que servirá como base para la implementación de un simulador en Python (Etapa 1) y su posterior migración a un dispositivo físico basado en ESP32 (Etapa 2).

### 1.2 Alcance
Cubre la arquitectura del sistema, mecánicas de juego, interfaz de usuario, hardware objetivo y estrategia de migración entre etapas.

### 1.3 Especies del juego
- Gato Güiña (*Leopardus guigna*)
- Chungungo (*Lontra felina*)
- Ranita de Darwin (*Rhinoderma darwinii*)
- Zorro chilote (*Lycalopex fulvipes*)

---

## 2. Arquitectura del sistema

### 2.1 Visión general

```
┌─────────────────────────────────────────────────┐
│                   Pichi-Kulliñ                   │
├─────────────────────────────────────────────────┤
│  Etapa 1: Simulador Python                       │
│  ┌─────────┐ ┌──────────┐ ┌──────────────────┐  │
│  │ Game    │ │ UI       │ │ Input (teclado/  │  │
│  │ Engine  │ │ (pygame) │ │       mouse)     │  │
│  └────┬────┘ └────┬─────┘ └──────────────────┘  │
│       └───────────┴──────────────┘              │
│                      │                          │
├──────────────────────┼──────────────────────────┤
│  Etapa 2: Físico     │                          │
│  ┌─────────┐ ┌───────┴──────┐ ┌──────────────┐ │
│  │ Game    │ │ TFT ST7789   │ │ Botones/     │ │
│  │ Engine  │ │ 280×240      │ │ Táctil       │ │
│  └────┬────┘ └──────────────┘ └──────────────┘ │
│       │                                          │
│  ┌────┴────┐  ┌──────────┐  ┌──────────────┐   │
│  │ RTC     │  │ Buzzer   │  │ Batería Lipo │   │
│  │ RV8803  │  │ PWM      │  │ + Carga      │   │
│  └─────────┘  └──────────┘  └──────────────┘   │
└─────────────────────────────────────────────────┘
```

### 2.2 Principios de diseño
- **Modularidad**: El Game Engine debe ser independiente de la capa de presentación.
- **Portabilidad**: La lógica de juego se escribe para ser directamente traducible de Python a C++.
- **Simulación fiel**: El tiempo de juego debe ser calculado con precisión (1 min real = 10 min juego).
- **Respeto de resolución**: Toda la interfaz se diseña para 280×240 píxeles desde el inicio.

---

## 3. Especificación de hardware (Etapa 2)

| Componente | Especificación | Interfaz |
|------------|---------------|----------|
| MCU | ESP32 (Xtensa LX6) | GPIO, I2C, SPI |
| Pantalla | TFT 280×240, driver ST7789 | SPI |
| RTC | RV8803 | I2C |
| Batería | Lipo con módulo de carga | ADC (medición) |
| Buzzer | Parlante pasivo | PWM |

**Asignación de pines (propuesta inicial):**

| Señal | GPIO ESP32 | Notas |
|-------|-----------|-------|
| TFT CS | 5 | SPI |
| TFT DC | 4 | SPI |
| TFT RST | 3 | SPI |
| TFT MOSI | 23 | SPI |
| TFT SCK | 18 | SPI |
| TFT BL | 2 | Backlight PWM |
| RTC SDA | 21 | I2C |
| RTC SCL | 22 | I2C |
| Buzzer | 25 | PWM |
| Botón A | 32 | Pull-up |
| Botón B | 33 | Pull-up |
| Botón C | 26 | Pull-up |
| Bat ADC | 34 | Divider 2:1 |

---

## 4. Especificación de software — Etapa 1 (Simulador Python)

### 4.1 Game Loop

```
while running:
    dt = clock.tick(60) / 1000.0        # 60 FPS fijo
    
    # 1. Actualizar tiempo de juego
    game_time = update_game_time(dt)     # dt * factor_tiempo
    
    # 2. Procesar entrada
    actions = process_input()
    
    # 3. Actualizar lógica
    for action in actions:
        apply_action(animal, action)
    update_stats(animal, game_time)
    check_critical_effects(animal, game_time)
    check_life_stage(animal, game_time)
    check_end_conditions(animal)
    
    # 4. Renderizar
    render(screen, animal, ui_state)
```

### 4.2 Módulos del simulador

| Módulo | Responsabilidad |
|--------|----------------|
| `main.py` | Inicialización, game loop, coordinación |
| `game/animal.py` | Clase `Animal`: estado, estadísticas, etapa de vida |
| `game/actions.py` | Efectos de cada acción sobre estadísticas |
| `game/stats.py` | Gestión de decaimiento y efectos críticos |
| `game/time_system.py` | Conversión tiempo real ↔ tiempo de juego |
| `game/species.py` | Datos específicos por especie + datos educativos (facts) |
| `game/save_manager.py` | Persistencia del estado en archivo JSON (simula memoria no volátil) |
| `ui/screens.py` | Máquina de estados de pantallas |
| `ui/hud.py` | Render del HUD principal |
| `ui/widgets.py` | Botones, barras de progreso, indicadores |
| `ui/assets.py` | Carga y gestión de sprites/fuentes |
| `data/species.json` | Configuración de especies |

### 4.3 Clase `Animal`

```python
@dataclass
class AnimalState:
    especie: str
    nombre: str
    hambre: int       # 0-100
    energia: int      # 0-100
    felicidad: int    # 0-100
    higiene: int      # 0-100
    salud: int        # 0-100
    etapa: str        # "cachorro", "joven", "adulto", "liberado"
    triste: bool      # True si felicidad == 0
    tiempo_total: float  # minutos de juego acumulados
    vivo: bool
```

### 4.4 Sistema de tiempo

```
factor_tiempo = 10    # 1 min real = 10 min juego

tiempo_juego_min = tiempo_real_seg * factor_tiempo / 60
```

Cada frame se acumulan fracciones de minuto de juego para aplicar decaimientos progresivos sin pérdida de precisión.

---

## 5. Mecánicas de juego

### 5.1 Variables y rangos

| Variable | Rango | Valor inicial | Decaimiento | Intervalo |
|----------|-------|---------------|-------------|-----------|
| Hambre | 0–100 | 30 | +4 | cada 10 min juego |
| Energía | 0–100 | 80 | -5 | cada 15 min juego |
| Felicidad | 0–100 | 70 | -5 | cada 20 min juego |
| Higiene | 0–100 | 80 | -5 | cada 20 min juego |
| Salud | 0–100 | 80 | — | no decae sola |

### 5.2 Acciones del jugador

| Acción | Hambre | Energía | Felicidad | Higiene | Salud |
|--------|--------|---------|-----------|---------|-------|
| Alimentar | -20 | 0 | +5 | 0 | 0 |
| Jugar | +5 | -10 | +15 | 0 | 0 |
| Dormir | +5 | +30 | +5 | 0 | 0 |
| Limpiar | 0 | 0 | +5 | +20 | 0 |
| Curar | 0 | 0 | 0 | 0 | +20 |
| Aprender | 0 | 0 | +10 | 0 | 0 |
| Liberar | — | — | — | — | — reinicio — |

La acción Aprender comparte el sexto slot de la UI con Liberar. Mientras el animal no sea liberable, el botón muestra "Info" y al presionarlo entrega un hecho educativo aleatorio de la especie. Al cumplir las condiciones de liberación (5 días de juego, adulto, salud=100), el botón cambia a "Lib" (verde) reemplazando a Aprender.

Todas las acciones tienen un límite: no pueden llevar una variable fuera del rango 0–100 (se trunca).

### 5.3 Efectos críticos (aplicados cada 10 min juego)

| Condición | Efecto |
|-----------|--------|
| Hambre >= 90 | Salud -= 2 |
| Higiene <= 20 | Salud -= 2 |
| Energía == 0 | Salud -= 1 |
| Felicidad == 0 | Estado "triste": todas las necesidades aumentan su decaimiento en +2 puntos por intervalo |
| Triste + cualquier otro crítico | Se acumulan |

### 5.4 Etapas de vida

| Transición | Condición |
|------------|-----------|
| Cachorro → Joven | tiempo_total >= 1 día de juego (144 min reales) |
| Joven → Adulto | tiempo_total >= 4 días de juego (576 min reales, 3 desde joven) |
| Adulto → Liberable | tiempo_total >= 5 días de juego (720 min reales), salud == 100 |

### 5.5 Condiciones de fin

| Condición | Resultado |
|-----------|-----------|
| Salud == 0 | Pantalla "Rescate": especialistas rescatan al animal. Juego se reinicia. |
| Liberable + acción Liberar | Pantalla "Liberación": animal vuelve a su hábitat. Créditos. Reinicio. |

---

## 6. Interfaz de usuario

### 6.1 Resolución y canvas
- **Resolución fija**: 280 × 240 píxeles.
- **Orientación**: Apaisado (landscape).
- **Escalado**: En el simulador se usa una ventana de 560×480 con escalado ×2 para facilitar la visualización.

### 6.2 Mapa de pantallas

```
┌──────────────┐
│   Título     │  → "Pichi-Kulliñ", botón "Comenzar"
└──────┬───────┘
       ▼
┌──────────────┐
│  Selección   │  → 4 especies con imagen y nombre
│  de especie  │
└──────┬───────┘
       ▼
┌──────────────┐
│  Juego       │  → HUD principal (ver 6.3)
│  (principal) │
└──────┬───────┘
       │
       ├── Salud = 0 ──► ┌──────────────┐
       │                  │  Rescate     │ → Título
       │                  └──────────────┘
       │
       └── Liberar ──► ┌──────────────┐
                        │  Liberación  │ → Créditos → Título
                        └──────────────┘
```

### 6.3 Layout del HUD de juego (280×240)

```
┌──────────────────────────────────────┐
│  [Etapa] [Nombre]        ⏱️ 00:00   │  ← 30px
├──────────────────────────────────────┤
│                                      │
│          SPRITE DEL ANIMAL           │  ← 100px
│          (120×120 aprox)             │
│                                      │
├──────────────────────────────────────┤
│  🍖 ████████░░ 80  ⚡ ██████░░░░ 60│  ← 20px c/u
│  ❤️ ██████░░░░ 60  🧹 ████████░ 70│  ← 20px c/u
│  ❤️‍🩹 ████████░░ 80                  │  ← 20px c/u
├──────────────────────────────────────┤
│  [🍎] [🎮] [😴] [🧹] [💊] [🆓]  │  ← botones 40×40
└──────────────────────────────────────┘
```

### 6.4 Botones de acción (íconos)

| Ícono | Acción |
|-------|--------|
| 🍎 | Alimentar |
| 🎮 | Jugar |
| 😴 | Dormir |
| 🧹 | Limpiar |
| 💊 | Curar |
| 📖 | Aprender (slot compartido con Liberar) |
| 🆓 | Liberar (reemplaza a Aprender cuando está disponible) |

### 6.5 Indicadores visuales
- **Barras de progreso**: color verde (≥50), amarillo (25–49), rojo (<25).
- **Efecto triste**: el sprite del animal se muestra con expresión triste, fondo ligeramente azulado.
- **Transiciones de etapa**: animación de evolución al cambiar de etapa.
- **Notificaciones**: burbuja de texto sobre el animal para feedback de acciones.

---

## 7. Sistema de sonido (Etapa 2)

| Evento | Sonido |
|--------|--------|
| Acción realizada | Tono corto de confirmación |
| Cambio de etapa | Melodía ascendente |
| Estado crítico | Tono de alerta intermitente |
| Salud = 0 | Melodía triste descendente |
| Liberación | Melodía alegre ascendente |

En la Etapa 1, los sonidos son opcionales (se pueden simular con pitidos de pygame o desactivarse).

---

## 8. Estrategia de migración (Etapa 1 → Etapa 2)

1. **Encapsular lógica**: Toda la lógica de juego en `game/` sin dependencias de pygame.
2. **Definir interfaz `IGameRenderer`**: Contrato abstracto que ambas etapas implementan.
3. **Traducir estructuras de datos**: `AnimalState` en Python → `struct AnimalState` en C++.
4. **Reimplementar renderer**: Usar TFT_eSPI para dibujar primitivas en lugar de pygame.
5. **Adaptar input**: Eventos de teclado/mouse → lectura de botones GPIO.
6. **Sistema de tiempo**: `time.time()` en Python → RTC RV8803 + millis() en ESP32.

### 8.1 Equivalencias Python → C++

| Python | C++ (Arduino) |
|--------|---------------|
| `class Animal` | `class Animal` |
| `pygame.Surface` | `TFT_eSPI` + Sprites |
| `pygame.time.Clock` | `millis()` + RTC |
| `dataclass` | `struct` |
| `dict` config | `constexpr` arrays / PROGMEM |
| `pygame.mouse` | `digitalRead()` botones |

---

## 9. Pruebas y validación

### 9.1 Simulador (Etapa 1)
- Tests unitarios para decaimiento de estadísticas.
- Tests de integración para condiciones críticas y transiciones de etapa.
- Tests de bucle de 24h simuladas para verificar condiciones de liberación.
- Validación visual manual con el simulador corriendo.

### 9.2 Físico (Etapa 2)
- Test de visualización (todos los sprites, todas las pantallas).
- Test de RTC (precisión de tiempo de juego vs tiempo real).
- Test de acciones con botones.
- Test de consumo de batería.
- Test de ciclo completo (cachorro → liberación).

---

## 10. Referencias

- `docs/idea.md` — Documento conceptual original
- `docs/agents.md` — Guía del agente de desarrollo
- `docs/log.md` — Registro histórico de cambios
- TFT_eSPI library: https://github.com/Bodmer/TFT_eSPI
- RV8803 datasheet: https://www.microcrystal.com/en/products/real-time-clock-rtc-modules/rv-8803-c7/
