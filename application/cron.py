from flask import Blueprint, render_template
from flask import current_app as app
from flask import redirect, url_for
import sqlite3

from application.trends import trends
from application.control import control

from application.trends.models import db
from application.trends.models import Trends
from application.trends.models import Trend_Data

# NOTE: This file is fired from system cron at (nominal) 1 min interval

release = app.config["RELEASE"]
version = app.config["VERSION"]


# Blueprint Configuration
cron_bp = Blueprint(
	'cron_bp', 
	__name__,
	template_folder='templates',
	static_folder='static'
)





# NOTE: Do we need separate API controller????

# CRON Endpoint
@cron_bp.route('/cron/execute')
def cron_execute():


	# Trends
	# Call Trends 'CRON' handler
	if trends.cron_tasks():
		trends_cron = 'Success'
	else:
		trends_cron = 'Failed'


	# Control
	# Call control 'CRON' handler
	if control.cron_tasks():
		control_cron = 'Success'
	else:
		control_cron = 'Failed'
	
	return render_template(
		'cron.html', release=release, version=version, trends_cron = trends_cron, control_cron = control_cron
	)



# Time decode
# for date based: is datetime within one minute of current datetime?
# for 5 minute intervals is Minute divisible by 5? 
# for 10 minute intervals is minute divisible by 10
# for hourly intervals is timedate within 1 minute?
# etc. 
# For all other time frequencies.

# frequency fields need to be aligned for both trends and control 
# this way a common time decode function can be used here for both functions!!!
