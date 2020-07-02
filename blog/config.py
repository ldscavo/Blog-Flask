from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os

# Settings from env
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

SECRET_KEY = os.environ.get('SECRET_KEY')

RECAPTCHA_SECRET_KEY = os.environ.get('RECAPTCHA_SECRET_KEY')

RECAPTCHA_SITE_KEY = os.environ.get('RECAPTCHA_SITE_KEY')

DEBUG = os.environ.get('DEBUG')

# Settings that don't change
DEBUG_TB_INTERCEPT_REDIRECTS = False

SQLALCHEMY_TRACK_MODIFICATIONS = False

WHOOSH_BASE = 'search.db'

MSEARCH_BACKEND = 'whoosh'