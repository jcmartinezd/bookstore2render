import os
from app import app, db
from models import Libro, TipoTransaccion, Transaccion, Caja

def init_db():
    # Crear directorio instance si no existe
    if not os.path.exists('instance'):
        os.makedirs('instance')
    
    # Crear todas las tablas
    with app.app_context():
        db.create_all()
        
        # Insertar tipos de transacciones si no existen
        if not TipoTransaccion.query.first():
            venta = TipoTransaccion(id_tipo=1, nombre='VENTA')
            abastecimiento = TipoTransaccion(id_tipo=2, nombre='ABASTECIMIENTO')
            db.session.add(venta)
            db.session.add(abastecimiento)
            db.session.commit()
        
        # Insertar saldo inicial en caja si no existe
        if not Caja.query.first():
            saldo_inicial = Caja(
                tipo_movimiento='INGRESO',
                monto=1000000.00,
                saldo_actual=1000000.00
            )
            db.session.add(saldo_inicial)
            db.session.commit()
        
        print("Base de datos inicializada correctamente")

if __name__ == '__main__':
    init_db() 