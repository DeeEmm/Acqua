from flask import Blueprint, render_template
from flask import current_app as app
from flask_nav.elements import View

release = app.config["RELEASE"]
version = app.config["VERSION"]


# Blueprint Configuration
admin_bp = Blueprint(
	'admin_bp', 
	__name__,
	template_folder='templates',
	static_folder='static'
)


@admin_bp.route('/admin')
def admin():
	return render_template(
		'admin.html', RELEASE=release, VERSION=version
	)
	