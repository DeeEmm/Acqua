from flask import Blueprint, render_template
from flask import current_app as app
from flask.ext.sqlalchemy import SQLAlchemy
# from application.admin.database import resetDB
from flask import request
from flask import Flask, redirect, url_for
import sqlite3

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


@admin_bp.route('/admin/<action>', methods=["GET", "POST"])
def database(action):
    #  hello = request.args.get('hello') - how to decode extra arguments
    return render_template(
        'admin.html', RELEASE=release, VERSION=version
    )

# Trends - id | type | description | unit
# Trend_data - id | trend_id | datetime | value
@admin_bp.route('/admin/reset')
def reset():
    conn = sqlite3.connect('acqua.db')
    conn.execute('DROP TABLE IF EXISTS trend_types;')
    conn.execute('CREATE TABLE trend_types (id INTEGER PRIMARY KEY, description TEXT);')
    conn.execute('DROP TABLE IF EXISTS trends;')
    conn.execute('CREATE TABLE trends (id INTEGER PRIMARY KEY, description TEXT(80), unit_of_measure TEXT(80), trend_type INT);')
    conn.execute('DROP TABLE IF EXISTS trend_data;')
    conn.execute('CREATE TABLE trend_data (id INTEGER PRIMARY KEY, trend_id INT, timestamp TEXT(80), value REAL);')
    conn.close()
    return redirect(url_for('admin_bp.admin')) # just a test
    