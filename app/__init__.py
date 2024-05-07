
from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager







app = Flask(__name__)
app.config.from_object(Config)
    
    
app.app_context().push()

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'



from . import routes
app.register_blueprint(routes.auth)
app.register_blueprint(routes.product)

