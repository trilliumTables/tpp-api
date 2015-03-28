#!/usr/bin/env python

from flask import Blueprint, request, current_app

from .util import log


api_bp = Blueprint("api", __name__)


@api_bp.after_request
def log_response(response):
    """Log any requests/responses with an error code"""
    if current_app.debug:  # pragma: no cover, debugging only
        log.debug('%7s: %s - %i', request.method, request.url,
                  response.status_code)
        if response.status_code >= 400:
            log.debug('Response data: \n%s', response.data)
            log.debug('Request data: \n%s', request.data)

    return response


# Import the resources to add the routes to the blueprint before the app is
# initialized
from . import (  # NOQA
    s3url,
    email,
)
