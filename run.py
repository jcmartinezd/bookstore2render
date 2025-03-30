import os
import socket
import uvicorn
from app import app
from init_db import init_db

def find_available_port(start_port=8000, max_port=8999):
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                return port
            except OSError:
                continue
    raise RuntimeError('No se encontró un puerto disponible')

def main():
    # Crear directorio instance si no existe
    if not os.path.exists('instance'):
        os.makedirs('instance')
    
    # Inicializar la base de datos
    init_db()
    
    # Encontrar puerto disponible para la API
    api_port = find_available_port()
    
    # Iniciar la API FastAPI en un proceso separado
    uvicorn.run('api:api', host='0.0.0.0', port=api_port, reload=True)
    
    # Iniciar la aplicación Flask
    app.run(debug=True, port=5000)

if __name__ == '__main__':
    main() 