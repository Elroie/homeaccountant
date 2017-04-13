import random
import string

import werkzeug
from flask import Flask, current_app as app, Blueprint
from flask_restful import reqparse, abort


api_bp = Blueprint('v1', __name__)


@api_bp.route("/test", methods=['GET'])
def test():
    return "test....."


@api_bp.route("/login")
def login(username, password):
    pass


@api_bp.route("/upload", methods=['POST'])
def upload_image(image):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('file', type=werkzeug.FileStorage, location='files', required=True)
    args = parser.parse_args()

    file_obj = args['file']

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
    path = current_app.config['USER_AGENT_UPLOAD_PATH']

    # save file to disk
    with open(os.path.join(path, file_name), 'wb+') as d:
        d.write(file_obj.stream.read())

    # save a copy of package in assets/packages
    package_path = os.path.join(current_app.config['ASSETS_PATH'],
                                'packages', os_family)

    if not os.path.exists(package_path):
        os.makedirs(package_path)

    self._remove_old_files(package_path)

    shutil.copyfile(
        os.path.join(path, file_name),
        os.path.join(package_path, file_name)
    )


@api_bp.route("/download", methods=['POST'])
def download_file(file_name):
    pass