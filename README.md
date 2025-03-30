# Tienda de Libros

Sistema de gestión para una tienda de libros desarrollado con Flask y FastAPI.

## Características

- Gestión de catálogo de libros
- Control de inventario
- Registro de transacciones (ventas y abastecimientos)
- Control de caja
- Estadísticas de ventas
- API REST documentada
- Interfaz web moderna con Bootstrap
- Autenticación de usuarios

## Requisitos

- Python 3.8 o superior
- Windows 11
- PowerShell

## Instalación

1. Clonar el repositorio:
```powershell
git clone <url-del-repositorio>
cd tiendalibros
```

2. Ejecutar el script de configuración:
```powershell
.\setup.ps1
```

Este script:
- Crea los directorios necesarios
- Configura un entorno virtual
- Instala las dependencias
- Inicializa la base de datos

## Uso

1. Iniciar la aplicación:
```powershell
python run.py
```

2. Acceder a la aplicación web:
- Abrir el navegador y visitar `http://localhost:5000`
- Iniciar sesión con las credenciales:
  - Usuario: juan
  - Contraseña: 2025
  - O
  - Usuario: maria
  - Contraseña: 2025

3. Acceder a la API:
- La documentación de la API está disponible en `http://localhost:8000/docs`
- Usar las mismas credenciales para autenticación

## Funcionalidades

### Gestión de Libros
- Agregar nuevos libros al catálogo
- Eliminar libros
- Buscar libros por título o ISBN
- Ver detalles de libros

### Transacciones
- Registrar ventas
- Registrar abastecimientos
- Ver historial de transacciones

### Control de Caja
- Ver saldo actual
- Seguimiento de ingresos y egresos

### Estadísticas
- Libro más costoso
- Libro menos costoso
- Libro más vendido
- Resumen de inventario

## Estructura del Proyecto

```
tiendalibros/
├── app.py              # Aplicación Flask principal
├── api.py              # API FastAPI
├── models.py           # Modelos de datos
├── init_db.py          # Inicialización de la base de datos
├── run.py             # Script de inicio
├── setup.ps1          # Script de configuración
├── requirements.txt   # Dependencias
├── instance/          # Base de datos SQLite
├── static/           # Archivos estáticos
│   ├── css/
│   └── js/
└── templates/        # Plantillas HTML
```

## Desarrollo

### Modificar la Base de Datos
1. Editar `models.py` para modificar los modelos
2. Eliminar la base de datos en `instance/tiendalibros.db`
3. Ejecutar `python init_db.py`

### Agregar Nuevas Funcionalidades
1. Crear nuevas rutas en `app.py` o `api.py`
2. Crear plantillas HTML en `templates/`
3. Agregar estilos en `static/css/style.css`
4. Agregar JavaScript en `static/js/main.js`

## Solución de Problemas

### Error de Permisos en PowerShell
Si hay problemas de permisos al ejecutar scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Puerto en Uso
Si el puerto 5000 o 8000 está en uso, la aplicación buscará automáticamente un puerto disponible.

### Base de Datos
Si hay problemas con la base de datos:
1. Detener la aplicación
2. Eliminar `instance/tiendalibros.db`
3. Ejecutar `python init_db.py`
4. Reiniciar la aplicación

## Contribuir

1. Fork el repositorio
2. Crear una rama para la característica
3. Hacer commit de los cambios
4. Push a la rama
5. Crear un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. 