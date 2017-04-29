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


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    # fix proxy headers
    from werkzeug.contrib.fixers import ProxyFix
    # max number of proxies is 2 because we allow another hop for load balancer
    app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=2)

    mongoengine.connect(config.DB_NAME)
    if len(User.objects) == 0:
        test_user = User(id=uuid.uuid4(), username='testuser', password='ab1234')
        test_user.save()
        for user in User.objects:
            print user.id, user.username

    if config.SHOULD_USE_MACHINE_LEARNING:
        # start the classification thread.
        classification_manager = ClassificationManager()
        classification_manager.start()

    if config.SHOULD_USE_OCR:
        ocr_service = OcrService()
        ocr_service.start()
        image_path = config.BASE_PATH + 'ML/images/electricity/test/test1.jpg'
        # ocr_service.enqueue_ocr_task(image_path)

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
