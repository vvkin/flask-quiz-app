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

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize database
    from . import db
    db.init_app(app)

    from .auth.auth import auth_bp
    app.register_blueprint(auth_bp)
    from .general.general import general_bp
    app.register_blueprint(general_bp)
    
    return app
