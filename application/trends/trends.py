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
from markupsafe import escape

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


@trends_bp.route('/trend/<active_trend_id>')
def showtrend(active_trend_id):

    active_trend = Trends.query.filter_by(id=active_trend_id).first()
    trend_name = active_trend.description
    min_value = active_trend.min_value
    max_value = active_trend.max_value
    trends = Trends.query.all()
    trend_data = Trend_Data.query.filter_by(trend_id=active_trend_id).all()

    return render_template(
        "trends.html",
        trends=trends,
        trend_data=trend_data,
        trend_name=trend_name,
        release=release,
        version=version,
        max_value=max_value,
        min_value=min_value,
        active_trend_id=active_trend_id
    )


@trends_bp.route('/trends/')
def trends():

    default_trend = Trends.query.filter_by(default=True).first()
    active_trend_id = default_trend.id
    trend_name = default_trend.description
    min_value = default_trend.min_value
    max_value = default_trend.max_value

    trends = Trends.query.all()
    trend_data = Trend_Data.query.filter_by(trend_id=active_trend_id).all()

    return render_template(
        "trends.html",
        trends=trends,
        trend_data=trend_data,
        trend_name=trend_name,
        release=release,
        version=version,
        max_value=max_value,
        min_value=min_value,
        active_trend_id=active_trend_id
    )

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


@trends_bp.route("/trends/delete_value/<value_id>", methods=["GET", "POST"])
def delete(value_id):

    active_trend = Trend_Data.query.filter_by(id=value_id).all()
    active_trend_id = active_trend[0].trend_id

    trend_data = Trend_Data.query.filter_by(id=value_id).first()
    db.session.delete(trend_data)
    db.session.commit()
    trend_data = Trend_Data.query.all()
    return redirect(
        "/trend/" +  str(active_trend_id)
    )


@trends_bp.route("/trends/add_value/<active_trend_id>", methods=["GET", "POST"])
def add_data(active_trend_id=None):
    id=active_trend_id
    with app.app_context():
        if request.form:
            trend_data=Trend_Data(
                timestamp=func.now(),
                id=None,
                trend_id=active_trend_id,
                value=request.form.get("value")
            )
            db.session.add(trend_data)
            db.session.commit()
            trends = Trends.query.all()
            trend_data =Trend_Data.query.all()

            return redirect(
                "trend/" + id
            )

