"""Setup.py: setup communication between IMU and Pi 
Authors: Ruby Burgess, Rachel Barron
Date last modified: 02/19/2020
"""

import mscl
import serial


#scan ports for IMU connection and set port connection 
port= "/dev/ttyACM0"
#next steps: find data rate from user manual (see slack for help)

#need to figure out what COM3 is

connection = mscl.Connection.Serial(port)
node = mscl.InertialNode(connection)
success = node.ping()
node.setToIdle

ahrsImuChs = mscl.MipChannels()
ahrsImuChs.append(mscl.MipChannel(mscl.MipTypes.CH_FIELD_SENSOR_RAW_ACCEL_VEC, mscl.SampleRate.Hertz(500)))
ahrsImuChs.append(mscl.MipChannel(mscl.MipTypes.CH_FIELD_SENSOR_RAW_GYRO_VEC, mscl.SampleRate.Hertz(100)))

estFilterChs = mscl.MipChannels()
estFilterChs.append(mscl.MipChannel(mscl.MipTypes.CH_FIELD_ESTFILTER_ESTIMATED_GYRO_BIAS, mscl.SampleRate.Hertz(100)))

node.setActiveChannelFields(mscl.MipTypes.CLASS_AHRS_IMU, ahrsImuChs)
node.setActiveChannelFields(mscl.MipTypes.CLASS_ESTFILTER, estFilterChs)

node.enableDataStream(mscl.MipTypes.CLASS_AHRS_IMU)

node.resume()

node = mscl.InertialNode(connection)





connection = mscl.Connection.Serial(COM3, port)
node = mscl.DisplacementNode(connection)
success = node.ping()
node.setToIdle()
node.setDeviceTime
node.resume()

node = mscl.DisplacementNode(connection)

while True:

    packets = node.getDataPackets(500)

    for packet in packets:
        packet.descriptorSet()
        packet.timestamp()

