#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import urllib
import config, mongoengine, uuid

from ML.ClassificationManager import ClassificationManager
from OCR.ocr_service import OcrService
from flask import url_for, Flask
from flask_script import Manager, Shell, prompt, prompt_pass, prompt_bool
from REST.api import api_bp
from config import Config, basedir
from Entities.User import User
from . import create_app

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
