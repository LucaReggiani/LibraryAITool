from flask import Flask
from flask_restful import Api
from sqlalchemy.orm import declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
from flask_cors import CORS

class Configurations():

    def __init__(self, database_path="mysql://root:root@127.0.0.1:3306/AICHALLENGE"):

        # create the app
        self._app = Flask(__name__)

        CORS(self._app)

        # add API extension
        self._api = Api(self._app)

        # instance of the alembic extension
        self._alembic = Alembic()
        
        # instance of the SQLAlchemy extension 
        self._db = self.config_database(self._app, database_path)

        # initialize the app with the extensions
        self.init_applications()

    def config_database(self, app, database_path):

        Base = declarative_base()

        # create the SQLAlchemy instance
        db = SQLAlchemy(model_class=Base)

        # configure the SQLite database, relative to the app instance folder
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        return db

    def init_applications(self):
        self._db.init_app(self._app)
        self._alembic.init_app(self._app)

    def get_app(self):
        return self._app

    def get_api(self):
        return self._api

    def get_db(self):
        return self._db

    def get_alembic(self):
        return self._alembic

configuration = Configurations()