from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request
from flask import Blueprint
from flask import current_app as app
from flask import redirect

from application.trends.models import db
from application.trends.models import Trends
from application.trends.models import Trend_Data

# db.init_app(app)

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
            trend = Trends(description=request.form.get("description"))
#            trend = Trends(id='',trend_type=1,description=request.form.get("description"),unit_of_measure='rats')
            db.session.add(trend)
            db.session.commit()
        trends = Trends.query.all()
        return render_template("trends.html", trends=trends)


@trends_bp.route("/trends/update", methods=["POST"])
def update():
    with app.app_context():
        newdescription = request.form.get("newdescription")
        olddescription = request.form.get("olddescription")
        trend = Trends.query.filter_by(description=olddescription).first()
        trend.description = newdescription
        db.session.commit()
        return redirect("/trends")

@trends_bp.route("/trends/delete", methods=["GET", "POST"])
def delete():
    description = request.form.get("description")
    trend = Trends.query.filter_by(description=description).first()
    db.session.delete(trend)
    db.session.commit()
    trends = Trends.query.all()
    return render_template("trends.html", trends=trends)
