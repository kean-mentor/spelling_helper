import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config


db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from .models import Score, Word
    db.create_all(app=app)

    from .import quiz
    app.register_blueprint(quiz.bp)

    return app

