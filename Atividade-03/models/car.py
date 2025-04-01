from models.database import db

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.String(4), nullable=False)
    descricao = db.Column(db.Text)
    potencia = db.Column(db.Integer)
    categoria = db.Column(db.String(20), nullable=False)
    foto = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Car {self.marca} {self.modelo} {self.ano}>'
