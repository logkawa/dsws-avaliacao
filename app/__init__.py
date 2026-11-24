
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        from .models import Disciplina
        db.create_all()

        disciplinas = [
            ('DSWA5', 'Desenvolvimento de Sistemas Web'),
            ('TCOA5', 'Técnicas de Comunicação'),
            ('GPSA5', 'Gestão de Projetos'),
            ('IHCA5', 'Inglês')
        ]

        for codigo, nome in disciplinas:
            existente = Disciplina.query.filter_by(codigo=codigo).first()
            if existente is None:
                db.session.add(Disciplina(codigo=codigo, nome=nome))

        db.session.commit()

    return app
