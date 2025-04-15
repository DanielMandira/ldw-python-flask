from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow
app = Flask(__name__)

ma = Marshmallow(app)

app.config["MONGO_URI"] = 'mongodb://localhost:27017/api-movies'

api = Api(app)
mongo = PyMongo(app)



from .resources import movies_resources

