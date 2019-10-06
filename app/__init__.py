import os
import random
from urllib.parse import urljoin
import uuid
from flask import Flask, redirect, request, url_for

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

    db.init_app(app)
    with app.app_context():
        
        from . import routes
        
        db.create_all()

    return app
