#!/usr/bin/python3
#https://github.com/custom-build-robots/Feinstaubsensor/blob/master/web_feinstaub_bme280.py

import serial, time, struct
import os
import csv

#Sensor Libraries
import sds011
import Adafruit_DHT
#https://pypi.org/project/RPi.bme280/
import smbus2
import bme280

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
pin = 4

humidity, temperature = Adafruit_DHT.read_retry(sensorDHT, pin)
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
	
while True:
    time.sleep(10)
    data = bme280.sample(bus, address, calibration_params)
    humidity, temperature = Adafruit_DHT.read_retry(sensorDHT, pin)
    pm_25, pm_10 = sensor.query()
    try:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    except TypeError:
...     print("Oops!")
    write_csv(data.timestamp, pm_25, pm_10, temperature, humidity, data.temperature, data.pressure, "sensor.log")

