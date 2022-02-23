import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')   or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI') or \
        'postgresql://postgres:nemuuser@localhost:5432/microblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POST_PER_PAGE = 25
