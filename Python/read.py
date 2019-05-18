"""
This script uses tcpdump to capture VLP-32c data over Ethernet connection.
PCAP files generated can be playback in 3D with VeloView sotware.

A project of Ingenium (Wheaton College, IL).
Created by Ellie Tan, Rachel Barron.
Last revised February 2019.

"""

# import needed packages
import sys
import os
import time
import subprocess
import datetime
import func_ops as f

# convert command line inputs to variables
print('Command format: python {} <CaptureDuration(seconds)>'.format(sys.argv[0]))
if len(sys.argv) < 2:
    duration = 30 # default capture time for testing
    print('No duration specified, switching to default '+ str(duration)+ ' seconds.')

else:
    print('Duration is ' + str(sys.argv[1]) + ' seconds.')

# settings for recording data
buffersize = '524288' # not used for now
filesize = '100' # MB, max size 2048?
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
filepath = '/home/pi/' + timestamp + 'test.pcap'

# set Pi's ethernet IP address to anything but sensor's IP address
# see Velodyne manual for more information about this
ethernetIP = '192.168.1.123' # range 0-254
command = 'sudo ifconfig eth0 ' + ethernetIP + ' netmask 255.255.0.0'
os.system(command)

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

    # need to figure out better way to stop tcpdump
    # pause to capture data
    time.sleep(duration) # pause script 

    # terminate tcpdump process in background 
    print('Ending tcpdump process, please type ps -A to double check.')
    closecommand = 'sudo kill ' + str(process.pid)
    os.system(closecommand)

except:
    print('Error occured: Please check code and connections.')


print('Capture complete..Sending to connected drive')

# send data
# try wifi


# try bluetooth
# try connected device

# remember to submit your code changes by typing these commands:
# git add [filename(s) here or use '.' for everything]
# git commit (make comments on what you changed_
# git push (upload changes to master)

# NEXT STEPS:
# find best settings for buffer, filesize, use of -w loop
# Include push-button to stop and activate?
# Include LED blinking status with GPIO?
# next part of the script - to visualize?
