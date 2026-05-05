from flask import Flask
from pathlib import Path
from .config import Config

BASE_DIR = Path(__file__).resolve().parent

def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static")
    )

    app.config.from_object(config_class)

    app.config["DATA_DIR"].mkdir(parents=True, exist_ok=True)

    from .blueprints.home import home_bp
    from .blueprints.detail import detail_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(detail_bp)

    return app