from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/flask-mysqlalchemy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db= SQLAlchemy(app)
ma= Marshmallow(app)

class Categoria(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50), unique=True)

    def __init__(self,nombre):
        self.nombre= nombre

class Articulo(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50), unique=True)
    precio=db.Column(db.Float)
    iva=db.Column(db.Float)
    description=db.Column(db.String(100))
    stock=db.Column(db.Integer)
    id_categorias = db.Column(db.Integer, db.ForeignKey(Categoria.id))

    def __init__(self,nombre,precio,iva,description,stock,id_categorias):
        self.nombre=nombre
        self.precio=precio
        self.iva=iva
        self.description=description
        self.stock=stock
        self.id_categorias=id_categorias

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    nombre = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    admin = db.Column(db.Integer)

    def __init__(self,username,password,nombre,email,admin):
        self.username=username
        self.password=password
        self.nombre=nombre
        self.email=email
        self.admin=admin

class Carrito(db.Model):
    id_articulos = db.Column(db.Integer, db.ForeignKey(Articulo.id), primary_key=True)
    id_usuarios = db.Column(db.Integer, db.ForeignKey(Usuario.id), primary_key=True)
    cantidad = db.Column(db.Integer)

    def __init__(self,id_articulos,id_usuarios,cantidad):
        self.id_articulos=id_articulos
        self.id_usuarios=id_usuarios
        self.cantidad=cantidad

db.create_all()

class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('id','nombre')
categoria_schema=CategoriaSchema(many=True)

class ArticuloSchema(ma.Schema):
    class Meta:
        fields = ('id','nombre','precio','iva','description','stock','id_categorias')
articulo_schema=ArticuloSchema(many=True)


class CarritoSchema(ma.Schema):
    class Meta:
        fields=('id_articulos','id_usuarios','cantidad')
carrito_schema= CarritoSchema(many=True)

class UsuariosSchema(ma.Schema):
    class Meta:
        fields=('id','username','password','nombre','email','admin')
usuario_schema=UsuariosSchema(many=True)


@app.route('/categoria', methods=['POST'])
def post_categoria():
    nombre= request.json['nombre']
    new_categoria=Categoria(nombre)
    db.session.add(new_categoria)
    db.session.commit()
    return 'OK'
@app.route('/categoria', methods=['GET'])
def get_categoria():
    all_categorias=Categoria.query.all()
    result=categoria_schema.dump(all_categorias)
    return jsonify(result)

@app.route('/articulo', methods=['POST'])
def post_articulo():
    nombre= request.json['nombre']
    precio= request.json['precio']
    iva= request.json['iva']
    description= request.json['description']
    stock= request.json['stock']
    id_categorias= request.json['id_categorias']
    new_articulo=Articulo(nombre,precio,iva,description,stock,id_categorias)
    db.session.add(new_articulo)
    db.session.commit()
    return 'OK'
@app.route('/articulo', methods=['GET'])
def get_articulo():
    articulos_all=Articulo.query.all()
    result=articulo_schema.dump(articulos_all)
    return jsonify(result)

@app.route('/usuario', methods=['POST'])
def post_usuario():
    username= request.json['username']
    password= request.json['password']
    nombre= request.json['nombre']
    email= request.json['email']
    admin= request.json['admin']
    new=Usuario(username,password,nombre,email,admin)
    db.session.add(new)
    db.session.commit()
    return 'OK'
@app.route('/usuario', methods=['GET'])
def get_usuario():
    usuario_all=Usuario.query.all()
    result=usuario_schema.dump(usuario_all)
    return jsonify(result)

@app.route('/carrito', methods=['POST'])
def post_carrito():
    id_articulos= request.json['id_articulos']
    id_usuarios= request.json['id_usuarios']
    cantidad= request.json['cantidad']
    new=Carrito(id_articulos,id_usuarios,cantidad)
    db.session.add(new)
    db.session.commit()
    return 'OK'
@app.route('/carrito', methods=['GET'])
def get_carrito():
    carrito_all=Carrito.query.all()
    result=carrito_schema.dump(carrito_all)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)