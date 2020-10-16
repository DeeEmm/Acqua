from flask import Blueprint, render_template
from flask import current_app as app
from flask_nav.elements import View

release = app.config["RELEASE"]
version = app.config["VERSION"]


# Blueprint Configuration
control_bp = Blueprint(
	'control_bp', 
	__name__,
	template_folder='templates',
	static_folder='static'
)


@control_bp.route('/control')
def control():
	return render_template(
		'control.html', RELEASE=release, VERSION=version
	)
	