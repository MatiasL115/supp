from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = 'your_secret_key'  # Cambia 'your_secret_key' por una clave secreta

    db.init_app(app)
    csrf.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app
