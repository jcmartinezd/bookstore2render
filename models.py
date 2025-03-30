from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Libro(db.Model):
    __tablename__ = 'Libros'
    
    ISBN = db.Column(db.String(13), primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    precio_compra = db.Column(db.Numeric(10, 2), nullable=False)
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False)
    cantidad_actual = db.Column(db.Integer, nullable=False, default=0)
    
    transacciones = db.relationship('Transaccion', backref='libro', lazy=True)

class TipoTransaccion(db.Model):
    __tablename__ = 'TiposTransaccion'
    
    id_tipo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)

class Transaccion(db.Model):
    __tablename__ = 'Transacciones'
    
    id_transaccion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ISBN = db.Column(db.String(13), db.ForeignKey('Libros.ISBN', ondelete='CASCADE'), nullable=False)
    tipo_transaccion = db.Column(db.Integer, db.ForeignKey('TiposTransaccion.id_tipo'), nullable=False)
    fecha_transaccion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cantidad = db.Column(db.Integer, nullable=False)
    
    caja = db.relationship('Caja', backref='transaccion', uselist=False)

class Caja(db.Model):
    __tablename__ = 'Caja'
    
    id_movimiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha_movimiento = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tipo_movimiento = db.Column(db.String(20), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    saldo_actual = db.Column(db.Numeric(10, 2), nullable=False)
    id_transaccion = db.Column(db.Integer, db.ForeignKey('Transacciones.id_transaccion')) 