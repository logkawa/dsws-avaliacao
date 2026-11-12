from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import BadData
from flask import current_app
from flask_login import UserMixin
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    # --- Senha (nunca guardada em texto puro) ---
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password,
                                                    method='pbkdf2:sha256')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # --- Tokens assinados (confirmação, reset de senha, troca de e-mail) ---
    @staticmethod
    def _serializer():
        return Serializer(current_app.config['SECRET_KEY'])

    @staticmethod
    def _load_token(token, expiration):
        """Devolve os dados do token ou None se for inválido/expirado."""
        try:
            return User._serializer().loads(token, max_age=expiration)
        except BadData:
            return None

    def generate_confirmation_token(self):
        return self._serializer().dumps({'confirm': self.id})

    def confirm(self, token, expiration=3600):
        data = self._load_token(token, expiration)
        if data is None or data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self):
        return self._serializer().dumps({'reset': self.id})

    @staticmethod
    def reset_password(token, new_password, expiration=3600):
        data = User._load_token(token, expiration)
        if data is None:
            return False
        user = db.session.get(User, data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email):
        return self._serializer().dumps(
            {'change_email': self.id, 'new_email': new_email})

    def change_email(self, token, expiration=3600):
        data = self._load_token(token, expiration)
        if data is None or data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if User.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
