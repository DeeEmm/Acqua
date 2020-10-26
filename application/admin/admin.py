from flask import Blueprint, render_template
from flask import current_app as app
from flask import redirect, url_for
import sqlite3


from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, DateTime
from flask import render_template
from flask import request
from flask import Blueprint
from flask import current_app as app
from flask import redirect
from markupsafe import escape
# from datetime import datetime

from application.trends.models import db
from application.trends.models import Trends
from application.trends.models import Trend_Data

release = app.config["RELEASE"]
version = app.config["VERSION"]


# Blueprint Configuration
admin_bp = Blueprint(
    'admin_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

# authentication needed


@admin_bp.route('/admin')
def admin():

    trends = Trends.query.all()
    trend_data = Trend_Data.query.all()

    return render_template(
        'admin.html', release=release, version=version,
        trends=trends, trend_data=trend_data
    )

# -[Admin Overview]------------------------------------------------------------

# -[General Settings]----------------------------------------------------------

# Example -  shell in file and get results
# https://stackoverflow.com/questions/53380988/how-to-execute-shell-script-from-flask-app


@admin_bp.route('/admin/general/shutdown')
def general_shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    # print(output)
    return render_template('shutdown.html')


@admin_bp.route('/admin/general/reboot')
def general_reboot():
    command = "/usr/bin/sudo reboot now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    # print(output)
    # print('rebooting...')
    return redirect("admin#tab-general-settings")

# -[Communication]-------------------------------------------------------------
# -[Nodes]---------------------------------------------------------------------
# -[GPIO]----------------------------------------------------------------------
# -[Control Schema]------------------------------------------------------------
# -[CRON Tasks]----------------------------------------------------------------
# -[Conditional Control]-------------------------------------------------------
# -[User Management]-----------------------------------------------------------
# -[Trend Data]----------------------------------------------------------------


@admin_bp.route('/admin/trends/add', methods=["GET", "POST"])
def trends_add():
    with app.app_context():
        if request.form:
            trend = Trends(
                description=request.form.get("description"),
                data_source=request.form.get("data_source"),
                min_value=request.form.get("min_value"),
                max_value=request.form.get("max_value"),
                unit_of_measure=request.form.get("unit_of_measure")
            )
            db.session.add(trend)
            db.session.commit()
        trend_data = Trend_Data.query.all()
        return redirect("admin#tab-trend-management")


@admin_bp.route("/admin/trends/delete", methods=["GET", "POST"])
def trends_delete():
    description = request.form.get("description")
    trend = Trends.query.filter_by(description=description).first()
    db.session.delete(trend)
    db.session.commit()
    trends = Trends.query.all()
    return redirect("admin#tab-trend-management")


@admin_bp.route("/admin/trends/set_default/<trend_id>", methods=["GET", "POST"])
def trends_set_default(trend_id=None):

    ###disable_trends = Trends.query.all()
    for row in Trends.query:  # all() is extra
        row.default = False

    trend = Trends.query.get(trend_id)
    trend.default = True
    db.session.add(trend)
    db.session.commit()

    ###trends = Trends.query.all()
    return redirect("admin#tab-trend-management")

# -[Event History]-------------------------------------------------------------

# -[Database management]-------------------------------------------------------


# Trends - id | type | description | unit
# Trend_data - id | trend_id | datetime | value
@admin_bp.route('/admin/database/reset')
def reset():
    conn = sqlite3.connect('acqua.db')
    conn.execute('\
        DROP TABLE IF EXISTS data_source\
    ;')
    conn.execute('\
        CREATE TABLE data_source (\
        id INTEGER PRIMARY KEY,\
        description TEXT\
    );')
    conn.execute('\
        DROP TABLE IF EXISTS trends\
    ;')
    conn.execute('\
        CREATE TABLE trends (\
            id INTEGER PRIMARY KEY,\
            description TEXT(80),\
            unit_of_measure TEXT(80),\
            data_source INT,\
            min_value REAL,\
            max_value REAL,\
            enabled BOOLEAN,\
            default BOOLEAN,\
            update_frequency INT\
        );'
    )
    conn.execute('\
        DROP TABLE IF EXISTS trend_data\
    ;')
    conn.execute('\
        CREATE TABLE trend_data (\
        id INTEGER PRIMARY KEY, \
        trend_id INT,\
        timestamp TEXT(80), \
        value REAL);')
    conn.close()
#    return redirect(url_for('admin_bp.admin'))   # just a test
    return render_template(
        'admin.html', RELEASE=release, VERSION=version
    )


@admin_bp.route('/admin/database')
def database():
    #  hello = request.args.get('hello') - how to decode extra arguments
    return render_template(
        'admin.html', RELEASE=release, VERSION=version
    )