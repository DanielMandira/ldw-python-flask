
from flask import Flask, render_template, request, redirect, url_for
import os
import urllib
import json
from werkzeug.utils import secure_filename
import uuid

# Configurações globais
UPLOAD_FOLDER = 'static/images'  # Pasta para salvar as imagens
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # Extensões permitidas

# Garantir que a pasta de upload existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


streaming = ["Netflix"]
favs = [{"title": 'Castle in the Sky',
         "movie_banner": "static/images/castelonoceu.jpg",
         "description": "The orphan Sheeta inherited a mysterious crystal that links her to the mythical sky-kingdom of Laputa. With the help of resourceful Pazu and a rollicking band of sky pirates, she makes her way to the ruins of the once-great civilization. Sheeta and Pazu must outwit the evil Muska, who plans to use Laputa's science to make himself ruler of the world.",
         }]

# Função para verificar se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def fetch_movies():
    url = 'https://ghibliapi.vercel.app/films'
    response = urllib.request.urlopen(url)
    data = response.read()
    return json.loads(data)


def fetch_movie(movie_id):
    """ Busca informações do filme, incluindo personagens e espécies específicas do filme. """
    url = f'https://ghibliapi.vercel.app/films/{movie_id}'

    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())

        # Buscar os personagens do filme
        movie_characters = []
        for person_url in data.get("people", []):
            try:
                response = urllib.request.urlopen(person_url)
                character = json.loads(response.read())
                movie_characters.append(character)
            except urllib.error.HTTPError:
                pass  # Ignorar erro caso o personagem não exista

        # Buscar as espécies do filme
        movie_species = []
        for species_url in data.get("species", []):
            try:
                response = urllib.request.urlopen(species_url)
                species_data = json.loads(response.read())
                movie_species.append(species_data)
            except urllib.error.HTTPError:
                pass  # Ignorar erro caso a espécie não exista

        # Adicionar os dados filtrados ao filme
        data["filtered_people"] = movie_characters
        data["filtered_species"] = movie_species

        return data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def init_app(app):
    @app.route('/')
    def home():
        moviesjson = fetch_movies()
        return render_template('index.html', moviesjson=moviesjson)

    @app.route('/favoritos', methods=['GET', 'POST'])
    def favoritos():
        moviesjson = fetch_movies()
        if request.method == 'POST':
            if request.form.get('streaming'):
                streaming.append(request.form.get('streaming'))
                return redirect(url_for('favoritos'))
        return render_template('favoritos.html', favs=favs, streaming=streaming, moviesjson=moviesjson)

    @app.route('/cadfavoritos', methods=['GET', 'POST'])
    def cadfavoritos():
        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            movie_banner = request.files.get('movie_banner')

            image_path = ""

            if movie_banner and allowed_file(movie_banner.filename):
                # Garantir que a pasta existe
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)

                # Gerar nome único para o arquivo
                ext = movie_banner.filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid.uuid4().hex}.{ext}"
                filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
                movie_banner.save(filepath)

                # Caminho relativo para armazenar na lista
                image_path = f"static/images/{unique_filename}"

            # Adicionar o filme aos favoritos
            favs.append({
                "title": title,
                "movie_banner": image_path or "",  # Se não houver imagem, manter string vazia
                "description": description
            })

            return redirect(url_for('favoritos'))

        return render_template('cadfavoritos.html', favs=favs)

    @app.route('/movies', methods=['GET', 'POST'])
    def movies():
        moviesjson = fetch_movies()
        return render_template('movies.html', moviesjson=moviesjson)

    @app.route('/movie/<id>', methods=['GET'])
    def movie(id):
        movieinfo = fetch_movie(id)
        if movieinfo:
            # Correto
            return render_template('movieinfo.html', movieinfo=movieinfo)
        else:
            return render_template('error.html', message="Filme não encontrado"), 404
