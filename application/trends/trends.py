from flask import Blueprint, render_template
from flask import current_app as app
from flask_nav.elements import View

release = app.config["RELEASE"]
version = app.config["VERSION"]


# Blueprint Configuration
trends_bp = Blueprint(
	'trends_bp', 
	__name__,
	template_folder='template',
	static_folder='static',
	static_url_path='/trends'
)


@trends_bp.route('/trends')
def trends():
	return render_template(
		'trends.html', RELEASE=release, VERSION=version
	)
	