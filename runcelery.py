#!/usr/bin/env python

from trillium.extensions import celery
from trillium import create_app, DefaultConfig

if __name__ == '__main__':
    app = create_app(DefaultConfig)

    with app.app_context():
        celery.start()
