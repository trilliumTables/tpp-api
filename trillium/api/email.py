#!/usr/bin/env python

from flask import render_template, current_app
from webargs import Arg
from webargs.flaskparser import use_args

from trillium.api import api_bp, log
from trillium.extensions import limiter
from trillium.tasks import send_email

email_args = {
    'user_name': Arg(required=True),
    'user_email': Arg(required=True),
    'subject': Arg(default=''),
    'body': Arg(required=True),
    'link': Arg(required=True),
}


@api_bp.route('/send_email', methods=['POST'])
@limiter.limit('10/second,200/minute')
@use_args(email_args)
def send_info_email(args):

    recipients = current_app.config['CONTACT_EMAIL_RECIPIENTS'].split(',')
    _email = {
        'subject': 'Trillium Pet Products Inquiry: "%s"' % args['subject'],
        'html': render_template('contact_email.html.j2', **args),
        'reply_to': '%s <%s>' % (args['user_name'], args['user_email']),
        'recipients': recipients,
    }
    log.info('Sending email from "{user_name} <{user_email}>"'.format(**args))
    send_email.delay(**_email)

    return 'OK', 200
