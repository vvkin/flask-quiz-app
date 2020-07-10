import os
from flask import Flask

def create_app():
    """ App factory function """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'secret',
        DATABASE = os.path.join(app.instance_path, 'quizappdb.sqlite')
    )
    app.config.from_pyfile('config.py', silent=True)

    # Initialize database
    from . import db
    db.init_app()
    
    from .auth.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    return app
