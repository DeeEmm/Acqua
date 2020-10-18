from flask import Blueprint, render_template
from flask import current_app as app

release = app.config["RELEASE"]
version = app.config["VERSION"]


# Blueprint Configuration
home_bp = Blueprint(
    'home_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@home_bp.route('/')
@home_bp.route('/home')
@home_bp.route('/index')
def home():
    return render_template(
        'home.html', RELEASE=release, VERSION=version
    )


@home_bp.route('/help')
def help():
    return render_template(
        'help.html', RELEASE=release, VERSION=version
    )
