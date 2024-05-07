import os

class Config:
    SECRET_KEY = '48a89ef0b9a63e63dc8a5ca21fc1871d'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'postgresql://flask_ecommerce_81dp_user:KD5OFXHSHIOdhpmoZ48j8zC1B2gyvX1J@dpg-cotb936g1b2c73de8qeg-a.oregon-postgres.render.com/flask_ecommerce_81dp'
    # postgresql://postgres:08060110993@localhost/flask_eCommerce
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.abspath('static/profile_pic')
    DEBUG = True
