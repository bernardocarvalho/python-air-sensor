#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 tw=0 et :
# https://github.com/ikalchev/py-sds011
########################################################
__author__ = "Bernardo Carvalho <bernardo.carvalho@tecnico.ulisboa.pt>"
__license__ = "GPL3"
__version__ = "1.0"

import csv, time, datetime
from sds011 import SDS011
sensor = SDS011("/dev/tty_airsensor", use_query_mode=True)
try:
    #with open("measurments.csv","w") as csvfile:
    with open("measurments.csv","a") as csvfile:
        log = csv.writer(csvfile, delimiter=',',quotechar="'") #, quoting=csv.QUOTE_MINIMAL)
        #logcols = ["timestamp","pm2.5","pm10","device_id"]
        logcols = ['timestamp','pm2_5','pm10']
        log.writerow(logcols)
        while True:
            sensor.sleep(sleep=False)  # Turn on fan and diode
            time.sleep(20)  # Allow time for the sensor to measure properly
            meas=sensor.query()  # Gets (pm25, pm10)
            sensor.sleep()  # Turn off fan and diode
            now = datetime.datetime.now()
            #vals = [str(now), meas] #  [str(meas.get(k)) for k in logcols]
            vals = [str(now)] + [str(i) for i in meas]
            log.writerow(vals)
            csvfile.flush()
            print(vals)
            # print(val2)
            time.sleep(280)  # Wait next 5 min cycle

except KeyboardInterrupt:
    sensor.sleep()  # Turn off fan and diode
    print("Ending!")
        #sds.sleep()
    #sds.__del__()

