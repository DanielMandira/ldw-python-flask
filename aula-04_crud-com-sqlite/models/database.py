# Importando a biblioteca SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Instanciando a classe SQLAlchemy
db = SQLAlchemy()

# Criando a classe Game
# Essa classe é uma representação da tabela Game no banco de dados
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    year = db.Column(db.Integer)
    category = db.Column(db.String(100))
    platform = db.Column(db.String(100))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    
    # Metodo construtor da classe
    def __init__(self, title, year, category, platform, price, quantity):
        self.title = title
        self.year = year
        self.category = category
        self.platform = platform
        self.price = price
        self.quantity = quantity
        