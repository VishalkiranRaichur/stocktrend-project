from flask import Flask
from .config import Config

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config["DATA_DIR"].mkdir(parents=True, exist_ok=True)

    from .blueprints.home import home_bp
    from .blueprints.detail import detail_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(detail_bp)

    return app