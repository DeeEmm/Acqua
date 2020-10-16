#!/bin/sh

# To run automatically on reboot - add to crontab
# @reboot sh /home/acqua/start.sh >/var/log/acqua.log 2>&1

cd /home/acqua

# Just install dependencies by default to pick up any changes
pip install -r requirements.txt

#
# run the data server
#

python3 wsgi.py &