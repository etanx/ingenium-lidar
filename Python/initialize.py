"""
CThis script uses PycURL to access the web interface
and resets Velodyne VLP-32c LiDAR over Ethernet connection.

A project of Ingenium (Wheaton College, IL).
Created by Ellie Tan
Last revised Feb 2019.

"""


#import needed packages
import pycurl # you will need to install this
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import urllib2
import json
import time
import os
import func_ops as f

#######################################################################

# function to send commands to sensor
def sensor_do(s,url,pf,buf):
    s.setopt(s.URL,url)
    s.setopt(s.POSTFIELDS,pf)
    s.setopt(s.WRITEDATA,buf)
    s.perform()
    rcode = s.getinfo(s.RESPONSE_CODE)
    success = rcode in range(200,207)
    print('%s %s: %d (%s)' % (url,pf,rcode,'OK' if success else'ERROR'))
    return success

#######################################################################

# default IP address of sensor
Base_URL ='http://192.168.1.201/cgi/'

# set ethernet IP address to anything but sensor's IP address
ethernetIP = '192.168.1.123' # range 0-254
command = 'sudo ifconfig eth0 ' + ethernetIP + ' netmask 255.255.0.0'
os.system(command)


# initiate pycurl website connection
sensor = pycurl.Curl()
buffer = BytesIO()

# NOTE: See Velodyne manual for list of commands to use
# reset sensor via web interface
rc = sensor_do(sensor,Base_URL+'reset',urlencode({'data':'reset_system'}),buffer)
print('Sensor re-starting...')

# if reset successful, set motor RPM and turn laser on
if rc:
    time.sleep(10)
    command = 'sudo ifconfig eth0 ' + ethernetIP + ' netmask 255.255.255.0'
    os.system(command)
    print('\nRe-set eth0 IP set to ' + ethernetIP)
    # specify motor RPM
    # valid motor RPM 300-1200, ideally in increments of 60.
    rc = sensor_do(sensor,Base_URL+'setting',urlencode({'rpm':'300'}),buffer)

if rc:
    time.sleep(1)
    # turn laser on
    rc = sensor_do(sensor,Base_URL+'setting',urlencode({'laser':'on'}),buffer)

if rc:
    time.sleep(10)

# get response from laser website and display status
response1 = urllib2.urlopen(Base_URL+'status.json')

if response1:
    status = json.loads(response1.read())
    print('Sensor laser is %s, motor RPM %s,\n GPS %s %s\n' % \
    (status ['laser']['state'],status['motor']['rpm'], \
    status['gps']['pps_state'],status['gps']['position']))

# get diagnostic data
response2 = urllib2.urlopen(Base_URL+'diag.json')

""" 
NOTE: there was an area with 'top' command

if response2:
    # convert data to temperature (see manual)
    status = json.loads(response2.read())
    temp = status['top']['lm20_temp']
    frac = temp * 5 /4096 
    celsius = -1481.96 + math.sqrt(2.1962*10^6+(1.8639 - frac)/3.88e-6)

    print 'Sensor temperature is %s Celsius\n' % (celsius)

    if celsius<-25 or celsius>90:
       print('Warning: Sensor beyond operating range -25 to 90 Celsius.') 
"""

sensor.close()




# REMEMBER to submit your code changes by typing these commands:

# git add [filename(s) here or use '.' for everything]
# git commit (make comments on what you changed_
# git push (upload changes to master)

