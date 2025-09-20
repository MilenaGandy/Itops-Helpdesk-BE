# Itops HelpDesk Backend

Este proyecto es un backend para un sistema de HelpDesk desarrollado con Django y Django REST Framework.

## Estructura del Proyecto

- `src/core/`: Contiene la configuración principal del proyecto Django (settings, urls, wsgi, asgi).
- `src/helpdesk/`: Aplicación principal donde se encuentran los modelos, vistas, serializadores y rutas relacionadas con la gestión de tickets de soporte.

## Funcionalidades Implementadas

- **Modelos**: Definición de modelos para la gestión de tickets de soporte.
- **Serializadores**: Serialización de los modelos para exponerlos a través de la API REST.
- **Vistas**: Lógica de negocio y endpoints para la gestión de tickets.
- **Rutas**: Configuración de URLs para acceder a los diferentes endpoints de la API.
- **Admin**: Registro de modelos en el panel de administración de Django.

## Instalación y Ejecución

1. Clona el repositorio.
2. Instala las dependencias necesarias (Django, djangorestframework, etc.).
3. Ejecuta las migraciones:
   ```bash
   python src/manage.py migrate
   ```
4. Inicia el servidor de desarrollo:
   ```bash
   python src/manage.py runserver
   ```

## Pruebas

Las pruebas se encuentran en `src/helpdesk/tests.py`.

## Notas

- El proyecto está estructurado para facilitar la escalabilidad y el mantenimiento.
- Se recomienda crear un entorno virtual para la instalación de dependencias.

---

