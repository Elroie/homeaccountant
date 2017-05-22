#!/bin/sh -

cd /homeaccountant

/usr/local/bin/gunicorn --workers 3 --bind unix:homeaccountant.sock -m 007 "create_app()"
