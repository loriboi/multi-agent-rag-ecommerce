from __future__ import annotations

from flask import Flask

from catalog_rag.api.routes import api_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    return app
