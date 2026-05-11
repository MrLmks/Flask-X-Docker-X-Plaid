import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.middleware.proxy_fix import ProxyFix


db = SQLAlchemy()


def get_credentials():
    try:
        with open("./secrets/db_user", "r") as user, open("./secrets/db_password", "r") as passw:
            username = user.read().strip()
            password = passw.read().strip()
    except FileNotFoundError:
        return jsonify({"File not Found ! Make sur you created a secrets folder with the files : "
        "db_user & db_password"})
    return username, password


def create_app():
    username, password = get_credentials()
    DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@db:5432/fxdxp_db"

    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
    db.init_app(app)

    from app.models import Transaction, Token

    with app.app_context():
        db.create_all()

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
    
    from .routes import fxdxp
    app.register_blueprint(fxdxp)
    return app
