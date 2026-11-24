from datetime import datetime
from zoneinfo import ZoneInfo

from flask import render_template, flash, redirect, url_for

from .. import db
from ..models import Aluno, Disciplina
from . import main
from .forms import AlunoForm


@main.route('/')
def index():
    data_hora = datetime.now(ZoneInfo('America/Sao_Paulo'))

    return render_template(
        'index.html',
        data_hora=data_hora
    )


@main.route('/alunos', methods=['GET', 'POST'])
def alunos():
    form = AlunoForm()

    disciplinas = Disciplina.query.order_by(
        Disciplina.codigo.asc()
    ).all()

    form.disciplina.choices = [
        (disciplina.id, disciplina.codigo)
        for disciplina in disciplinas
    ]

    if form.validate_on_submit():
        aluno = Aluno(
            nome=form.nome.data.strip(),
            disciplina_id=form.disciplina.data
        )

        try:
            db.session.add(aluno)
            db.session.commit()

            flash('Aluno cadastrado com sucesso!', 'success')
            return redirect(url_for('.alunos'))

        except Exception:
            db.session.rollback()

            main.logger.exception('Erro ao cadastrar aluno.')

            flash('Não foi possível cadastrar o aluno.', 'danger')

    lista_alunos = Aluno.query.order_by(Aluno.id.asc()).all()

    data_hora = datetime.now(ZoneInfo('America/Sao_Paulo'))

    return render_template(
        'alunos.html',
        form=form,
        alunos=lista_alunos,
        data_hora=data_hora
    )


@main.route('/professores')
def professores():
    return render_template(
        'indisponivel.html',
        modulo='Cadastro de Professores',
        data_hora=datetime.now(ZoneInfo('America/Sao_Paulo'))
    )


@main.route('/disciplinas')
def disciplinas():
    return render_template(
        'indisponivel.html',
        modulo='Cadastro de Disciplinas',
        data_hora=datetime.now(ZoneInfo('America/Sao_Paulo'))
    )


@main.route('/cursos')
def cursos():
    return render_template(
        'indisponivel.html',
        modulo='Cadastro de Cursos',
        data_hora=datetime.now(ZoneInfo('America/Sao_Paulo'))
    )


@main.route('/ocorrencias')
def ocorrencias():
    return render_template(
        'indisponivel.html',
        modulo='Cadastro de Ocorrências',
        data_hora=datetime.now(ZoneInfo('America/Sao_Paulo'))
    )