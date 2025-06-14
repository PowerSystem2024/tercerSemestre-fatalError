# Top Down Shooter - Proyecto Pygame

## Descripción
Juego hecho en Python con Pygame. Modularizado para trabajo en equipo: cada nivel es un módulo independiente.

---

## Estructura del Proyecto

```
Juego/
│
├── assets/                # Imágenes y recursos gráficos
│   ├── jugador/           # Sprites y plist del jugador
│   ├── enemigos/          # Sprites y plist de enemigos
│   ├── muerte/            # Efectos de muerte (sangre)
│   ├── cursor/            # Imagen personalizada del cursor
│   └── mapa/              # Fondos de mapa
│
├── core/                  # Lógica principal del juego
│   ├── game.py            # Bucle principal y gestión de niveles
│   └── registry.py        # Registro/login de usuario
│
├── db/                    # Simulación de base de datos de usuarios
│   └── users.json         # Usuarios registrados (IGNORADO en git)
│
├── entities/              # Clases de los objetos del juego
│   ├── player.py          # Jugador
│   ├── enemy.py           # Enemigo básico
│   └── bullet.py          # Balas
│
├── niveles/               # Módulos independientes de cada nivel
│   ├── nivel1.py
│   ├── nivel2.py
│   ├── nivel3.py
│   └── nivel4.py
│
├── screens/               # Pantallas especiales
│   ├── game_over.py
│   ├── login.py
│   └── level_transition.py
│
├── utils/                 # Utilidades (manejo de spritesheets, etc)
│
├── requirements.txt       # Dependencias del proyecto
├── main.py                # Punto de entrada
└── README.md              # Este archivo
```

---

## ¿Cómo colaborar?

- **Cada compañero trabaja SOLO en su archivo de nivel** (por ejemplo, `niveles/nivel2.py`).
- Si necesitas nuevos enemigos, crea la clase en `entities/` y úsala en tu nivel.
- Si necesitas nuevos assets, agrégalos en `assets/`.
- Si necesitas cambiar algo global (jugador, balas, etc.), ¡habla con el equipo antes!
- Haz `pull` antes de empezar y `push` después de cada cambio.

---

## Ejemplo: ¿Qué puedes hacer en tu nivel?

- Cambiar la cantidad y tipo de enemigos:
  ```python
  from entities.enemy import Enemy
  def cargar_nivel(game):
      game.enemies = []
      for _ in range(10):
          game.enemies.append(Enemy(game.level, game.MAP_SIZE))
  ```
- Agregar enemigos especiales:
  ```python
  from entities.enemy_shooter import EnemyShooter
  def cargar_nivel(game):
      ...
      game.enemies.append(EnemyShooter(game.level, game.MAP_SIZE))
  ```
- Agregar drops, obstáculos, efectos visuales, reglas propias, etc.

---

## ¿Cómo correr el juego?

1. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta:
   ```bash
   python main.py
   ```

---

## Consejos para el equipo
- No borres ni cambies archivos de otros niveles sin avisar.
- Si tienes dudas, consulta el README o pregunta al equipo.
- ¡Diviértete y aprende colaborando! 