# RP_Macavei_25

# Dodge & Collect

Controlas un cuadrado **morado** que debe esquivar bloques rojos que caen y recoger monedas amarillas. Cuanto más tiempo sobrevives, más difícil se pone.

## Requisitos

- Python 3.8 o superior
- pygame

## Instalación

```bash
git clone <URL-DEL-REPOSITORIO>
cd RP_Surname1_Surname2_Surname3_25
git checkout Game
pip install pygame
```

## Cómo ejecutarlo

```bash
python game.py
```

## Cómo jugar

| Acción | Tecla |
|---|---|
| Mover | Flechas o W / A / S / D |
| Empezar | Cualquier tecla (pantalla de bienvenida) |
| Jugar de nuevo | R (pantalla final) |
| Salir | ESC |

**Reglas**

- Empiezas con **3 vidas**.
- Chocar con un bloque rojo te quita una vida (tras el golpe tienes un breve periodo de invulnerabilidad).
- Esquivar un bloque: **+1 punto**.
- Recoger una moneda: **+10 puntos**.
- Cada 10 segundos subes de **nivel**: los bloques caen más rápido y aparecen con más frecuencia.
- El juego termina al perder las 3 vidas y se muestra tu puntuación final.

## Estructura del repositorio

```
main
Game  -> game.py, README.md
ROS
```

## Autores

- Ruben Fineas Macavei