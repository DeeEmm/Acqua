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

import smbus2

release = app.config["RELEASE"]
version = app.config["VERSION"]

# Blueprint Configuration
nodes_bp = Blueprint(
    'nodes_bp',
    __name__,
    template_folder='template',
    static_folder='static',
    static_url_path='/nodes'
)


def i2c_address_list():
    # scan I2C network
    # Create array of Addresses
    # return array
    
    busNumber = 0  # 1 indicates /dev/i2c-1
    bus = smbus2.SMBus(busNumber)
    deviceCount = 0
    i2cList = []

    for device in range(0, 128):
        try:
            bus.write_byte(device, 0)
            # print("Found {0}".format(hex(device)))
            # i2cList[device - 3] = device
            i2cList.append(hex(device))
            deviceCount = deviceCount + 1
        except:
            # exception handler
            deviceCount = deviceCount + 1
    bus.close()
    bus = None

    return i2cList