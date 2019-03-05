"""
This script contains useful functions (such as setting the ethernet address)
to avoid overwriting information

A project of Ingenium (Wheaton College, IL).
Created by Rachel Barron Feb 15, 2019
Last Revised Feb 15, 2019
"""
import os
import numpy as np
import socket
import ipaddress
#Set ethernet IP address to anything but the sensor's IP address
def setEthernet():
    ethernetIP = '192.168.1.1222'
    command = 'sudo ifconfig eth0 ' + ethernetIP + ' netmask 255.255.255.0'
    os.system(command)
    print('\nEthernet IP is set to ' + ethernetIP)
    return(ethernetIP)
def setWifi():
    net4 = ipaddress.ip_network('192.0.2.0/24')
    for x in net4.hosts():
        if x in net4:
            ipAddr = x
            break
    return(ipAddr)
# need to actually change the IP if it's invalid (in use). Also make sure
# that this is checking to make sure the IP is unique. Also, makes sure the IP
# has not already been set. If it has, use that one
class export:
    def __init__(self,file): 
        self.file = file
    def wifi(self):
        #TCP_IP =  call the IP generator
        TCP_PORT = 5005
        BUFFER_SIZE = 1024
        MESSAGE = self.file
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        data = s.recv(BUFFER_SIZE)
        s.close()
        print("received data:", data)
