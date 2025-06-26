# Top Down Shooter - Proyecto Pygame

## Descripción
Juego hecho en Python con Pygame. Modularizado para trabajo en equipo: cada nivel es un módulo independiente.

**Nuevas características:**
- 🏆 Sistema de puntuación global con MongoDB
- 📊 Top 10 de mejores puntuaciones
- 🥇 Visualización de récords en tiempo real
- 🔐 Autenticación de usuarios con base de datos
- 📈 Sistema de combos y multiplicadores

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
│   ├── mapa/              # Fondos de mapa
│   └── transicionNiveles/ # Fuentes y fondos para transiciones
│
├── core/                  # Lógica principal del juego
│   ├── game.py            # Bucle principal y gestión de niveles
│   └── registry.py        # Registro/login de usuario
│
├── systems/               # Sistemas del juego
│   ├── mongodb_auth.py    # Autenticación con MongoDB
│   └── level_manager.py   # Gestión de niveles y progreso
│
├── entities/              # Clases de los objetos del juego
│   ├── player.py          # Jugador
│   ├── enemy.py           # Enemigo básico
│   ├── enemy2.py          # Enemigo tipo 2
│   ├── enemy3.py          # Enemigo tipo 3
│   ├── boss.py            # Jefe de nivel
│   └── bullet.py          # Balas
│
├── niveles/               # Módulos independientes de cada nivel
│   ├── nivel1.py
│   ├── nivel2.py
│   ├── nivel3.py
│   └── nivel4.py
│
├── screens/               # Pantallas especiales
│   ├── game_over.py       # Pantalla de game over con puntuación
│   ├── login.py           # Pantalla de login con ranking
│   ├── leaderboard.py     # Pantalla de top 10
│   └── level_transition.py
│
├── utils/                 # Utilidades (manejo de spritesheets, etc)
│
├── requirements.txt       # Dependencias del proyecto
├── auth.py                # Sistema de autenticación
├── main.py                # Punto de entrada
├── test_score_system.py   # Script de prueba del sistema de puntuación
└── README.md              # Este archivo
```

---

## Sistema de Puntuación

### Características
- **Puntuación en tiempo real**: Se muestra durante el juego
- **Sistema de combos**: Multiplicador que aumenta con kills rápidos
- **Puntos por enemigo**: 100 puntos base por enemigo eliminado
- **Puntos por nivel**: 500 puntos por completar un nivel
- **Puntos por jefe**: 500 puntos por eliminar un jefe
- **Multiplicador máximo**: 3x para combos

### Visualización
- **En pantalla**: Score actual, nivel, enemigos eliminados, combo
- **Mejor puntuación personal**: Se muestra en tiempo real
- **Récord mundial**: Se muestra en tiempo real
- **Ranking**: Presiona TAB durante el juego para ver el top 10

### Pantallas de puntuación
- **Login**: Botón "Ver Ranking" para ver el top 10
- **Game Over**: Muestra puntuación final, ranking personal y global
- **Victoria**: Muestra puntuación final y opción de ver ranking

---

## Configuración de Base de Datos

### MongoDB Atlas
1. Crea una cuenta en [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Crea un cluster gratuito
3. Obtén tu URI de conexión
4. Crea un archivo `.env` en la raíz del proyecto:

```env
MONGO_URI=mongodb+srv://usuario:contraseña@cluster.mongodb.net/game_db?retryWrites=true&w=majority
```

### Instalación de dependencias
```bash
pip install -r requirements.txt
```

### Probar el sistema
```bash
python test_score_system.py
```

---

## Controles del Juego

### Controles básicos
- **WASD**: Mover jugador
- **Mouse**: Apuntar
- **Click izquierdo**: Disparar
- **ESC**: Salir del juego
- **F11**: Pantalla completa

### Controles de ranking
- **TAB**: Ver ranking durante el juego
- **L**: Ver ranking en pantallas de game over/victoria

### Controles de debug (solo en modo debug)
- **N**: Siguiente nivel
- **P**: Nivel anterior

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

2. Configura MongoDB (ver sección de configuración)

3. Ejecuta:
   ```bash
   python main.py
   ```

---

## Consejos para el equipo
- No borres ni cambies archivos de otros niveles sin avisar.
- Si tienes dudas, consulta el README o pregunta al equipo.
- ¡Diviértete y aprende colaborando!

---

## Características técnicas

### Base de datos
- **MongoDB Atlas**: Base de datos en la nube
- **Colección users**: Almacena usuarios, contraseñas hasheadas, puntuaciones y progreso
- **Índices**: Optimizados para consultas de ranking

### Seguridad
- **Contraseñas hasheadas**: Usando bcrypt
- **Validación de entrada**: Prevención de inyección
- **Conexión segura**: MongoDB Atlas con SSL

### Rendimiento
- **Consultas optimizadas**: Solo obtiene datos necesarios
- **Caché local**: Datos de usuario en memoria durante la sesión
- **Conexión persistente**: Reutiliza conexión a MongoDB 