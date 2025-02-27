from flask import render_template, request, redirect, url_for
import urllib
import json

streaming = []
favoritos = [{"title": 'Castle in the Sky', 
              "movie_banner": "https://image.tmdb.org/t/p/w533_and_h300_bestv2/3cyjYtLWCBE1uvWINHFsFnE8LUK.jpg",
               "description": "The orphan Sheeta inherited a mysterious crystal that links her to the mythical sky-kingdom of Laputa. With the help of resourceful Pazu and a rollicking band of sky pirates, she makes her way to the ruins of the once-great civilization. Sheeta and Pazu must outwit the evil Muska, who plans to use Laputa's science to make himself ruler of the world.",
              }]

def fetch_movies():
    url = 'https://ghibliapi.vercel.app/films'
    response = urllib.request.urlopen(url)
    data = response.read()
    return json.loads(data)

def fetch_movie(movie_id):
    url = f'https://ghibliapi.vercel.app/films/{movie_id}'
    try:
        response = urllib.request.urlopen(url)
        data = response.read()
        return json.loads(data)
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
        if request.method == 'POST':
            if request.form.get('streaming'):
                streaming.append(request.form.get('streaming'))
                return redirect(url_for('favoritos'))
        return render_template('favoritos.html', favoritos=favoritos, streaming=streaming)
    
    @app.route('/cadfavoritos', methods=['GET', 'POST'])
    def cadfavoritos():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            favoritos.append(form_data)
            return redirect(url_for('cadfavoritos'))
        return render_template('cadfavoritos.html', favoritos=favoritos)
    
    @app.route('/movies', methods=['GET', 'POST'])
    def movies():
        moviesjson = fetch_movies()
        return render_template('movies.html', moviesjson=moviesjson)
    @app.route('/movie/<id>', methods=['GET', 'POST'])
    def movie(id):
        movieinfo = fetch_movie(id)
        if movieinfo:
            return render_template('movieinfo.html', movieinfo=movieinfo)
        else:
            return 'Filme não encontrado', 404
        