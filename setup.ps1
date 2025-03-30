# Crear directorios necesarios
$directories = @(
    "instance",
    "templates",
    "static",
    "static/css",
    "static/js"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir
        Write-Host "Directorio creado: $dir"
    }
}

# Crear entorno virtual
python -m venv venv
Write-Host "Entorno virtual creado"

# Activar entorno virtual
.\venv\Scripts\Activate.ps1
Write-Host "Entorno virtual activado"

# Instalar dependencias
pip install -r requirements.txt
Write-Host "Dependencias instaladas"

# Inicializar la base de datos
python init_db.py
Write-Host "Base de datos inicializada"

Write-Host "Configuración completada exitosamente" 