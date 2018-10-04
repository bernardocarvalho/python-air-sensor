#!/usr/bin/python3
# -*- coding: utf-8 -*-
#https://github.com/custom-build-robots/Feinstaubsensor/blob/master/web_feinstaub_bme280.py
########################################################
__author__ = "Bernardo Carvalho <bernardo.carvalho@tecnico.ulisboa.pt>"
__license__ = "GPL3"
__version__ = "1.0"
#https://github.com/edwork/RPI-MQTT-JSON-Multisensor/blob/master/multisensor.py
### RPI-MQTT-JSON-Multisensor
#
#
########################################################

import serial, time, struct
import os, sys
import csv
import json
import paho.mqtt.publish as publish

#Sensor Libraries
import sds011
import Adafruit_DHT
#https://pypi.org/project/RPi.bme280/
import smbus2
import bme280

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

## Configuration
# MQTT Server Information
#MQTT_HOST = 'epics.ipfn.ist.utl.pt'
MQTT_HOST = 'mqtt.dioty.co'
MQTT_PORT = 1883
#MQTT_USER = 'ist'
#MQTT_PASSWORD = 'isttok'
MQTT_USER = 'bernardo.brotas@gmail.com'
MQTT_PASSWORD = '995ef6b2'
MQTT_CLIENT_ID = 'pi-sensor-1'
MQTT_TOPIC_PREFIX = '/bernardo.brotas@gmail.com/air-quality/lx/aveua'
#MQTT_TOPIC_PREFIX = 'ipfn/pisensornode/air'
## Sensor Information
#TEMP_SENSOR_PIN = 17 ## GPIO PIN
DHT_SENSOR_PIN = 4 ## GPIO PIN

## Setup
sensor_data = {}
auth_info = {
  'username':MQTT_USER,
  'password':MQTT_PASSWORD
  }

global dir_path
dir_path = "/home/pi/particles/"

def write_log(msg):
    global dir_path
    message = msg
    fname = dir_path+"particle_python_program.log"
    #fname = "/home/pi/feinstaub/feinstaub.log"
    with open(fname,'a+') as file:
        file.write(str(message))
        file.write("\n")
        file.close()	

def write_csv(time, pm_25, pm_10, temp, humidity, temp2, pressure, fname):

    with open(fname,'a') as file:
        line = ""+str(time)+";"+str(pm_25)+";"+str(pm_10)+";"+str(temp)+";"+str(humidity)+';'
        line = line +str(temp2)+';'+str(pressure)
        file.write(line)
        file.write('\n')
        file.close()

# Try to attach serial port to Particle Sensor vlues
try:
    #sensor = sds011.SDS011("/dev/ttyAMA0", use_query_mode="True")
    sensor = sds011.SDS011("/dev/ttyUSB0", use_query_mode="True")
except Exception as e:
    write_log(e)

rpr=sensor.query()
print(rpr)
pm_25, pm_10 = sensor.query()
#print "PM 2.5:",pm_25,"μg/m^3  PM 10:",pm_10,"μg/m^3"
print("PM 2.5:{} μg/m^3  PM 10:{} μg/m^3".format(pm_25, pm_10))
#print(".  appears {} times.".format(i, key, wordBank[key]))

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensorDHT = Adafruit_DHT.DHT22

# Example using a Raspberry Pi with DHT sensor
# connected to GPIO4.
#pin = 4

humidity, temperature = Adafruit_DHT.read_retry(sensorDHT, DHT_SENSOR_PIN)
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
data = bme280.sample(bus, address, calibration_params)

# the compensated_reading class has the following attributes
print(data.id)
print(data.timestamp)
print(data.temperature)
print(data.pressure)
print(data.humidity)

# there is a handy string representation too
print(data)

try:
    while True:
        data = bme280.sample(bus, address, calibration_params)
        humidity, temperature = Adafruit_DHT.read_retry(sensorDHT, DHT_SENSOR_PIN)
        try:
            humidity = round(humidity, 3) ## Round to 3 places
            temperature = round(temperature, 3) ## Round to 3 places
            pm_25, pm_10 = sensor.query()
            sensor_data['temperature'] = temperature
            sensor_data['humidity'] = humidity
            sensor_data['pm_25'] = pm_25
            sensor_data['pm_10'] = pm_10
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
            write_csv(data.timestamp, pm_25, pm_10, temperature, humidity, data.temperature, data.pressure, "sensor.log")
            ## Publish the message to the MQTT Broker
            publish.single(MQTT_TOPIC_PREFIX,
                        json.dumps(sensor_data),
                        hostname = MQTT_HOST,
                        client_id = MQTT_CLIENT_ID,
                        auth = auth_info,
                        port = MQTT_PORT
                       )
        except TypeError:
            print("TypeError!")
        except:
            print("Unexpected error:", sys.exc_info()[0])
        time.sleep(10)
except KeyboardInterrupt:
    pass

