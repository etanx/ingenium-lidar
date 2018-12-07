
# or this method using tcdump to capture packets over ethernet
import os
import time
import subprocess

buffersize = '524288'
filesize = '2048'
filepath = '/home/pi/velodyne/' + 'test.pcap'

print('\nInitiating tcpdump capture to ' + filepath)
print('Press Ctrl-C to quit.')

try:
    #command = 'sudo tcpdump -i eth0 -n -B ' + buffersize + ' -w ' + filepath +' -C ' + filesize
    #os.system(command)

    #command = 'sudo tcpdump -i eth0 -C 100 -w test'
    process = subprocess.Popen(['tcpdump','-i','eth0','-C','50','-w','/home/pi/velodyne/test.pcap'], stdout=subprocess.PIPE)
    print('Starting process ' + str(process.pid))

    time.sleep(10)

    print('Attempting to kill tcpdump process, please type ps -A to check process')

    closecommand = 'sudo kill ' + str(process.pid)
    os.system(closecommand)

except KeyboardInterrupt:
    print('Recording stopped.')



###########################################################
"""
# Another method which has not been tested due to pyshark install errors
import pyshark


#capture = pyshark.RemoteCapture('192.168.1.101','eth0')
capture = pyshark.LiveCapture(interface='eth0')
capture.sniff(timeout=50)
capture

# not sure what this section is for
#<LiveCapture (5 packets)>
#capture[3]
#<UDP/HTTP Packet>

for packet in capture.sniff_continuously(packet_count=5):
    print('Just arrived:', packet)

"""
