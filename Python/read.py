"""
# maybe try this method if we can figure it out
import socket
import subprocess

UDP_IP = "192.168.1.201" #sensor IP?
UDP_PORT = 9933

sock = socket.socket(socket.AF_INET, # Internet
socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
  data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
  print "received message:", data
subprocess.call(data.split())
"""
##################################################################

# or this method using tcdump to capture packets over ethernet
import os
import time

buffersize = '524288'
filesize = '2048'
filepath = 'LiDAR/' + 'velodyne.pcap'

print('\nInitiating tcpdump capture to ' + filepath)
print('Press Ctrl-C to quit.')

try:
    command = 'sudo tcpdump -i eth0 -n -B ' + buffersize + ' -w ' + filepath +' -C ' + filesize
    os.system(command)
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
