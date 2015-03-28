#!/usr/bin/env python

import logging
import functools

from flask.ext.mail import Message as EmailMessage
from celery.task import current

from trillium.extensions import celery, mail

log = logging.getLogger('tasks')


def retry_exp(max=3600, exc=Exception):
    """Apply an exponential backoff to failed tasks"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exc as e:
                countdown = min(2 ** current.request.retries, max)
                log.error('Task "%s" failed! Retrying in %i seconds...',
                          current.name, countdown)
                current.retry(exc=e, countdown=countdown)
        return wrapper
    return decorator


@celery.task(ignore_result=True, max_retries=12)
@retry_exp()
def send_email(**kwargs):
    msg = EmailMessage(**kwargs)
    return mail.send(msg)
