import os
import random
import string
import werkzeug
import config
import uuid

from mongoengine import connect
from flask import Flask, current_app as app, Blueprint, current_app
from flask_restful import reqparse, abort
from datetime import timedelta
from flask import make_response, request, current_app , jsonify , g
from functools import update_wrapper
from Entities.User import User
import Entities.User
from Entities.UserImage import UserImage
from Entities.ScannedImage import ScannedImage

from ML.ClassificationManager import ClassificationManager


api_bp = Blueprint('v1', __name__)


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@api_bp.route("/test", methods=['GET'])
@crossdomain(origin='*')
def test():
    return "test....."


@api_bp.route("/register",methods = ['POST'])
@crossdomain(origin='*')
def register_new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.objects(username = username).first() is not None:
        abort(400) # existing user

    connect(config.DB_NAME)
    user = User(id=uuid.uuid4(), username=username,password=User.hash_password(password))
    user.hash_password(password)
    user.save()
    return jsonify({ 'username': user.username }), 201,


@api_bp.route("/login",methods = ['POST'])
@crossdomain(origin='*')
def login(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.objects(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False

    g.user = user
    return True

@api_bp.route("/logout")
@crossdomain(origin='*')


@api_bp.route('/token')
@crossdomain(origin='*')
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

@api_bp.route("/upload", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def upload_image():
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('file', type=werkzeug.FileStorage, location='files', required=True)
    args = parser.parse_args()

    file_obj = args['file']

    # elroie todo: remove this when the endpoint is ready
    user_id = args.get('user_id', '746fc33a-fb7c-4595-ba83-19842631859b')

    is_valid_extension = True
    # extract and validate file extension
    file_ext = file_obj.filename.rsplit('.', 1)[1]
    if file_ext not in ['jpg', 'jpeg', 'png']:
        is_valid_extension = False

    if not is_valid_extension:
        abort(
            400,
            status=400,
            error='InvalidExtension',
            message='Invalid extension.',
        )

    # generate update file name
    file_name = '{prefix}.{ext}'.format(
        prefix=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)),
        ext=file_ext,
    )

    # clean and create upload directory before upload
    path = current_app.config['UPLOADS_PATH']
    if not os.path.exists(path):
        os.makedirs(path)

    # save file to disk
    file_path = os.path.join(path, file_name)
    with open(os.path.join(path, file_name), 'wb+') as d:
        d.write(file_obj.stream.read())

    classification_manager = ClassificationManager()
    classification_manager.enqueue_classification_task(user_id, file_path)

    return "", 204


@api_bp.route("/download", methods=['POST'])
def download_file(file_name):
    pass