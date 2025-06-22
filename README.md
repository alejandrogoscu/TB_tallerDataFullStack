# 🧠 Colaboración Full Stack & Data Science

Este documento resume brevemente la colaboración entre los perfiles de **Data Science** y **Full Stack Development** en un proyecto conjunto. Se detallan tareas, herramientas utilizadas, ventajas de ciertos enfoques y organización del equipo.

---

## 1. ¿Qué hace un Data Scientist?

El equipo de Data Science se encargó de:

- Obtener y limpiar los datos.
- Seleccionar únicamente las columnas relevantes para el ejercicio.
- Montar y levantar la base de datos para que el equipo de desarrollo pudiera conectarse a ella.

Gracias a ese trabajo previo, el equipo de Full Stack pudo:

- Programar las consultas necesarias.
- Desarrollar los endpoints que posteriormente serían consumidos desde el front.

---

## 2. ¿Qué ventajas tiene hacer un front en JavaScript vs Python (y viceversa)?

**JavaScript (React, etc.):**

- ✅ Mayor control visual sobre la interfaz.
- ✅ Permite una experiencia de usuario más personalizada e interactiva.
- ❌ Requiere más configuración y conocimientos específicos.

**Python (con Streamlit):**

- ✅ Desarrollo más rápido e inmediato.
- ✅ Ideal para mostrar datos de forma rápida y sencilla.
- ❌ Menor control sobre el diseño y la interacción del usuario.

---

## 3. ¿Ventajas e inconvenientes de usar Streamlit como front?

**Ventajas:**

- Fácil y rápido de implementar.
- Ideal para dashboards y visualización de datos.
- No requiere conocimientos profundos de frontend.

**Inconvenientes:**

- Poca personalización visual.
- Menor control sobre la experiencia de usuario.
- Limitado para aplicaciones complejas o altamente interactivas.

---

## 4. ¿Cómo de importante es la comunicación?

**La comunicación es clave.**  
El trabajo de un equipo afecta directamente al otro. Si no hay comunicación constante entre Data Science y Full Stack, el flujo de trabajo se ve afectado y surgen bloqueos innecesarios.

---

## 5. ¿Cómo nos organizamos para paralelizar tareas?

Mientras el equipo de Data Science:

- Obtenía, limpiaba y cargaba la base de datos,

El equipo de Full Stack:

- Montaba el repositorio.
- Instalaba dependencias y configuraba el proyecto.
- Preparaba la conexión con la base de datos.
- Definía los modelos y tipos de datos.
- Comenzaba a implementar los endpoints en JS.

Al mismo tiempo, el equipo de Data Science ya podía trabajar en su parte con Streamlit utilizando los endpoints desarrollados.

https://tb-tallerdatafullstack.onrender.com
