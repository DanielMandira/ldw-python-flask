from flask import Flask, render_template
from controllers import routes
# Importando o model
from models.database import db
# Importando a biblioteca OS (comandos de S.O)
import os
import pymysql
# Criando a instância do Flask na variável app
app = Flask(__name__, template_folder='views')  # Representa o nome do arquivo
routes.init_app(app)

# Define o nome do banco
DB_NAME = 'carshow'

app.config['DATABASE_NAME'] = DB_NAME

# Passando o endereço do banco ao SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root@localhost/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret para as flash messages
app.config['SECRET_KEY'] ='thegamesecret'

# Tempo de duração da sessão
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# Iniciar o servidor
if __name__ == '__main__':
    # Conecta ao MySQL para criar o banco de dados (se necessário)
    connection = pymysql.Connect(host='localhost', user='root', password='', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            # Apaga o banco de dados se existir
            cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
            # Cria o banco de dados
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            print("Database recreated successfully")
    except Exception as e:
        print(f"Error managing database: {str(e)}")
    finally:
        connection.close()
    
    # Inicializa o app com o SQLAlchemy
    db.init_app(app=app)
    
    # Cria todas as tabelas
    with app.app_context():
        db.drop_all()  # Remove todas as tabelas existentes
        db.create_all()  # Cria todas as tabelas novamente
        print("Tables recreated successfully")
    
    # Inicia o aplicativo Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
