#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import urllib

from flask import url_for, Flask
from flask_script import Manager, Shell, prompt, prompt_pass, prompt_bool

from REST.api import api_bp
from config import Config, basedir


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    # fix proxy headers
    from werkzeug.contrib.fixers import ProxyFix
    # max number of proxies is 2 because we allow another hop for load balancer
    app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=2)


    # prepare db

    app.register_blueprint(api_bp, url_prefix='/api')

    return app


app = create_app()
manager = Manager(app)


@manager.command
def secure():
    """Runs the Flask development server with https enabled."""
    manager.app.run('0.0.0.0', debug=True, port=5000, ssl_context='adhoc')

@manager.command
def profile():
    """Runs the Flask development server with profiling."""
    from werkzeug.contrib.profiler import ProfilerMiddleware

    manager.app.config['PROFILE'] = True
    manager.app.wsgi_app = ProfilerMiddleware(manager.app.wsgi_app,
                                              restrictions=[30])
    manager.app.run(debug=True)


if __name__ == '__main__':
    manager.run()
