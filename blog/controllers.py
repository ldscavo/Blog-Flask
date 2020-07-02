from blog import app
from blog.models import *
from flask import render_template, flash, session, request, \
        redirect, url_for
from sqlalchemy.sql import extract, desc
import hashlib
from datetime import datetime
from functools import wraps
import requests
import json

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def utility_processor():
    year = datetime.now().year
    posts = Post.query.order_by(desc(Post.pub_date)).limit(3)
    comments = Comment.query.order_by(desc(Comment.pub_date)).limit(3)

    return dict(current_year=year, recent_posts=posts, recent_comments=comments)

@app.route('/', endpoint='index')
def index():
    return page(1)

@app.route('/page/<int:page>')
def page(page):
    posts = Post.query.order_by(desc(Post.pub_date)).paginate(page, per_page=3)

    return render_template('page.html', posts=posts)

@app.route('/search')
def search():
    query = request.args.get('q')
    page = 1
    if request.args.get('page'):
        page = request.args.get('page')

    matching_posts = Post.query.msearch(query).paginate(page, per_page=3)
    return render_template('search.html', query=query,  posts=matching_posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method != 'POST':
        return render_template('login.html')
    
    password_hashed = hashlib.sha512(request.form['password'].encode('utf-8')).hexdigest()
    
    user = User.query.filter_by(
            username=request.form['username'],
            passwordhash=password_hashed).first()

    if user is not None:
        session['user_id'] = user.id

        flash('You have successfully logged in!')
        return redirect(url_for('index'))
    else:
        flash('Username or password is not correct!')
        return render_template('login.html')

    

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)

    flash('You have successfully logged out.')
    return redirect(url_for('index'))

@app.route('/<int:year>/<int:month>/<int:day>/<string:slug>')
def post(year, month, day, slug):
    post = Post.query.filter(
            extract('year', Post.pub_date) == year,
            extract('month', Post.pub_date) == month,
            extract('day', Post.pub_date) == day,
            Post.slug == slug).first_or_404()

    captcha_key = app.config['RECAPTCHA_SITE_KEY']

    return render_template('post.html', post=post, captcha_key=captcha_key)

@app.route('/post/<int:post_id>')
def post_by_id(post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()
    captcha_key = app.config['RECAPTCHA_SITE_KEY']

    return render_template('post.html', post=post, captcha_key=captcha_key)

@app.route('/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method != 'POST':
        post = Post(session['user_id'], '', '')
        return render_template('post_form.html', post=post)

    post = Post(
            session['user_id'],
            request.form['title'],
            request.form['body'])

    db.session.add(post)
    db.session.commit()

    flash('Published successfully!')
    return redirect(url_for('index'))

@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()

    if request.method == 'POST':
        post.title = request.form['title']
        post.body  = request.form['body']
        db.session.commit()

        flash('Changes saved successfully!')
        return redirect(post.get_url())

    return render_template('post_form.html', post=post)

@app.route('/post/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()

    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()

        flash('Post deleted successfully!')
        return redirect(url_for('index'))

    return render_template('delete_post.html', post=post)

@app.route('/new-comment', methods=['POST'])
def new_comment():
    # check for a valid captcha
    captcha_validation_params = {
        'secret': app.config['RECAPTCHA_SECRET_KEY'],
        'response': request.form['g-recaptcha-response']
    }
    
    captcha_validation_request = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        params=captcha_validation_params)
    
    if not json.loads(captcha_validation_request.text)['success']:
        flash('Error: could not validate captcha.')
        return redirect("/post/{}".format(request.form['post_id']))

    comment = Comment(request.form['post_id'],
            request.form['username'],
            request.form['email'],
            request.form['body'])

    db.session.add(comment)
    db.session.commit()

    return redirect("/post/{}#comments".format(comment.post_id))

@app.route('/comment/delete/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter(Comment.id == comment_id).first_or_404()

    if request.method == 'POST':
        redirect_url = comment.post.get_url()
        db.session.delete(comment)
        db.session.commit()

        flash('Comment deleted successfully!')
        return redirect(redirect_url)

    return render_template('delete_comment.html', comment=comment)
