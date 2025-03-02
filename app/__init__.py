from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config.config import Config
from extensions import db
from services.EVMLisa.EVMLisaInterface import EVMLisaInterface
from flask_cors import CORS


def create_app():
    # Crea una nuova istanza Flask
    app = Flask(__name__)
    app.config.from_object(Config)  # Carica la configurazione da config.py

    # Inizializza SQLAlchemy
    db.init_app(app)
    CORS(app)  

    app.evmLisaInterface = EVMLisaInterface('./evm-lisa-all.jar')

    from routes import register_routes
    register_routes(app)

    

    with app.app_context():

        db.create_all()

    return app
