from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'dev-change-this-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project3.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from .routes import main
    app.register_blueprint(main)
    return app
