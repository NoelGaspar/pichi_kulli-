#Pichi-Kulliñ

Este proyecto consiste en la creación de un tamagoshi. La particularidad central de este tamagoshi recae en que es una versión nacional que tiene por objetivo enseñar sobre las especies nativas endemicas de Chile.

--
## Hardware
Este tamagoshi esta compuesto en hardware por una ESP32+Patanalla TFT de 280x240 basada en st7789+ RTC RV8803+Módulo de batería Lipo + Buzzer parlante.

--
## Etapas
Para la realización del proyecto se van a abordar por medio de etapas de desarrollo.
- Primera etapa: Simulación y validación del juego. Esta etapa consiste en diseñar el juego y validar la aplicación y funcionalidad por medio de una simulación realizada en Python /pyGameZero  y python/pyGame. Una vez completada la estructura general del juego este pasará a ser adaptado para la versión física. La idea de esta etapa es diseñar contemplando las limitaciones de la versión físca, para que la migración sea sencilla. considerar correctos tamaños de resolución y trabajar con estructuras modulares de alto nivel que puedan llevarse posteriormente a un código de Arduino.

- Segunda etapa: Versión física. Consiste en adaptar los códigos de la etapa 1 a la versión física, realizar las correcciones y calibraciones necesarias, para garantizar fluidez y robustez de la app general.

--
## Descripcion del juego

### Clases de animales elegibles

 - Gato Güiña
 - Chungungo
 - Ranita de darwin
 - Zorro chilote

### Etapas de vida

 - Cachorro
 - Joven
 - Adulto
 - Liberar

### Variables de juego

| Variable  | Rango |
| --------- | ----- |
| Hambre    | 0-100 |
| Energía   | 0-100 |
| Felicidad | 0-100 |
| Higiene   | 0-100 |
| Salud     | 0-100 |

### Acciones

 - Alimentar: {"hambre":-20, "felicidad":5}
 - Jugar : {"felicidad":15, "energía":-10,"hambre":5}
 - Dormir: {"energía":30, "felicidad":5, "hambre":5}
 - Limpiar: {"higene":20, "felicidad":5}
 - Curar: {"salud": 20}
 - Liberar: Reinicio del juego

### Reglas de tiempo

1 minuto real  = 10 min de juego.

| Variable  | Rango | Tiempo disminución | Disminución | Notas |
| --------- | ----- | ----- | ----- | ----- |
| Hambre    | 0-100 | 10 min de juego | 4 puntos | si llega a 90 o más comienza a afectar la Salud |
| Energía   | 0-100 | 15 min de juego | -5 puntos | si llega a 0 no podrá jugar |
| Felicidad | 0-100 | 20 min de juego | -5 puntos | si llega a 0 se vuelve triste|
| Higiene   | 0-100 | 20 min de juego | -5 puntos | Si llega a 10 o menos puede enfermar |
| Salud     | 0-100 | - | - | No disminuye sola. Solo si las otras estan muy mal|

### Efectos por nieveles críticos

- Hambre >= 90  -2 Salud cada 10 min de juego
- Higene <= 20  -2 Salud cada 10 min de juego
- Energía = 0  -1 Salud cada 10 minuto
- Felicidad = 0  se vuelve triste. ( todas las otras necesidades aumentan en 2 puntos su efecto)

Estado Triste: Todas las necesidades aumentan su efecto en 2 puntos.

### Condición de fin.

El juego puede terminar solo por dos razones. En caso de cuidar muy mal a nuestro animal y llegar a Salud = 0. El Juego se reinicia. Pero antes muestra un final que ayude a reflexionar sobre el cuidado de los animales. y muestre que un equipo de profesionales se hará cargo del animal.

El segundo caso es que cumpliendose las condiciones de Liberación aparece un indicador de que esta listo para ser liberado y entonces puedes usar la accion de liberar. En este caso el final muestra al equipo de especialistas devolviendo al animal a su entorno natural junto a más miembros de su especie. posteriormente el juego pasa a los agradecimientos para volver a iniciar.

- Salud = 0. El personaje es rescatado por especialistas. y debe volver a empezar el juego

- Estado de crecimiento Adulto, salud = 100 y tiempo > 5 días de juego. El animal puede ser liberado y devuelto a la naturaleza.

### Etapas de crecimiento

- Cachorro a juvenil:  1 día de juego
- Juvenil a adulto: 3 días de juego (desde que es joven)
- Adulto a listo para liberar: 5 días de juego en total (desde que inició el juego).



### narrativa de juego

"Eres cuidador de un centro de rehabilitación de fauna nativa. Tu misión es ayudar a una cría rescatada a crecer sana hasta que pueda volver a su hábitat natural."
