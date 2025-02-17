from flask import render_template, request
# Criando a primeira rota da aplicação #
players = []


def init_app(app):

    @app.route('/')
    # View function -> Função que retorna o conteúdo da página
    def home():
        return render_template('index.html')

    @app.route('/games', methods=['GET', 'POST'])
    def games():
        game = {"title": 'CS-GO', "year": 2012, "category": 'FPS'}
        if request.method == 'POST':
            if request.form.get('player'):
                players.append(request.form.get('player'))
        return render_template('games.html',  game=game, players=players)
