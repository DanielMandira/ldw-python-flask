from flask import Flask, render_template
from controllers import routes
from models.database import db
import os

# Criando instancia do flask na variavel app 
app = Flask(__name__, template_folder='views')
routes.init_app(app)

# permite ler o diretório absoluto do arquivo
dir = os.path.abspath(os.path.dirname(__file__))

# Passar o diretório do banco de dados ao SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/games.sqlite3')

# Iniciando o Servidor
if __name__ == '__main__':
    # Inicializando o banco de dados
    db.init_app(app=app)
    # Cria o banco de dados se não existir
    with app.test_request_context():
        db.create_all()
    app.run(host='localhost', port=5000, debug=True)
