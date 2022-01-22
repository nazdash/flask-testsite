# using to describe database models
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    posts = db.relationship('Post', backref='user')


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    snippet = db.Column(db.Text)
    feature_image_path = db.Column(db.String(200))
    feature_video_link = db.Column(db.String(200))
    # tag = db.Column(db.String(100))
    visibility = db.Column(db.Boolean, default=True)
    post_url = db.Column(db.String(200))

class BodyImage(db.Model):
    #__tablename__ = "body_images"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    img_path = db.Column(db.String(175))

    # def __init__(self, post_id, img_path):
    #     self.post_id = post_id
    #     self.img_path = img_path
