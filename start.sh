#!/bin/sh

# To run automatically on reboot - add to crontab 
# crontab-e
# add the following line:
# @reboot sh /home/acqua/start.sh >/var/log/acqua.log 2>&1

cd /home/acqua

# Lets install dependencies by default to pick up any changes 
# (uncomment for distribution)
# pip install -r requirements.txt

# where's our configuration file?
export APP_CONFIG_FILE=config.py

# run the data server (opens on port 80)
python3 wsgi.py &