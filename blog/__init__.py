from flask import Flask
from flask.ext.markdown import Markdown

app = Flask(__name__)

#from models import *

app.debug = True
app.config.from_pyfile('config.py')

Markdown(app)

import blog.controllers

if __name__ == '__main__':
    app.run(host='0.0.0.0')
