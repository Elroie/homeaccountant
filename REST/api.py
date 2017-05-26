import os
import random
import string
import werkzeug
import config
import json
import uuid



from mongoengine import connect, Q
from flask import Flask, current_app as app, Blueprint, current_app
from flask_restful import reqparse, abort
from datetime import timedelta
from flask import make_response, request, current_app , jsonify , g
from functools import update_wrapper, wraps

from Entities import BillComment
from Entities.User import User
import Entities.User
from Entities.UserImage import UserImage
from Entities.ScannedImage import ScannedImage
from werkzeug.exceptions import HTTPException, NotFound, BadRequest, Unauthorized
from ML.BillCommentManager import BillCommentManager

from ML.ClassificationManager import ClassificationManager
from ML.FeedNoteManager import FeedNoteManager
from ML.GraphDataManager import GraphDataManager

api_bp = Blueprint('v1', __name__)

def verify_authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
       token = request.headers.get('token')
       if token is None:
           raise Unauthorized("the token is not valid you son of a bitch")
       user = User.verify_auth_token(token)
       if user is None:
           raise Unauthorized("the token is not valid you son of a bitch")

       g.user = user
       return func()
    return wrapper

@verify_authentication
@api_bp.route("/test",methods=['POST','OPTIONS'])
def test():
    return "test....", 204

@api_bp.route("/note/addnote", methods=['POST'])
def add_note():
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('user_id', type=werkzeug.FileStorage, location='files', required=True)
    parser.add_argument('user_id', type=werkzeug.FileStorage, location='files', required=True)
    # args = parser.parse_args()
    # file_obj = args['file']
    manager = FeedNoteManager()
    user_id = 'a9ab55e1-419c-43c6-9cb4-8e71462c84b3'
    note_title = 'User Updated Settings'
    note_text = ''
    manager.add(user_id,note_title,note_text,"234","Settings")
    return "", 204

@api_bp.route("/note/allnotes", methods=['GET'])
def return_all_notes():
    manager = FeedNoteManager()
    user_id = request.args.get('user_id', 'a9ab55e1-419c-43c6-9cb4-8e71462c84b3')
    notes = manager.get_all_notes(user_id)
    return notes.to_json()

@api_bp.route("/note/count", methods=['GET'])
def return_notes_count():
    manager = FeedNoteManager()
    user_id = request.args.get('user_id', 'a9ab55e1-419c-43c6-9cb4-8e71462c84b3')
    return str(manager.get_note_count(user_id))


@api_bp.route("/statusbar", methods=['GET'])
def return_statusbar():
    connect(config.DB_NAME)
    response = {}
    response['reportCount'] = str(len(UserImage.objects))
    response['currentMonthExpenses'] = "200"
    response['expenseChanges'] = "50"
    return json.dumps(response)

@api_bp.route("/comment/addcomment", methods=['POST'])
def add_comment():
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('file', type=werkzeug.FileStorage, location='files', required=True)
    args = parser.parse_args()
    file_obj = args['file']
    manager = BillCommentManager()
    user_id = request.args.get('user_id', 'a9ab55e1-419c-43c6-9cb4-8e71462c84b3')
    bill_id = request.args.get('bill_id', '746fc33a-fb7c-4595-ba83-198426311234')
    comment_text = request.args.get('comment_text', 'Sample Text')
    manager.add(user_id,bill_id,comment_text)
    return

@api_bp.route("/comment/allcomments", methods=['GET'])
def return_all_comments():
    manager = BillCommentManager()
    user_id = request.args.get('user_id', 'a9ab55e1-419c-43c6-9cb4-8e71462c84b3')
    bill_id = request.args.get('bill_id', '746fc33a-fb7c-4595-ba83-198426311234')
    comments = manager.get_all_comments(user_id,bill_id)
    return json.dumps(comments)


@api_bp.route("/register",methods=['POST','OPTIONS'])
def register_new_user():
    account = request.json.get('account')
    username = account['username']
    password = account['password']
    firstName = account['firstName']
    lastName = account['lastName']
    email = account['email']
    phone = account['phone']
    country = account['country']
    city = account['city']
    address = account['address']
    homeType = account['homeType']
    homeSize = account['homeSize']
    income = account['income']
    residence = account['residence']

    if username is None or password is None:
        abort(400) # missing arguments
    if User.objects(username = username).first() is not None:
        abort(400) # existing user

    connect(config.DB_NAME)
    user = User(id=uuid.uuid4(), username=username,password=User.hash_password(password), firstName=firstName, lastName=lastName, email=email, phone=phone, country=country, city=city, address=address, homeType=homeType, homeSize=homeSize, income=income, residence=residence)
    user.save()
    return jsonify({'username': user.username}), 201,


@api_bp.route("/user/settings", methods=['GET', 'OPTIONS'])
@verify_authentication
def get_user_settings():
    connect(config.DB_NAME)
    user = User.objects(username=g.user).first()
    user_settings = {
        'firstName': user.firstName,
        'lastName': user.lastName,
        'email': user.email,
        'phone': user.phone,
        'country': user.country,
        'city': user.city,
        'address': user.address,
        'homeType': user.homeType,
        'homeSize': user.homeSize,
        'income': user.income,
        'residence': user.residence
    }
    return jsonify(user_settings), 200,


@api_bp.route("/login",methods=['POST','OPTIONS'])
def login():
    username_or_token = request.json.get('username')
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if user is None:
        password = request.json.get('password')
        # try to authenticate with username/password
        user = User.objects(username = username_or_token).first()
        if not user or not user.verify_hashed_password(password):
            return "Wrong password", 404
        g.user = user
        token = g.user.generate_auth_token()
        return jsonify({'token': token.decode('ascii')})

    g.user = user
    return jsonify({'token': g.user.generate_auth_token().decode('ascii')})

@api_bp.route("/logout")
def logout(token):
    g.user = ""
    return "", 200


@api_bp.route('/token')
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })


@api_bp.route("/scanned-images", methods=['GET', 'OPTIONS'])
def get_scanned_images():
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('status', type=str, location='args')
    args = parser.parse_args()

    query = Q()
    if args['status']:
        query &= Q(status=args['status'])


    images = ScannedImage().objects(query).get()


    return images.to_json()


@api_bp.route("/upload", methods=['POST', 'OPTIONS'])
def upload_image():
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('file', type=werkzeug.FileStorage, location='files', required=True)
    # parser.add_argument('date', type=str, location='form', required=True)
    # parser.add_argument('note', type=str, location='form', required=True)
    # parser.add_argument('amount', type=str, location='form', required=True)
    # parser.add_argument('date', type=str, location='form', required=True)
    # parser.add_argument('amount', type=str, location='form', required=True)
    # parser.add_argument('note', type=str, location='form', required=True)
    args = parser.parse_args()

    file_obj = args['file']
    # date = args['date']
    # note = args['note']
    # amount = args['amount']

    # elroie todo: remove this when the endpoint is ready
    user_id = args.get('user_id', 'a9ab55e1-419c-43c6-9cb4-8e71462c84b3')

    is_valid_extension = True
    # extract and validate file extension
    file_ext = file_obj.filename.rsplit('.', 1)[1]
    if file_ext.lower() not in ['jpg', 'jpeg', 'png']:
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

@api_bp.route("/user/update", methods=['POST', 'OPTIONS'])
@verify_authentication
def update_user():
    firstname = request.json.get('firstName')
    lastname = request.json.get('lastName')
    email = request.json.get('email')
    phone = request.json.get('phone')
    country = request.json.get('country')
    city = request.json.get('city')
    address = request.json.get('address')
    hometype = request.json.get('homeType')
    homesize = request.json.get('homeSize')
    income = request.json.get('income')
    residence = request.json.get('residence')

    if firstname is None:
        abort(400) # missing arguments
    elif lastname is None:
        abort(400)  # missing arguments
    elif email is None:
        abort(400)  # missing arguments
    elif phone is None:
        abort(400)  # missing arguments
    elif country is None:
        abort(400)  # missing arguments
    elif city is None:
        abort(400)  # missing arguments
    elif address is None:
        abort(400)  # missing arguments
    elif hometype is None:
        abort(400)  # missing arguments
    elif homesize is None:
        abort(400)  # missing arguments
    elif income is None:
        abort(400)  # missing arguments
    elif residence is None:
        abort(400)  # missing arguments

    connect(config.DB_NAME)
    user = g.user
    user.firstName = firstname
    user.lastName = lastname
    user.email = email
    user.phone = phone
    user.country = country
    user.city = city
    user.address = address
    user.homeType = hometype
    user.homeSize = homesize
    user.income = income
    user.residence = residence
    user.save()
    return jsonify({'username': user.username}), 200,


@api_bp.route("/reports", methods=['POST'])
def return_reports():
    connect(config.DB_NAME)
    user = g.user
    images = UserImage.objects(id = user.id)
    reports = {}
    for image in images:
        if image.classification_type not in reports:
            reports[image.classification_type] = []
            reports[image.classification_type].append(image)
        else:
            reports[image.classification_type].append(image)
    return reports.to_json()