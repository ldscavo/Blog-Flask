from flask_sqlalchemy import SQLAlchemy
from flask_msearch import Search
from datetime import datetime
from blog import app
import hashlib

db = SQLAlchemy(app)

search = Search(db=db)
search.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    passwordhash = db.Column(db.String(150))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.passwordhash = hashlib.sha512(password).hexdigest()

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    __searchable__ = ['title', 'body'] # Allows searching with WhooshAlchemy 

    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User',
            backref = db.backref('posts', lazy='dynamic'))

    title = db.Column(db.String(150))
    body = db.Column(db.Text)
    
    slug = db.Column(db.String(80))
    pub_date = db.Column(db.DateTime)
   
    comments = db.relationship('Comment',
            lazy='dynamic',
            cascade='all,delete',
            backref='post')

    def __init__(self, author_id, title, body):
        self.author_id = author_id
        self.title = title
        self.body = body
        self.pub_date = datetime.utcnow()
        
        self.__create_slug()
        
    def __repr__(self):
        return '<Post %r>' % self.title

    def __create_slug(self):
        import re
        
        title_slug = re.sub(r'[^\w ]', '', self.title)
        
        slug = title_slug.lower().replace(' ', '-')

        self.slug = slug

    def get_url(self):
        url = "/{0}/{1}".format(
                self.pub_date.strftime('%Y/%m/%d'),
                self.slug)
        return url
                

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    email_md5 = db.Column(db.String(32))
    body = db.Column(db.Text)

    pub_date = db.Column(db.DateTime)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, post_id, username, email, body):
        self.post_id = post_id
        self.username = username
        self.email = email
        self.email_md5 = hashlib.md5(email).hexdigest()
        self.body = body
        self.pub_date = datetime.utcnow()

    def __repr__(self):
        return '<Category %r>' % self.username
