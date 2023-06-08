from flask import Flask
import os

from models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    return app