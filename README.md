# 🎮 Proyecto [Piano Tiles Game]

## 👤 Líder del Proyecto
**Nombre del líder:** Sofia Maisha Osorno Aimar

---

## 🧱 Estructura del Proyecto

Este proyecto sigue una arquitectura en capas para mantener una separación clara de responsabilidades:

📁 presentation/ → Interfaz de usuario y elementos visuales

📁 business_logic/ → Lógica del juego y reglas principales 

📁 data/ → Acceso a datos, almacenamiento y persistencia


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


---

## 👥 Contribuidores

A continuación se detalla la participación de cada integrante del equipo según la capa o funcionalidad asignada:

| Nombre                | Rol / Capa Asignada       | Descripción de Contribución                                         |
|-----------------------|---------------------------|----------------------------------------------------------------------|
| [Nombre del líder]    | Líder del proyecto         | Coordinación general, revisión de arquitectura y soporte transversal |
| [Nombre 1]            | Capa de presentación       | Desarrollo de la interfaz de usuario y experiencia visual            |
| [Nombre 2]            | Lógica de negocio          | Implementación de reglas del juego y flujo principal                 |
| [Nombre 3]            | Capa de datos              | Gestión de almacenamiento, persistencia y acceso a datos             |
| [Nombre 4] *(opcional)* | QA / Testing / Soporte     | Pruebas, documentación y soporte técnico                             |

---

