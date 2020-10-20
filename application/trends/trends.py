from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, DateTime
from flask import render_template
from flask import request
from flask import Blueprint
from flask import current_app as app
from flask import redirect
# from datetime import datetime

from application.trends.models import db
from application.trends.models import Trends
from application.trends.models import Trend_Data

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


@trends_bp.route('/trends', methods=["GET", "POST"])
def trends():
    with app.app_context():
        if request.form:
            trend = Trends(
                description=request.form.get("description"),
                trend_type=request.form.get("trend_type"),
                unit_of_measure=request.form.get("unit_of_measure")
            )
            db.session.add(trend)
            db.session.commit()
        trends = Trends.query.all()
        trend_data = Trend_Data.query.all()
#        trend_data = Trend_Data.query\
#        .join(Trends, Trend_Data.id==Trends.id)\
#        .add_columns(Trend_Data.trend_id, Trend_Data.timestamp, Trend_Data.value, Trends.unit_of_measure, Trends.trend_type)\
#        .filter(Trend_Data.id == Trends.id)\

        return render_template("trends.html", trends=trends,
        trend_data=trend_data, release=release, version=version)


@trends_bp.route("/trends/update", methods=["POST"])
def update():
    with app.app_context():
        newdescription = request.form.get("newdescription")
        olddescription = request.form.get("olddescription")
        trend = Trends.query.filter_by(description=olddescription).first()
        trend.description = newdescription
        db.session.commit()
        return redirect("\
        /trends", trends=trends, release=release, version=version)


@trends_bp.route("/trends/delete", methods=["GET", "POST"])
def delete():
    description = request.form.get("description")
    trend = Trends.query.filter_by(description=description).first()
    db.session.delete(trend)
    db.session.commit()
    trends = Trends.query.all()
    return redirect("/trends", trends=trends, release=release, version=version)


@trends_bp.route("/trends/add_data", methods=["GET", "POST"])
def add_data():
    with app.app_context():
        if request.form:
            trend_data=Trend_Data(
                timestamp=func.now(),
                id=None,
                trend_id=request.form.get("trend_id"),
                value=request.form.get("value")
            )
            db.session.add(trend_data)
            db.session.commit()
            trends = Trends.query.all()
            trend_data =Trend_Data.query.all()
#            trend_data = Trend_Data.query\
#            .join(Trend_Data, Trends.id==Trend_Data.id)\
#            .add_columns(Trend_Data.trend_id, Trend_Data.timestamp, Trend_Data.value, Trends.unit_of_measure, Trends.trend_type)\
#            .filter(Trend_Data.id == Trends.id)\

            return render_template("trends.html", trends=trends,
            trend_data=trend_data, release=release, version=version)
