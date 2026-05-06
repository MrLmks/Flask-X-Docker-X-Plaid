from flask import Flask
from .routes import fxdxp
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app():
    app=Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
    app.register_blueprint(fxdxp)
    return app