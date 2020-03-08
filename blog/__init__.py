from flask import Flask
from flaskext.markdown import Markdown

app = Flask(__name__)

app.debug = True
app.config.from_pyfile('config.py')

Markdown(app)

import blog.controllers

if __name__ == '__main__':
    app.run(host='0.0.0.0')
