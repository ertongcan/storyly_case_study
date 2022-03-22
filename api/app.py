from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache

db = SQLAlchemy()
migrate = Migrate()
cache = Cache(config={
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': 'cache'})


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # if not declared here migration problem occurs
    from api import models

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)

    from api.routes import stories, event
    app.register_blueprint(stories, url_prefix='/api')
    app.register_blueprint(event, url_prefix='/api')

    @app.route('/')
    def index():
        return ''

    return app
