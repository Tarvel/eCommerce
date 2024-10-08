from flask import Flask
from config import DevelopmentConfig
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        from .routes import auth, product
        from .forms import DeleteForm  # Import here to avoid circular dependency

        app.register_blueprint(auth)
        app.register_blueprint(product)

        @app.context_processor
        def inject_delete_form():
            delete = DeleteForm()
            return dict(delete=delete)

    @app.cli.command('create_db')
    def create_db():
        """Create the database tables."""
        db.create_all()
        print("Database tables created.")

    return app
