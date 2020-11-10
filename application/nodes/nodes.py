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

from application.nodes.models import db
from application.nodes.models import Nodes

import smbus2
import time


from smbus2 import SMBus, i2c_msg, SMBusWrapper

RELEASE = app.config["RELEASE"]
VERSION = app.config["VERSION"]
I2C_BUS = app.config["I2C_BUS"]

# Blueprint Configuration
nodes_bp = Blueprint(
    'nodes_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/nodes'
)


@nodes_bp.route('/nodes/test')
def nodes():
    data = ''
    data_length = 10
    node_address = int(0x38) # decimal: 56
    
    request = {0x33};

    # Single transaction writing two bytes then read two at address 80
    write = i2c_msg.write(node_address, request)
    read = i2c_msg.read(node_address, 10)
    with SMBusWrapper(I2C_BUS) as bus:
        bus.i2c_rdwr(write, read)
        data = list(read)
#        bus.close()

    time.sleep(0.5)

    return render_template(
        "nodes.html",
        data=repr(data),
        RELEASE=RELEASE,
        VERSION=VERSION
    )

    

def i2c_address_list():
    # scan I2C network
    # Create array of Addresses
    # return array
    
    busNumber = I2C_BUS  # 1 indicates /dev/i2c-1
    bus = smbus2.SMBus(busNumber)
    deviceCount = 0
    i2cList = []

    for device in range(0, 128):
        try:
            bus.write_byte(device, 0)
            i2cList.append(hex(device))
            deviceCount = deviceCount + 1
        except:
            # exception handler
            deviceCount = deviceCount + 1
    bus.close()
    bus = None

    return i2cList