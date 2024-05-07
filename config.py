import os

class Config:
    SECRET_KEY = '48a89ef0b9a63e63dc8a5ca21fc1871d'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.abspath('static/profile_pic')
    DEBUG = True
