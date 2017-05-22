#!/bin/sh -

cd /homeaccountant

/usr/local/bin/gunicorn --workers 3 --bind 127.0.0.1:33014 "create_app()"
