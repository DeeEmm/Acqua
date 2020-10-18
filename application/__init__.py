from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py')

    # Initialise Plugins
    bootstrap = Bootstrap(app)

    with app.app_context():

        # Include our Routes
        from . import routes
        from . import nav

        # from .profile import profile
        from .home import home
        from .trends import trends
        from .control import control
        from .admin import admin

        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(trends.trends_bp)
        app.register_blueprint(admin.admin_bp)
        app.register_blueprint(control.control_bp)

        return app

