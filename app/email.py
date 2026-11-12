import requests
from flask import current_app, render_template


def send_email(to, subject, template, **kwargs):
    """Envia um e-mail pela API HTTP do Mailgun.

    O corpo vem dos templates '<template>.txt' e '<template>.html'.
    Retorna True se o Mailgun aceitou o envio.
    """
    app = current_app._get_current_object()
    assunto = app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject

    try:
        resposta = requests.post(
            app.config['MAILGUN_API_URL'],
            auth=('api', app.config['MAILGUN_API_KEY']),
            data={
                'from': app.config['MAILGUN_FROM'],
                'to': to,
                'subject': assunto,
                'text': render_template(template + '.txt', **kwargs),
                'html': render_template(template + '.html', **kwargs),
            },
            timeout=15,
        )
    except requests.RequestException as erro:
        app.logger.error('[Mailgun] erro de conexão ao enviar para %s: %s',
                         to, erro)
        return False

    if resposta.status_code != 200:
        app.logger.error('[Mailgun] falha (%s) para %s: %s',
                         resposta.status_code, to, resposta.text)
        return False

    app.logger.info('[Mailgun] enviado para %s', to)
    return True
