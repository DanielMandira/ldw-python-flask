from api import mongo
from ..models import movie_model
from bson import ObjectId

def add_movie(movie):
    result = mongo.db.movies.insert_one({
        'title': movie.title,
        'description': movie.description,
        'year':movie.year
    })
    
    new_movie = mongo.db.movies.find_one({
        '_id': result.inserted_id
    })
    return new_movie



#Metodos estaticos não precisam de instâncias
@staticmethod
def get_movies():
    return list(mongo.db.movies.find())

@staticmethod
def delete_movie(id):
    mongo.db.movies.delete_one({'_id': ObjectId(id)})