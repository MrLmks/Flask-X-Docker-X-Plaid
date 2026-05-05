from flask import Flask
from .routes import fxdxp

def create_app():
    app=Flask(__name__)
    app.register_blueprint(fxdxp)
    return app