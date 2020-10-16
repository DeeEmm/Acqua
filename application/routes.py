from flask import current_app as app
from flask import render_template
from flask import make_response
from flask_nav.elements import View

	
release = app.config["RELEASE"]
version = app.config["VERSION"]

@app.errorhandler(404)
def not_found(self):
	return render_template('error.html', ERROR_CODE='404', RELEASE=release, VERSION=version), 404


@app.errorhandler(400)
def bad_request(self):
	return render_template("error.html", ERROR_CODE='400', RELEASE=release, VERSION=version), 400


@app.errorhandler(500)
def server_error(self):
	return render_template("error.html", ERROR_CODE='500', RELEASE=release, VERSION=version), 500
			