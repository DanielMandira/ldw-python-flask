from flask import Flask, render_template

##################################################
### Criando instancia do flask na variavel app ###
##################################################
app = Flask(__name__, template_folder='views')

############################################
### Criando a primeira rota da aplicação ###
############################################
@app.route('/')
# View function -> Função que retorna o conteúdo da página
def home():
    return render_template('index.html')

############################
### Iniciando o Servidor ###
############################
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
