from flask_restful import Resource
from api import api

class MovieList(Resource):
    def get(self):
        return "Olá, Mundo! API Rodando!"
             
class RecursosAPI(Resource):
    def get(self):
        return "Você enviou uma solicitação GET"
    def post(self):
        return "Você enviou uma solicitação POST"
    def put(self):
        return "Você enviou uma solicitação PUT"
    def delete(self):
        return "Você enviou uma solicitação DELETE"
    
api.add_resource(MovieList, '/movies')
api.add_resource(RecursosAPI, '/recursos')