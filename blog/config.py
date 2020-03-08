from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

DEBUG_TB_INTERCEPT_REDIRECTS = False

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.environ.get('SECRET_KEY')

WHOOSH_BASE = 'search.db'

DEBUG = os.environ.get('DEBUG')

RECAPTCHA_SECRET_KEY = os.environ.get('RECAPTCHA_SECRET_KEY')

RECAPTCHA_SITE_KEY = os.environ.get('RECAPTCHA_SITE_KEY')