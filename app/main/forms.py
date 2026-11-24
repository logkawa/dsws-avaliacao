from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class AlunoForm(FlaskForm):
    nome = StringField(
        'Cadastre o novo Aluno:',
        validators=[
            DataRequired(message='Informe o nome do aluno.'),
            Length(max=120)
        ]
    )

    disciplina = SelectField(
        'Disciplina associada:',
        coerce=int,
        validators=[
            DataRequired(message='Selecione uma disciplina.')
        ]
    )

    submit = SubmitField('Cadastrar')