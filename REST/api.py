import functools
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
from datetime import timedelta, datetime
from flask import make_response, request, current_app, jsonify, g
from functools import update_wrapper, wraps

from Entities import GraphData
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


def json(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        rv = f(*args, **kwargs)
        status_or_headers = None
        headers = None
        if isinstance(rv, tuple):
            rv, status_or_headers, headers = rv + (None,) * (3 - len(rv))
        if isinstance(status_or_headers, (dict, list)):
            headers, status_or_headers = status_or_headers, None
        if not isinstance(rv, dict):
            rv = rv.to_json()
        rv = jsonify(rv)
        if status_or_headers is not None:
            rv.status_code = status_or_headers
        if headers is not None:
            rv.headers.extend(headers)
        return rv

    return wrapped


@verify_authentication
@api_bp.route("/test", methods=['POST'])
def test():
    return "test....", 204


@api_bp.route("/note/addnote", methods=['POST'])
@verify_authentication
def add_note():
    manager = FeedNoteManager()
    user_id = g.user.id
    note_title = 'User Updated Settings'
    note_text = ''
    manager.add(user_id, note_title, note_text, "234", "Settings")
    return "", 204


@api_bp.route("/note/allnotes", methods=['GET'])
@verify_authentication
def return_all_notes():
    manager = FeedNoteManager()
    user_id = g.user.id
    notes = manager.get_all_notes(user_id)
    return notes.to_json()


@api_bp.route("/note/count", methods=['GET'])
@verify_authentication
def return_notes_count():
    manager = FeedNoteManager()
    user_id = g.user.id
    return str(manager.get_note_count(user_id))


@api_bp.route("/statusbar", methods=['GET'])
@verify_authentication
@json
def return_statusbar():
    return {
        'reportCount': UserImage.objects.count(),
        'currentMonthExpenses': 200,
        'expenseChanges': 50
    }


@api_bp.route("/comment/addcomment", methods=['POST'])
@verify_authentication
def add_comment():
    manager = BillCommentManager()
    user_id = g.user.id
    bill_id = request.args.get('bill_id', '746fc33a-fb7c-4595-ba83-198426311234')
    comment_text = request.args.get('comment_text', 'Sample Text')
    manager.add(user_id, bill_id, comment_text)
    return


@api_bp.route("/comment/allcomments", methods=['GET'])
@verify_authentication
def return_all_comments():
    manager = BillCommentManager()
    user_id = g.user.id
    bill_id = request.args.get('bill_id', '746fc33a-fb7c-4595-ba83-198426311234')
    comments = manager.get_all_comments(user_id, bill_id)
    return json.dumps(comments)


@api_bp.route("/register", methods=['POST', 'OPTIONS'])
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
        abort(400)  # missing arguments
    if User.objects(username=username).first() is not None:
        abort(400)  # existing user

    connect(config.DB_NAME)
    user = User(id=uuid.uuid4(), username=username, password=User.hash_password(password), firstName=firstName,
                lastName=lastName, email=email, phone=phone, country=country, city=city, address=address,
                homeType=homeType, homeSize=homeSize, income=income, residence=residence)
    user.save()
    return jsonify({'username': user.username}), 201,


@api_bp.route("/user/settings", methods=['GET'])
@verify_authentication
def get_user_settings():
    connect(config.DB_NAME)
    user = g.user
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


@api_bp.route("/login", methods=['POST'])
def login():
    username_or_token = request.json.get('username')
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if user is None:
        password = request.json.get('password')
        # try to authenticate with username/password
        user = User.objects(username=username_or_token).first()
        if not user or not user.verify_hashed_password(password):
            return "Wrong password", 404
        g.user = user
        token = g.user.generate_auth_token()
        feed_note_manager = FeedNoteManager()
        feed_note_manager.add(g.user.id, "Login", "User logged on", None, "Settings")
        return jsonify({'token': token.decode('ascii')})

    g.user = user
    return jsonify({'token': g.user.generate_auth_token().decode('ascii')})


@verify_authentication
@api_bp.route("/logout")
def logout():
    if g.user is not None:
        g.user = ""
        return "", 200

    return "", 404


@verify_authentication
@api_bp.route('/token')
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


def prepare_scanned_image(image):
    return {
        'id': str(image.id),
        'status': image.status,
        'price': image.price,
        'to_date': str(image.to_date),
        'created_at': str(image.created_at),
        'updated_at': str(image.updated_at),
    }


@api_bp.route("/scanned-images", methods=['GET', 'OPTIONS'])
@verify_authentication
@json
def get_scanned_images():
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('status', type=str, location='args')
    parser.add_argument('user', type=str, location='args')
    parser.add_argument('uniqueId', type=str, location='args', default=None)
    args = parser.parse_args()

    query = Q()
    if args['status']:
        query &= Q(status=args['status'])
    if args['user'] == 'currentUser':
        query &= Q(user_id=g.user.id)
    if args['uniqueId']:
        query &= Q(unique_id=args['uniqueId'])

    images = ScannedImage.objects(query)

    return {'scanned_images': map(prepare_scanned_image, images)}


@verify_authentication
@json
@api_bp.route('/scanned-images/<string:uniqueId>', methods=['PUT'])
def update_scanned_image(uniqueId):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('billAmount', type=int, location='json')
    parser.add_argument('billDate', type=str, location='json')
    parser.add_argument('billNote', type=str, location='json')
    args = parser.parse_args()

    image = ScannedImage.objects(unique_id=uniqueId).first()

    if not image:
        image = UserImage.objects(unique_id=uniqueId).first()
        image.price = args['billAmount']
        image.to_date = args['billDate']
        image.notes = args['billNote']

        image.save()
    else:
        image.original_image.price = args['billAmount']
        image.original_image.to_date = args['billDate']
        image.original_image.notes = args['billNote']

        image.original_image.save()

        image.status = 'done'
        image.save()

    return "", 204


@api_bp.route("/upload", methods=['POST', 'OPTIONS'])
@verify_authentication
def upload_image():
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('file', type=werkzeug.FileStorage, location='files', required=True)
    parser.add_argument('uniqueId', type=str, location='form', required=True)

    args = parser.parse_args()

    file_obj = args['file']
    unique_id = args['uniqueId']

    user_id = g.user.id

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
    classification_manager.enqueue_classification_task(user_id, file_path, unique_id)

    # user_image = UserImage(id=uuid.uuid4())
    # user_image.classification_result = 'Electricity Bill'
    # user_image.image.put(open(os.path.join(path, file_name)))
    # user_image.user_id = user_id
    # user_image.user = user_id
    # user_image.save()
    #
    # scanned_image = ScannedImage()
    # scanned_image.status = 'pending'
    # scanned_image.user_id = user_id
    # scanned_image.original_image = user_image
    # scanned_image.to_date = datetime.now()
    # scanned_image.price = 600
    # scanned_image.save()

    return "", 204


@api_bp.route("/download", methods=['POST'])
@verify_authentication
def download_file(file_name):
    pass


@api_bp.route("/user/update", methods=['POST', 'OPTIONS'])
@verify_authentication
def update_user():
    account = request.json.get('account')
    firstname = account['firstName']
    lastname = account['lastName']
    email = account['email']
    phone = account['phone']
    country = account['country']
    city = account['city']
    address = account['address']
    hometype = account['homeType']
    homesize = account['homeSize']
    income = account['income']
    residence = account['residence']

    if firstname is None:
        abort(400)  # missing arguments
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
    feed_note_manager = FeedNoteManager()
    feed_note_manager.add(g.user.id, "Settings Update", "Account settings changed", None, "Settings")
    return jsonify({'username': user.username}), 200,


@api_bp.route("/reports", methods=['POST'])
@verify_authentication
@json
def return_reports():
    connect(config.DB_NAME)
    user = g.user
    images = UserImage.objects(user_id=user.id)
    reports = {}
    for image in images:
        image_report = {}
        image_report['id'] = str(image.id)
        image_report['user_id'] = str(image.user_id)
        image_report['name'] = image.name
        image_report['classification_result'] = image.classification_result
        if image.classification_result not in reports:
            reports[image.classification_result] = []
            reports[image.classification_result].append(image_report)
        else:
            reports[image.classification_result].append(image_report)
    return reports


@api_bp.route("/graph/adddata", methods=['POST'])
@verify_authentication
def add_graphdata():
    manager = GraphDataManager()
    user_id = g.user.id
    note_title = 'User Updated Settings'
    note_text = ''
    manager.add(user_id, "5", "100", "200", "300")
    return "add data request", 200


@api_bp.route("/graph/getdata", methods=['GET'])
@verify_authentication
def return_graphdata():
    import json
    manager = GraphDataManager()
    realvalue = []
    forecastvalue=[]
    #empty_record = GraphData.GraphData(user_id = g.user.id , month = 0 , electricity_price = 0 , water_price = 0 , other_price = 0)
    for x in range(1, 13):
        empty_record = {
            'electricity_price': 0,
            'water_price': 0,
            'other_price': 0,
            'month': x
        }
        data_record = manager.get_month(x)
        if len(data_record) != 0:
            realvalue.append({ "electricity_price" : data_record[0].electricity_price,
                             "water_price" : data_record[0].water_price,
                             "other_price" : data_record[0].other_price,
                             "month" : x
                             })
            forecastvalue.append(empty_record)
        # elif x == (datetime.now().month + 1):
        #     objects.append(manager.get_detailed_forecast(x))
        else:
            realvalue.append(empty_record)
            forecastvalue.append(manager.get_detailed_forecast(x))
    data = [realvalue, forecastvalue]
    return json.dumps(data)


@api_bp.route("/graph/totalexpense", methods=['GET'])
@verify_authentication
def return_total_expense():
    import json
    manager = GraphDataManager()
    realvalue = []
    forecastvalue=[]
    for x in range(1, 13):
        datarecord = manager.get_month(x)
        if len(datarecord) != 0:
            realvalue.append(datarecord[0].electricity_price + datarecord[0].water_price + datarecord[0].other_price)
            forecastvalue.append(0)
        else:
            forecastvalue.append(manager.get_forecast(x))
            realvalue.append(0)
    forecastvalue[datetime.now().month-1] = manager.get_forecast(datetime.now().month)
    data = [realvalue,forecastvalue]
    return json.dumps(data)


@api_bp.route('/graph/getcurrentmonth', methods=['GET'])
@verify_authentication
def return_current():
    manager = GraphDataManager()
    data = manager.get_month(str(datetime.now().month))
    if len(data) == 0:
        manager.add(g.user.id, str(datetime.now().month), "0", "0", "0")
        data = manager.get_month(str(datetime.now().month))
    return data.to_json()


@api_bp.route("/graph/getpreviousmonth", methods=['GET'])
@verify_authentication
def return_previous():
    manager = GraphDataManager()
    data = manager.get_month(str(datetime.now().month-1))
    if len(data) == 0:
        manager.add(g.user.id, str(datetime.now().month-1), "0", "0", "0")
        data = manager.get_month(str(datetime.now().month-1))
    return data.to_json()
