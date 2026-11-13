from flask import render_template
from flask_login import current_user

from . import main
from ..models import User


@main.route('/')
def index():
    usuarios = User.query.order_by(User.id.asc()).all()

    return render_template(
        'index.html',
        usuarios=usuarios
    )