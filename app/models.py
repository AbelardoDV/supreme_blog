from hashlib import md5
from app import db
from sqlalchemy import DateTime, Integer
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer,
                               db.ForeignKey('user.id')),
                     )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    followed = db.relationship('User', secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic'
                               )

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def get_avatar_link(self, size: int) -> str:
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def follow(self, user: 'User') -> None:
        self.followed.append(user)

    def unfollow(self, user: 'User') -> None:
        if self.followed.filter(followers.c.followed_id == user.id):
            self.followed.remove(user)

    def is_following(self, user: 'User'):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        own_posts = Post.query.filter_by(user_id=self.id)
        followed = Post.query.join(
            followers,
            followers.c.followed_id == Post.user_id).filter(
            followers.c.follower_id == self.id)
        return followed.union(own_posts).order_by(Post.timestamp.desc())


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(DateTime(), index=True, default=datetime.utcnow)
    user_id = db.Column(Integer(), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return f'<Post {self.body}>'
