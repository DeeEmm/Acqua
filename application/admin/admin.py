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


@admin_bp.route('/admin')
def admin():
    
    
    trends = Trends.query.all()
    trend_data = Trend_Data.query.all()
    
    
    
    return render_template(
        'admin.html', release=release, version=version,
        trends=trends, trend_data=trend_data
    )




# -[General Settings]-----------------------------------------------------------
# -[Communication]--------------------------------------------------------------
# -[Nodes]----------------------------------------------------------------------
# -[GPIO]-----------------------------------------------------------------------
# -[Control Schema]-------------------------------------------------------------
# -[CRON Tasks]-----------------------------------------------------------------
# -[Conditional Control]--------------------------------------------------------
# -[User Management]------------------------------------------------------------
# -[Trend Data]-----------------------------------------------------------------

@admin_bp.route('/admin/trends/add', methods=["GET", "POST"])
def trends_add():
    with app.app_context():
        if request.form:
            trend = Trends(
                description=request.form.get("description"),
                trend_type=request.form.get("trend_type"),
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

            
            
# -[Event History]--------------------------------------------------------------

# -[Database management]--------------------------------------------------------


# Trends - id | type | description | unit
# Trend_data - id | trend_id | datetime | value
@admin_bp.route('/admin/database/reset')
def reset():
    conn = sqlite3.connect('acqua.db')
    conn.execute('DROP TABLE IF EXISTS trend_types;')
    conn.execute('CREATE TABLE trend_types (\
        id INTEGER PRIMARY KEY, description TEXT);')
    conn.execute('DROP TABLE IF EXISTS trends;')
    conn.execute('CREATE TABLE trends (\
        id INTEGER PRIMARY KEY, description TEXT(80), \
        unit_of_measure TEXT(80), trend_type INT);')
    conn.execute('DROP TABLE IF EXISTS trend_data;')
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