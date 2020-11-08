from flask import Blueprint, render_template
from flask import current_app as app
from flask_nav.elements import View


# Control - CRON function - called from CRON.PY
# Interrogate Control database and generate list of control actions to be undertaken.
# time decode - do we need to do it now?
# read realtime clock and compare
# Is time decode part of SQL Query? SELECT WHERE timeofcall >= datetime('now', '-1 minutes')
# https://www.tutorialspoint.com/sqlite/sqlite_date_time.htm
# https://kimsereyblog.blogspot.com/2016/06/nice-features-and-tricks-with-sqlite.html
# Parse control list and perform control actions (whatever they may be) 
# NOTE: need to take a look at stacked actions - where input to control action is reliant on output from previous action.
# we may need to store a result from the output of the control action and then use this in subsequent calls
# this result can be displayed in admin panel for each control action in datatable format (borrow layout form trends)
# this would also require that actions are parsed prior to the result being required.
# so essentially we need to parse control criteria based on the type of output it has.
# this may even need to be expanded into a priority / hierarchical based system where results are obtained in order.
# [NOTE: Should this be in CONTROL!!!]




release = app.config["RELEASE"]
version = app.config["VERSION"]


# Blueprint Configuration
control_bp = Blueprint(
	'control_bp', 
	__name__,
	template_folder='templates',
	static_folder='static'
)


@control_bp.route('/control')
def control():
	return render_template(
		'control.html', release=release, version=version
	)
	
	
def cron_tasks():
    # Trends - CRON function - called from CRON.PY
    # Interrogate Trend database table and generate list of trends/nodes to update (array of Trend IDs/nodes)
    # time decode - do we need to do it now?
    # read realtime clock and compare
    # Is time decode part of SQL Query? SELECT WHERE timeofcall >= datetime('now', '-1 minutes')
    # https://www.tutorialspoint.com/sqlite/sqlite_date_time.htm
    # https://kimsereyblog.blogspot.com/2016/06/nice-features-and-tricks-with-sqlite.html
    # should we just update all trends at set frequency? (1 min)
    # Parse Trend list and read data from Nodes - save data to trend_data table
    # [NOTE: Should this be in TRENDS!!!]
    with app.app_context():
        # trend_data = Trend_Data.query.filter_by(id=1).first()
        newvar = release
        # create array of trends to be updated
        return False
