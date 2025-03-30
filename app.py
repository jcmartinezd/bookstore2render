from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, Libro, TipoTransaccion, Transaccion, Caja
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_clave_secreta_aqui')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tiendalibros.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Decorador para proteger rutas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if (username == 'juan' and password == '2025') or \
           (username == 'maria' and password == '2025'):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Credenciales inválidas')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    libros = Libro.query.all()
    saldo_actual = Caja.query.order_by(Caja.id_movimiento.desc()).first()
    return render_template('index.html', libros=libros, saldo_actual=saldo_actual)

@app.route('/libro/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_libro():
    if request.method == 'POST':
        libro = Libro(
            ISBN=request.form['isbn'],
            titulo=request.form['titulo'],
            precio_compra=float(request.form['precio_compra']),
            precio_venta=float(request.form['precio_venta']),
            cantidad_actual=int(request.form['cantidad'])
        )
        db.session.add(libro)
        db.session.commit()
        flash('Libro agregado exitosamente')
        return redirect(url_for('index'))
    return render_template('nuevo_libro.html')

@app.route('/libro/eliminar/<isbn>')
@login_required
def eliminar_libro(isbn):
    libro = Libro.query.get_or_404(isbn)
    db.session.delete(libro)
    db.session.commit()
    flash('Libro eliminado exitosamente')
    return redirect(url_for('index'))

@app.route('/transaccion/nueva', methods=['GET', 'POST'])
@login_required
def nueva_transaccion():
    if request.method == 'POST':
        libro = Libro.query.get_or_404(request.form['isbn'])
        tipo = int(request.form['tipo'])
        cantidad = int(request.form['cantidad'])
        
        if tipo == 1 and libro.cantidad_actual < cantidad:
            flash('No hay suficientes ejemplares en stock')
            return redirect(url_for('nueva_transaccion'))
        
        transaccion = Transaccion(
            ISBN=libro.ISBN,
            tipo_transaccion=tipo,
            cantidad=cantidad
        )
        db.session.add(transaccion)
        db.session.commit()
        
        flash('Transacción realizada exitosamente')
        return redirect(url_for('index'))
    
    libros = Libro.query.all()
    tipos = TipoTransaccion.query.all()
    return render_template('nueva_transaccion.html', libros=libros, tipos=tipos)

@app.route('/buscar')
@login_required
def buscar():
    query = request.args.get('q', '')
    libros = Libro.query.filter(
        (Libro.titulo.ilike(f'%{query}%')) |
        (Libro.ISBN.ilike(f'%{query}%'))
    ).all()
    return render_template('buscar.html', libros=libros, query=query)

@app.route('/estadisticas')
@login_required
def estadisticas():
    libro_mas_caro = Libro.query.order_by(Libro.precio_venta.desc()).first()
    libro_mas_barato = Libro.query.order_by(Libro.precio_venta.asc()).first()
    
    # Libro más vendido
    mas_vendido = db.session.query(
        Libro,
        db.func.sum(Transaccion.cantidad).label('total_vendidos')
    ).join(Transaccion).filter(
        Transaccion.tipo_transaccion == 1
    ).group_by(Libro.ISBN).order_by(
        db.desc('total_vendidos')
    ).first()
    
    return render_template('estadisticas.html',
                         libro_mas_caro=libro_mas_caro,
                         libro_mas_barato=libro_mas_barato,
                         mas_vendido=mas_vendido)

if __name__ == '__main__':
    app.run(debug=True) 