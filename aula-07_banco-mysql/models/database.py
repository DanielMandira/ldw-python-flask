from flask_sqlalchemy import SQLAlchemy
# Criando uma instância do SQLAlchemy
db = SQLAlchemy()

# Classe responsável por criar a entidade "Games" no banco com seus atributos
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    year = db.Column(db.Integer)
    category = db.Column(db.String(150))
    platform = db.Column(db.String(150))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    
    # Método construtor da classe
    def __init__(self, title, year, category, platform, price, quantity):
        self.title = title
        self.year = year
        self.category = category
        self.platform = platform
        self.price = price
        self.quantity = quantity

# Classe de usuarios
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # Método construtor da classe
    def __init__(self, email, password):
        self.email = email
        self.password = password
    