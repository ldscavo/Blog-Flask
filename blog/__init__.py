from flask import Flask, request, session, g, redirect, url_for, \
                  abort, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
import hashlib

app = Flask(__name__)

from models import *

app.debug = True
app.config.from_pyfile('config.py')
toolbar = DebugToolbarExtension(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password_hashed = hashlib.sha512(request.form['password']).hexdigest()
        user = User.query.filter_by(username=request.form['username'],
                passwordhash=password_hashed).first()
        if user is not None:
            session['user_id'] = user.id            
            return render_template('index.html')
        else:
            flash('Username or password is not correct!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have successfully logged out.')
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['password'] != request.form['password-confirm']:
            flash('Passwords do not match.')
            return render_template('register.html')
        user = User(request.form['username'],
                request.form['email'],
                request.form['password'])
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id

        flash('You have been registered!')
        return render_template('index.html')

    return render_template('register.html')

if __name__ == '__main__':
    app.run()
