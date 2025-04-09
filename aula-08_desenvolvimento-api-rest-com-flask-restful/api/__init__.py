from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
app = Flask(__name__)

app.config["MONGO_URI"] = 'mongodb://localhost:27017/api-movies'

api = Api(app)
mongo = PyMongo(app)



from .resources import movies_resources

