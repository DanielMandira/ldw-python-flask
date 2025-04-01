from flask import render_template, request, redirect, url_for, flash, session
# Importando o Model
from models.database import db, Game, User
# Essa biblioteca serve para ler uma determinada URL
import urllib
# Converte dados para o formato json
import json
from werkzeug.security import generate_password_hash, check_password_hash
# Biblioteca para editar a flash message
from markupsafe import Markup # Inclui HTML dentro das Flash Message


jogadores = []

gamelist = [{'title': 'CS-GO',
             'year': 2012,
             'category': 'FPS Online'}]


def init_app(app):
    # Função de middleware para verificar a autenticação do usuario
    @app.before_request
    def check_auth():
        routes = ['login', 'caduser', 'home']
        if request.endpoint in routes or request.path.startswith('/static/'):
            return
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
    @app.route('/')
    # View function -> função de visualização
    def home():
        return render_template('index.html')

    @app.route('/games', methods=['GET', 'POST'])
    def games():
        game = gamelist[0]
        if request.method == 'POST':
            if request.form.get('jogador'):
                jogadores.append(request.form.get('jogador'))
                return redirect(url_for('games'))

        return render_template('games.html',
                               game=game,
                               jogadores=jogadores)

    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            gamelist.append(form_data)
            return (redirect(url_for('cadgames')))
        return render_template('cadgames.html', gamelist=gamelist)

    @app.route('/apigames', methods=['GET', 'POST'])
    # Passando parâmetros para a rota
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    # Definindo que o parâmetro é opcional
    def apigames(id=None):
        url = 'https://www.freetogame.com/api/games'
        res = urllib.request.urlopen(url)
        # print(res)
        data = res.read()
        gamesjson = json.loads(data)

        if id:
            ginfo = []
            for g in gamesjson:
                if g['id'] == id:
                    ginfo = g
                    break
            if ginfo:
                return render_template('gameinfo.html', ginfo=ginfo)
            else:
                return f'Game com a ID {id} não foi encontrado.'

        return render_template('apigames.html',
                               gamesjson=gamesjson)

    # ROTA COM O CRUD DE JOGOS
    @app.route('/estoque', methods=['GET', 'POST'])
    @app.route('/estoque/delete/<int:id>')
    def estoque(id=None):
        if id:
            # Selecionando o jogo no banco para ser excluído
            game = Game.query.get(id)
            # Deletar o game pea ID
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque'))
            
        if request.method == 'POST':
            # Cadastra um novo jogo
            newgame = Game(request.form['title'], request.form['year'], request.form['category'], request.form['platform'], request.form['price'], request.form['quantity'])
            # Envia os valores para o banco
            db.session.add(newgame)
            db.session.commit()
            return redirect(url_for('estoque'))
        
        else:
            # PAGINAÇÃO
            # A variável abaixo captura o valor de 'page' que foi passado pelo método GET. E define como padrão o valor 1 e o tipo inteiro
            page = request.args.get('page', 1, type=int)
            # Valor padrão de registros por página (definimos 5)
            per_page = 5
            # Abaixo está sendo feito um SELECT no banco a partir da página informada (page) e filtrando os registro de 5 em 5 (per_page)
            games_page = Game.query.paginate(page=page, per_page=per_page)
            return render_template('estoque.html', gamesestoque=games_page)
            # Método do SQLAlchemy que faz um select geral no banco na tabela Games
            # gamesestoque = Game.query.all()
            # return render_template('estoque.html', gamesestoque=gamesestoque)
    
    # ROTA DE EDIÇÃO
    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit(id):
        # Buscando informações do jogo:
        game = Game.query.get(id)
        # Edita o jogo com as informações do formulário
        if request.method == 'POST':
            game.title = request.form['title']
            game.year = request.form['year']
            game.category = request.form['category']
            game.platform = request.form['platform']
            game.price = request.form['price']
            game.quantity = request.form['quantity']
            db.session.commit()
            return redirect(url_for('estoque'))
        return render_template('editgame.html', game=game)

    # Rota de login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            # Verificando se o usuario existe
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['user_email'] = user.email
                nickName = user.email.split('@')[0]
                session['nickName'] = nickName
                flash(f'Login realizado com sucesso. Bem-vindo, {nickName}!','success')
                return redirect(url_for('home'))
            else:
                msg = Markup("<p>Usuário ou senha inválidos. <a href='/login'>Tente novamente!</a></p>")
                flash(msg,'danger')
        return render_template('login.html')
    
    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        session.clear()
        flash('Logout realizado com sucesso.','success')
        return redirect(url_for('login'))
    
    
    # Rota de cadastro
    @app.route('/caduser', methods=['GET', 'POST'])
    def caduser():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            #Verificando se o usuario já existe
            user = User.query.filter_by(email=email).first()
            if user:
                msg = Markup("<p>Este email já está cadastrado. <a href='/login'>Realize o login!</a></p>")
                flash(msg,'danger')
                return redirect(url_for('caduser'))
            else:
                # gerando hash
                hashed_password = generate_password_hash(password, method='scrypt')
                newUser = User(email=email, password=hashed_password)
                db.session.add(newUser)
                db.session.commit()
                flash('Registro realizado com sucesso', 'success')
                return redirect(url_for('login'))
        return render_template('caduser.html')