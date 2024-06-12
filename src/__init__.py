# -*- encoding: utf-8 -*-
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
import logging

logging.basicConfig(filename='record.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

db = SQLAlchemy()

def register_blueprints(app):
    for module_name in ('core',):
        module = import_module('src.{}.views'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):
    db.init_app(app)

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove() 

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprints(app)
    configure_database(app)
    return app
