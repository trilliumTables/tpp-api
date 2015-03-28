#!/usr/bin/env python

import os
from uuid import uuid4

from flask import current_app, abort, request, jsonify
from webargs import Arg
from webargs.flaskparser import use_kwargs

from trillium.aws import sign_s3
from trillium.api import api_bp
from trillium.extensions import limiter

s3_args = {
    'path': Arg(required=True),
    'mimetype': Arg(required=True),
}


@api_bp.route('/sign_s3')
@limiter.limit('10/second,200/minute')
@use_kwargs(s3_args)
def get_s3_url(path, mimetype):
    dir_, fname = os.path.split(path)
    path = '%s.%s' % (uuid4(), fname)
    expiry = current_app.config['AWS_URL_EXPIRY']
    return jsonify(sign_s3(path, mimetype, 'PUT', expiry))
