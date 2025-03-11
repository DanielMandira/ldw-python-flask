from flask import render_template, request, redirect, url_for
# Importando a classe Game do arquivo database.py
from models.database import db, Game
#Essa biblioteca é responsável por ler uma determinada URL e retornar o conteúdo da página
import urllib
# Connverte dados em json
import json
# Criando a primeira rota da aplicação #
players = []
gameList = [{"title": 'CS-GO', "year": 2012, "category": 'FPS'}, 
            {"title": 'LOL', "year": 2009, "category": 'MOBA'}, 
            {"title": 'Valorant', "year": 2020, "category": 'FPS'}]


def init_app(app):

    @app.route('/')
    # View function -> Função que retorna o conteúdo da página
    def home():
        return render_template('index.html')

    @app.route('/games', methods=['GET', 'POST'])
    def games():
        if request.method == 'POST':
            if request.form.get('player'):
                players.append(request.form.get('player'))
                return redirect(url_for('games'))
        return render_template('games.html',  gameList=gameList, players=players)

    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            gameList.append(form_data)
            return redirect(url_for('cadgames'))
        return render_template('cadgames.html', gameList=gameList)
    
    
    @app.route('/apigames', methods=['GET', 'POST'])
    # Passando parametros para a rota
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    # Definindo que o parametro é opcional
    def apigames(id=None):
        url = 'https://www.freetogame.com/api/games'
        response = urllib.request.urlopen(url)
        data = response.read()
        gamesjson = json.loads(data)
        if id:
            ginfo = []
            for g in gamesjson:
                if g['id'] == id:
                    ginfo=g
                    break
            if ginfo:
                return render_template('gameinfo.html', ginfo=ginfo)
            else:
                return 'Game not found'
        return render_template('apigames.html', gamesjson=gamesjson)

    @app.route('/estoque', methods=['GET', 'POST'])
    def estoque():
        # Método do SQLAlchemy que retorna todos os registros da tabela Game
        gamesEstoque = Game.query.all()
        return render_template('estoque.html', gamesEstoque=gamesEstoque)