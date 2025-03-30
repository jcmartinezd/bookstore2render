from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import secrets
from models import db, Libro, TipoTransaccion, Transaccion, Caja
from app import app

api = FastAPI(title="API de Tienda de Libros")

# Configurar CORS
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Autenticación básica
security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "juan")
    correct_password = secrets.compare_digest(credentials.password, "2025")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Modelos Pydantic
class LibroBase(BaseModel):
    ISBN: str
    titulo: str
    precio_compra: float
    precio_venta: float
    cantidad_actual: int

class TransaccionBase(BaseModel):
    ISBN: str
    tipo_transaccion: int
    cantidad: int

# Rutas de la API
@api.get("/libros", response_model=List[LibroBase])
async def obtener_libros(current_user: str = Depends(get_current_user)):
    with app.app_context():
        libros = Libro.query.all()
        return libros

@api.get("/libros/{isbn}", response_model=LibroBase)
async def obtener_libro(isbn: str, current_user: str = Depends(get_current_user)):
    with app.app_context():
        libro = Libro.query.get(isbn)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return libro

@api.post("/libros", response_model=LibroBase)
async def crear_libro(libro: LibroBase, current_user: str = Depends(get_current_user)):
    with app.app_context():
        db_libro = Libro(**libro.dict())
        db.session.add(db_libro)
        db.session.commit()
        return db_libro

@api.delete("/libros/{isbn}")
async def eliminar_libro(isbn: str, current_user: str = Depends(get_current_user)):
    with app.app_context():
        libro = Libro.query.get(isbn)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        db.session.delete(libro)
        db.session.commit()
        return {"message": "Libro eliminado exitosamente"}

@api.post("/transacciones", response_model=TransaccionBase)
async def crear_transaccion(transaccion: TransaccionBase, current_user: str = Depends(get_current_user)):
    with app.app_context():
        libro = Libro.query.get(transaccion.ISBN)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        
        if transaccion.tipo_transaccion == 1 and libro.cantidad_actual < transaccion.cantidad:
            raise HTTPException(status_code=400, detail="No hay suficientes ejemplares en stock")
        
        db_transaccion = Transaccion(**transaccion.dict())
        db.session.add(db_transaccion)
        db.session.commit()
        return db_transaccion

@api.get("/estadisticas/libro-mas-caro")
async def libro_mas_caro(current_user: str = Depends(get_current_user)):
    with app.app_context():
        libro = Libro.query.order_by(Libro.precio_venta.desc()).first()
        if not libro:
            raise HTTPException(status_code=404, detail="No hay libros en el catálogo")
        return libro

@api.get("/estadisticas/libro-mas-barato")
async def libro_mas_barato(current_user: str = Depends(get_current_user)):
    with app.app_context():
        libro = Libro.query.order_by(Libro.precio_venta.asc()).first()
        if not libro:
            raise HTTPException(status_code=404, detail="No hay libros en el catálogo")
        return libro

@api.get("/estadisticas/libro-mas-vendido")
async def libro_mas_vendido(current_user: str = Depends(get_current_user)):
    with app.app_context():
        mas_vendido = db.session.query(
            Libro,
            db.func.sum(Transaccion.cantidad).label('total_vendidos')
        ).join(Transaccion).filter(
            Transaccion.tipo_transaccion == 1
        ).group_by(Libro.ISBN).order_by(
            db.desc('total_vendidos')
        ).first()
        
        if not mas_vendido:
            raise HTTPException(status_code=404, detail="No hay ventas registradas")
        return {
            "libro": mas_vendido[0],
            "total_vendidos": mas_vendido[1]
        }

@api.get("/caja/saldo")
async def obtener_saldo(current_user: str = Depends(get_current_user)):
    with app.app_context():
        saldo = Caja.query.order_by(Caja.id_movimiento.desc()).first()
        if not saldo:
            raise HTTPException(status_code=404, detail="No hay movimientos en caja")
        return {"saldo_actual": saldo.saldo_actual} 