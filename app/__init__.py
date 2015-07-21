# Created by cxy on 2014-12-25
# -*- coding: utf-8 -*-
from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .views.admin import admin
from models import db

login_manager = LoginManager()

app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(admin, url_prefix='/admin')
login_manager.init_app(app)
# db = SQLAlchemy(app)

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(admin, url_prefix='/admin')
    db.init_app(app)
    return app


app = create_app()
# db = SQLAlchemy(app)