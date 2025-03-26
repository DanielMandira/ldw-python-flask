from flask import Flask
from models.database import db
from controllers.routes import init_routes
import os

def create_app():
    app = Flask(__name__, template_folder='views')
    
    # Configurações
    app.config.from_pyfile('config.py')
    
    # Banco de Dados
    db.init_app(app)
    
    # Rotas
    init_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)