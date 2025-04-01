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
DB_NAME = 'thegames'

app.config['DATABASE_NAME'] = DB_NAME

# Passando o endereço do banco ao SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root@localhost/{DB_NAME}"
#app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://root:senha@localhost/{DB_NAME}"
app.config['SQL_TRACK_MODIFICATIONS'] = False

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
            #cria o banco de dados se não existir
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print("Database created")
    except Exception as e:
        print(f"Error creating database: {str(e)}")
    finally:
        connection.close()
    
    db.init_app(app=app)
    with app.test_request_context():
        db.create_all() 
        
    
    # Inicia o aplicativo Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
