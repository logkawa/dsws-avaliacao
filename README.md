# Desenvolvimento Web com Flask

Repositório referente às aulas de DSWS
Aluno: Nathalia Ventura Kawakami
Prontuário: PT3036189

## Estrutura do projeto

```
├── app/
│   ├── __init__.py        # create_app() (application factory) e extensões
│   ├── models.py          # Role, User (senha com hash, tokens)
│   ├── email.py           # envio de e-mail via Mailgun
│   ├── auth/              # blueprint "auth" (autenticação)
│   │   ├── __init__.py
│   │   ├── forms.py       # login, cadastro, senha, e-mail
│   │   └── views.py       # login, logout, cadastro, confirmação, reset...
│   ├── main/              # blueprint "main"
│   │   ├── __init__.py
│   │   ├── errors.py      # páginas 404 e 500
│   │   ├── forms.py
│   │   └── views.py       # rota: /
│   ├── static/            # favicon
│   └── templates/         # base, index, 404, 500, auth/ (e auth/email/)
├── migrations/
├── tests/
├── config.py              # configurações (development / testing / production)
├── flasky.py              # ponto de entrada (FLASK_APP)
├── requirements.txt
└── .env.example
```

## 1. Preparando o ambiente

```powershell
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Variáveis de ambiente

Copie `.env.example` para `.env` e preencha (chaves do Mailgun e `SECRET_KEY`).
O `.env` não vai para o GitHub.

Gerar uma `SECRET_KEY`:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

`FLASKY_SHOW_LINKS=true` mostra na tela o link de confirmação/reset (útil no
sandbox do Mailgun, onde só endereços autorizados recebem e-mail). Fora das
aulas, use `false`: com `true`, qualquer pessoa confirma contas e redefine senhas
sem acesso ao e-mail.

## 3. Criando o banco de dados

```powershell
flask shell
```

```python
db.create_all()
db.session.add(Role(name='Usuário'))
db.session.commit()
exit()
```

Se o banco já existia de uma versão anterior (sem e-mail/senha), apague o arquivo
(`data-dev.sqlite`) antes e crie de novo.

## 4. Iniciando localmente

```powershell
flask run --debug
```

Acesse: http://127.0.0.1:5000

## 5. Testes

```powershell
flask test
```

## 6. Produção (PythonAnywhere)

No `.env` do servidor, defina `FLASK_CONFIG=production` e uma `SECRET_KEY` própria
(obrigatória em produção). O banco usado é o `data.sqlite`.
No arquivo WSGI da web app, importe a aplicação assim:

```python
from flasky import app as application
```
