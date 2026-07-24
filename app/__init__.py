from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app import models  # noqa - подгружаем модели чтобы они зарегистрировались

    from app.routes import bp
    app.register_blueprint(bp)

    return app