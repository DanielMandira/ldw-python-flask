from flask import Flask, render_template
from controllers import routes

# Criando instancia do flask na variavel app 
app = Flask(__name__, template_folder='views')
routes.init_app(app)

# Iniciando o Servidor
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
