from blog import app
from blog.models import *
from flask import render_template, flash, session, request
import hashlib

@app.route('/')
def index():
    posts = Post.query.all()

    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password_hashed = hashlib.sha512(request.form['password']).hexdigest()
        user = User.query.filter_by(username=request.form['username'],
                passwordhash=password_hashed).first()
        if user is not None:
            session['user_id'] = user.id
            flash('You have successfully logged in!')
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

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post = Post(session['user_id'],
                request.form['title'],
                request.form['body'])
        db.session.add(post)
        db.session.commit()

        flash('Published successfully!')
        return render_template('index.html')

    return render_template('new_post.html')
