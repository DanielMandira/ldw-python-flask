from flask import render_template, request, redirect, url_for
# Criando a primeira rota da aplicação #
players = []
gameList = [{"title": 'CS-GO', "year": 2012, "category": 'FPS'}]


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
