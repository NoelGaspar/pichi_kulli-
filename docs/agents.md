# Pichi-Kulliñ — Agente del proyecto

## Identidad del proyecto

**Pichi-Kulliñ** (mapudungún: "animal pequeño") es un tamagochi educativo que enseña sobre especies nativas endémicas de Chile. El proyecto se divide en dos etapas: simulación en Python/pygame-zero y versión física con ESP32.

## Stack tecnológico

| Etapa | Lenguaje/Plataforma | Librerías clave |
|-------|---------------------|-----------------|
| 1 — Simulación | Python 3 | pygame, pygame-zero |
| 2 — Física | C++ (Arduino Framework) | TFT_eSPI (ST7789), RV8803 RTC, ESP32 |

## Estructura de carpetas

```
pichi-kulli-/
├── docs/            # Documentación técnica
│   ├── idea.md      # Idea original del proyecto
│   ├── agents.md    # Este archivo — guía del agente
│   ├── FSD.md       # Especificación funcional detallada
│   └── log.md       # Historial de cambios
├── stage1/          # Simulador Python
│   ├── main.py      # Punto de entrada
│   ├── game/        # Lógica del juego
│   │   ├── animal.py
│   │   ├── actions.py
│   │   ├── stats.py
│   │   └── time_system.py
│   ├── ui/          # Interfaz de usuario
│   │   ├── screens.py
│   │   ├── hud.py
│   │   └── assets/
│   ├── data/        # Configuración y datos
│   │   └── species.json
│   └── tests/
├── stage2/          # Versión física ESP32
│   └── ...
└── README.md
```

## Convenciones de código

- **Idioma**: Código y comentarios en español (contexto del proyecto). Nombres de variables/funciones en inglés o spanglish consistente.
- **Estilo Python**: PEP8, type hints donde sea útil.
- **Estilo C++**: Convención Arduino (camelCase funciones, PascalCase clases).
- **Modularidad**: Separar lógica (`game/`) de presentación (`ui/`).
- **Compatibilidad**: Diseñar pensando en la migración a ESP32 (respetar resolución 280×240, evitar dependencias pesadas de Python).

## Flujo de trabajo

1. Leer `FSD.md` antes de implementar cualquier módulo.
2. Implementar y validar en `stage1/` primero.
3. Escribir tests unitarios para la lógica de juego (sin dependencia de gráficos).
4. Commits descriptivos en español o inglés con prefijo (`docs:`, `feat:`, `fix:`, `refac:`).
5. Al completar un módulo en stage1, actualizar `log.md`.
6. No pasar a stage2 hasta que stage1 esté completo y validado.

## Reglas para el agente

- Al comenzar una sesión, leer `agents.md`, `FSD.md` y `log.md` para contextualizarse.
- Priorizar legibilidad y modularidad sobre optimización prematura.
- Mantener consistencia con la nomenclatura de especies y variables del `idea.md`.
- Trabajar de a un módulo por vez, reportando avances en `log.md`.
