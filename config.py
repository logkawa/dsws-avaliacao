import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# Carrega o .env usando o caminho absoluto do projeto,
# funcionando não importa de onde o Flask for iniciado
load_dotenv(os.path.join(basedir, '.env'), override=True)


class Config:
    # A chave assina a sessão de login e os tokens de confirmação/reset.
    # Quem a conhece consegue forjar ambos, por isso ela vem só do .env.
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Mailgun (valores vêm do .env) ---
    MAILGUN_API_URL = os.environ.get('MAILGUN_API_URL')
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    MAILGUN_FROM = os.environ.get('MAILGUN_FROM')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'

    # Mostra na tela o link de confirmação/reset (como no exemplo do professor).
    # Útil no sandbox do Mailgun, onde só endereços autorizados recebem e-mail.
    # ATENÇÃO: com isso ligado, qualquer pessoa consegue confirmar contas e
    # redefinir senhas sem ter acesso ao e-mail. Desligue fora das aulas.
    FLASKY_SHOW_LINKS = os.environ.get('FLASKY_SHOW_LINKS', 'true').lower() in \
        ['true', 'on', '1']

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = Config.SECRET_KEY or 'chave-apenas-para-desenvolvimento'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = Config.SECRET_KEY or 'chave-apenas-para-testes'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        if not app.config.get('SECRET_KEY'):
            raise RuntimeError(
                'Defina SECRET_KEY no .env de produção (gere uma com: '
                'python -c "import secrets; print(secrets.token_hex(32))").')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
