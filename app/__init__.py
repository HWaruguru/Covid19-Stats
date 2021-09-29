from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_options
from flask_cors import CORS


db = SQLAlchemy()


def create_app(config_name):
    # creating a flask application
    app = Flask(__name__)
    CORS(app)

    # initialize flask applications
    db.init_app(app)
    # creating the app configurations
    app.config.from_object(config_options[config_name])

    #registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)



    return app