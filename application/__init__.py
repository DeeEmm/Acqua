from flask import Flask

#from flask_sqlalchemy import SQLAlchemy
#from flask_redis import FlaskRedis

from flask_bootstrap.nav import BootstrapRenderer
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_nav.renderers import Renderer
from flask_nav import register_renderer

import dominate
from dominate.tags import img


branding = img(src='static/logotype_dark.png')
#nav.register_element('top', Navbar(	
topbar = Navbar(
	branding,
	View('Home', 'home_bp.home'),
	View('Trends', 'trends_bp.trends'),
	View('Control', 'control_bp.control'),
	View('Admin', 'admin_bp.admin'),
	View('Help', 'home_bp.help')
)

nav = Nav()
nav.register_element('top', topbar)

# Globally accessible libraries
#db = SQLAlchemy()
#r = FlaskRedis()

def create_app():
	app = Flask(__name__, instance_relative_config=False)
	app.config.from_pyfile('config.py')
	
	
	
	
	# Initialize Plugins
	bootstrap = Bootstrap(app)
	nav.init_app(app)
	#db = SQLAlchemy(app)	
#	db.init_app(app)
#	r.init_app(app)

	with app.app_context():
		# Include our Routes
		from . import routes
		#from .profile import profile
		from .home import home
		from .trends import trends
		from .control import control
		from .admin import admin

		# Register Blueprints
		app.register_blueprint(home.home_bp)
		app.register_blueprint(trends.trends_bp)
		app.register_blueprint(admin.admin_bp)
		app.register_blueprint(control.control_bp)
		
		# Custom renderers		
		register_renderer(app, 'custom', CustomRenderer)
		

		return app



#Custom Navbar Renderer to render after certain bootstrap navbars templates
class CustomRenderer(BootstrapRenderer):
	def visit_Navbar(self, node):
		nav_tag = super(CustomRenderer, self).visit_Navbar(node)
		nav_tag['class'] += 'navbar navbar-inverse navbar-fixed-top'
		return nav_tag