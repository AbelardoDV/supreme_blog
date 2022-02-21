from app import db
from sqlalchemy import DateTime,Integer
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique= True)
    email = db.Column(db.String(120),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))
    timestamp=db.Column(DateTime(),index=True,default=datetime.utcnow)
    user_id = db.Column(Integer(),db.ForeignKey('user.id'),nullable=False)

    def __repr__(self) -> str:
        return f'<Post {self.body}>'