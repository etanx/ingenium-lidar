#import the mscl library
import sys
sys.path.append("../../dependencies/Python")
import mscl
import subprocess
import datetime
import os
import time

COM_PORT = "/dev/ttyACM0"
filesize = '250000'
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
filepath = '/home/pi/' + timestamp +'IMU.pcap'
print(filepath)
command = 'sudo modprobe usbmon'
os.system(command)

try:
    #create a Serial Connection with the specified COM Port, default baud rate of 921600
    connection = mscl.Connection.Serial(COM_PORT)

    #create an InertialNode with the connection
    node = mscl.InertialNode(connection)

    #many other settings are available than shown below
    #reference the documentation for the full list of commands

    #if the node supports AHRS/IMU
    if node.features().supportsCategory(mscl.MipTypes.CLASS_AHRS_IMU):
        node.enableDataStream(mscl.MipTypes.CLASS_AHRS_IMU)

    #if the node supports Estimation Filter
    if node.features().supportsCategory(mscl.MipTypes.CLASS_ESTFILTER):
        node.enableDataStream(mscl.MipTypes.CLASS_ESTFILTER)

    #if the node supports GNSS
    if node.features().supportsCategory(mscl.MipTypes.CLASS_GNSS):
        node.enableDataStream(mscl.MipTypes.CLASS_GNSS)

except mscl.Error: #, e:
    print ("Error:")#, e



ahrsImuChs = mscl.MipChannels()
ahrsImuChs.append(mscl.MipChannel(mscl.MipTypes.CH_FIELD_SENSOR_SCALED_ACCEL_VEC, mscl.SampleRate.Hertz(500)))
ahrsImuChs.append(mscl.MipChannel(mscl.MipTypes.CH_FIELD_SENSOR_SCALED_GYRO_VEC, mscl.SampleRate.Hertz(100)))

estFilterChs = mscl.MipChannels()
estFilterChs.append(mscl.MipChannel(mscl.MipTypes.CH_FIELD_ESTFILTER_ESTIMATED_GYRO_BIAS, mscl.SampleRate.Hertz(100)))

# set the active channels for the AHRS/IMU class on the Node
node.setActiveChannelFields(mscl.MipTypes.CLASS_AHRS_IMU, ahrsImuChs)
node.setActiveChannelFields(mscl.MipTypes.CLASS_ESTFILTER, estFilterChs)

#ADD SECOND option!!!
#node.resume()

response = node.ping()
print(response)
#try set up pcap
try: 
    process = subprocess.Popen(['tcpdump','-i','usbmon1','-C',filesize,'-w',filepath], stdout=subprocess.PIPE)
    print('Running process ' + str(process.pid) +' to capture data...')

except:
    subprocess.Popen.kill(process)
    print("error: Popen")

for i in range(100):
    packets = node.getDataPackets(3000)
    print("Packets: ", packets.size())
    for packet in packets:
        packet.descriptorSet()
        points = packet.data()
        #print("\nData Points: ",packet.data().size())
        for dataPoint in points:
            #print("\n",dataPoint.channelName())
            dataPoint.channelName()
            dataPoint.storedAs()
            dataPoint.as_float()
node.setToIdle()
time.sleep(2)
subprocess.Popen.kill(process)            

