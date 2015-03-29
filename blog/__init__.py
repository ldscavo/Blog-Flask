from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

#from models import *

app.debug = True
app.config.from_pyfile('config.py')
toolbar = DebugToolbarExtension(app)

import blog.controllers

if __name__ == '__main__':
    app.run()
