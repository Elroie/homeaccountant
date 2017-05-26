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
        test_user = User(id=uuid.uuid4(), username='testuser', password=User.hash_password('ab1234'), firstName='test',
                         lastName='testing', email='t@t.com', homeType='apt', income='1000', phone="654",
                         homeSize='4', residence='3', country='Israel', address='bla', city='blabla')
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

    if app.config['DEBUG']:
        from .web import web as web_blueprint
        app.register_blueprint(web_blueprint, url_prefix='')

    return app
