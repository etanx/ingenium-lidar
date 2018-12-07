"""
This script uses tcpdump to capture VLP-32c data over Ethernet connection.
PCAP files generated can be playback in 3D with VeloView sotware.

A project of Ingenium (Wheaton College, IL).
Created by Ellie Tan, 20 Nov 2018.
"""

# import needed packages
import sys
import os
import time
import subprocess
import datetime

# convert command line inputs to variables
if len(sys.argv) < 2:
    print('Command format: python {} <CaptureDuration(seconds)>'.format(sys.argv[0]))
    duration = 10 # default capture time for testing
    print('No duration specified, switching to default '+ str(duration)+ ' seconds.')

# settings for recording data
buffersize = '524288' # not used for now
filesize = '100' # MB, max size 2048
timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
filepath = '/home/pi/' + timestamp + ' test.pcap'

# set ethernet IP address to anything but sensor's IP address
ethernetIP = '192.168.1.222'
command = 'sudo ifconfig eth0 ' + ethernetIP + ' netmask 255.255.255.0'
os.system(command)
print('\nEthernet IP set to ' + ethernetIP)

# begin data capture
print('Initiating tcpdump capture to ' + filepath)
print('Target filesize ' + filesize + ' MB')
print('Press Ctrl-C to quit.')

try:
    #this can also work, but harder to terminate tcpdump
    #command = 'sudo tcpdump -i eth0 -n -B ' + buffersize + ' -w ' + filepath +' -C ' + filesize
    #os.system(command)

    # start subprocess to run tcpdump
    process = subprocess.Popen(['tcpdump','-i','eth0','-C',filesize,'-w',filepath], stdout=subprocess.PIPE)
    print('Running process ' + str(process.pid) +' to capture data...')
    
    # pause to capture data
    time.sleep(duration)

    print('Ending tcpdump process, please type ps -A to double check.')
    
    # terminate the tcpdump process in the background
    closecommand = 'sudo kill ' + str(process.pid)
    os.system(closecommand)

except:
    print('Error occured: Make sure tcdump is installed and check code.')


print('Done.')


# NEXT STEPS:
# find best settings for buffer, filesize, use of -w loop
# Include push-button to stop and activate?
# Include LED blinking status with GPIO?
# next part of the script - to visualize?