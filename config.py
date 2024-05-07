import os

class Config:
    SECRET_KEY = '48a89ef0b9a63e63dc8a5ca21fc1871d'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:08060110993@localhost/flask_eCommerce'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.abspath('static/profile_pic')
    DEBUG = True
