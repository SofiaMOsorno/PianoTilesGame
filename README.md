# 🎮 Proyecto Piano Tiles Game

## 👤 Líder del Proyecto
**Nombre del líder:** Sofia Maisha Osorno Aimar

---

## 🧱 Estructura del Proyecto

Este proyecto sigue una arquitectura en capas para mantener una separación clara de responsabilidades:

📁 views/ → Interfaz de usuario y elementos visuales

📁 controllers/ → Lógica del juego y reglas principales 

📁 modelo/ → Acceso a datos, almacenamiento y persistencia


---

## 🌿 Organización de Ramas en Git

Para facilitar el desarrollo colaborativo, se utilizaron ramas por capa o funcionalidad por ejemplo:

- `feature/ui` → Desarrollo de la interfaz de usuario  
- `feature/game-logic` → Implementación de la lógica del juego  
- `feature/data-layer` → Manejo de datos y persistencia

---

## 🔗 Integración de Capas

Las capas se comunican de forma jerárquica:

- La **presentation** interactúa con la **business_logic** para mostrar el estado del juego.
- La **business_logic** consulta o actualiza datos a través de la capa **data**.
- Cada capa está desacoplada para facilitar pruebas y mantenimiento.

---

## ▶️ Cómo Ejecutar el Juego

1. Clona el repositorio:  
   ```bash
   git clone https://github.com/usuario/proyecto-juego.git
   cd proyecto-juego
   pip install
   python main.py


---

## 👥 Contribuidores

A continuación se detalla la participación de cada integrante del equipo según la capa o funcionalidad asignada:

| Nombre                | Rol       | Descripción de Contribución                                         |
|-----------------------|---------------------------|----------------------------------------------------------------------|
| Sofia Osorno    | Líder del proyecto         | Coordinación general, revisión de arquitectura y soporte transversal |
| Luis Arturo            | Programador      | Desarrollo del main          |
| Jaime Contreras          | Programador          | Implementación de reglas del juego y flujo principal                 |
| Aura Gutierrez       | Programador              | Implementación de reglas del juego y flujo principal             |
| Daniel Rodriguez | Documentar     | Escribir la documentación del proyecto                             |

---

