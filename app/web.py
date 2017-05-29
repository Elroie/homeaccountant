from __future__ import absolute_import

import os

from flask import Blueprint, send_from_directory, send_file
from config import basedir

web = Blueprint('web', __name__)

root_dir = os.path.join(basedir, 'web')

static_dir = os.path.join(basedir, root_dir)
config_dir = os.path.join(basedir, root_dir, 'config')
bower_dir = os.path.join(basedir, root_dir, 'bower_components')
build_dir = os.path.join(basedir, root_dir, 'build')

images_dir = os.path.join(static_dir, 'images')
modules_dir = os.path.join(static_dir, 'app')
libs_dir = os.path.join(static_dir, 'libs')
styles_dir = os.path.join(static_dir, 'styles')
sounds_dir = os.path.join(static_dir, 'sound')
resources_dir = os.path.join(static_dir, 'resources')


@web.route('/')
@web.route('/index.html')
def index():
    return send_file(os.path.join(static_dir, 'index.html'))


@web.route('/bower_components/<path:filename>')
def bower(filename):
    return send_from_directory(bower_dir, filename)


@web.route('/app/<path:filename>')
def modules(filename):
    return send_from_directory(modules_dir, filename)


@web.route('/sound/<path:filename>')
def sound(filename):
    return send_from_directory(sounds_dir, filename)


@web.route('/resources/<path:filename>')
def resources(filename):
    return send_from_directory(resources_dir, filename)


@web.route('/build/<path:filename>')
def build(filename):
    return send_from_directory(build_dir, filename)


@web.route('/libs/<path:filename>')
def libs(filename):
    return send_from_directory(libs_dir, filename)


@web.route('/styles/<path:filename>')
def styles(filename):
    return send_from_directory(styles_dir, filename)


@web.route('/images/<path:filename>')
def images(filename):
    return send_from_directory(images_dir, filename)
