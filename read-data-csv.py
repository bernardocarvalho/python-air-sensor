#!/usr/bin/python3
# -*- coding: utf-8 -*-
########################################################
__author__ = "Bernardo Carvalho <bernardo.carvalho@tecnico.ulisboa.pt>"
__license__ = "GPL3"
__version__ = "1.0"
### RPI MPU9250
# https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect
#units of the MPU-9250
#Accelerometer	g (1g = 9.80665 m/s²)
#Gyroscope	degrees per second (°/s)
#Magnetometer	microtesla (μT) , Lisboa ~ 44 uT
#Temperature	celsius degrees (°C)
########################################################

#####################################################################
# Author: Jeferson Menegazzo                                        #
# Year: 2020                                                        #
# License: MIT                                                      #
#####################################################################

import sys
sys.path.append("")

import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

##################################################
# Create                                         #
##################################################

mpu = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
    address_mpu_slave=None, 
    bus=1, 
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

##################################################
# Configure                                      #
##################################################
mpu.configure() # Apply the settings to the registers.

##################################################
# Calibrate                                      #
##################################################
# mpu.calibrate() # Calibrate sensors
# mpu.configure() # The calibration function resets the sensors, so you need to reconfigure them

##################################################
# Get Calibration                                #
##################################################
# abias = mpu.abias # Get the master accelerometer biases
# gbias = mpu.gbias # Get the master gyroscope biases
# magScale = mpu.magScale # Get magnetometer soft iron distortion
# mbias = mpu.mbias # Get magnetometer hard iron distortion

# print("|.....MPU9250 in 0x68 Biases.....|")
# print("Accelerometer", abias)
# print("Gyroscope", gbias)
# print("Magnetometer SID", magScale)
# print("Magnetometer HID", mbias)
# print("\n")

##################################################
# Set Calibration                                #
##################################################
# mpu.abias = [0.16480683117378048, 0.08562190358231707, 0.043683307926829285] 
# ori [-0.08004239710365854, 0.458740234375, 0.2116996951219512]
# mpu.gbias = [1.3265842344702743, 0.091552734375, -0.2480483636623476]
# ori [0.8958025676448171, 0.45292551924542684, 0.866773651867378]
# mpu.magScale = [1.0104166666666667, 0.9797979797979799, 1.0104166666666667]
# mpu.mbias = [2.6989010989010986, 2.7832417582417586, 2.6989010989010986]

##################################################
# Show Values                                    #
##################################################
#while True:
   
print("|.....MPU9250 in 0x68 Address.....|")
print("Accelerometer", mpu.readAccelerometerMaster())
print("Gyroscope", mpu.readGyroscopeMaster())
print("Magnetometer", mpu.readMagnetometerMaster())
print("Temperature", mpu.readTemperatureMaster())
print("\n")

labels = mpu.getAllDataLabels() # return labels with data description for each array position
# ['timestamp', 'master_acc_x', 'master_acc_y', 'master_acc_z', 'master_gyro_x', 'master_gyro_y',
# 'master_gyro_z', 'slave_acc_x', 'slave_acc_y', 'slave_acc_z', 'slave_gyro_x', 'slave_gyro_y', 
# 'slave_gyro_z', 'mag_x', 'mag_y', 'mag_z', 'master_temp', 'slave_temp']

def write_csv_line(file, data, time0):
    #timestamp
    line = str(data[0]  -time0)+";" 
    #master_acc
    line = line +str(data[1])+';'+str(data[2]) + ';'+str(data[3])+';'
    #master_gyro
    line = line +str(data[4])+';'+str(data[5])+';'+str(data[6]) +';'
    #mag
    line = line +str(data[13])+';'+str(data[14])+';' + str(data[15]) +';'
    #master_temp
    line = line +str(data[16])+'\n' 
    file.write(line)

try:
# "w" overwrite
    f = open("mpudata.csv", "w")
    line =  'timestamp; acc_x; acc_y; acc_z; gyro_x; gyro_y; gyro_z; mag_x; mag_y; mag_z \n'
    f.write(line)
    time0 = time.time()
    for number in range(500):
        data = mpu.getAllData() # returns a array with data from all sensors
        write_csv_line(f, data, time0)

#    f.write("Now the file has more content!\n")
    f.close()
except KeyboardInterrupt:
    pass


