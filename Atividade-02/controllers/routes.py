from flask import render_template, request, redirect, url_for
from models.database import db
import urllib
import json


def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')