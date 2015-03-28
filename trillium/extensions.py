#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""

from flask.ext.mail import Mail
from flask.ext.celery import Celery
from flask.ext.cors import CORS
from flask.ext.limiter import Limiter

mail = Mail()
celery = Celery()
cors = CORS()
limiter = Limiter()
