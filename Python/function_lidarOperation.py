"""
This script contains useful functions (such as setting the ethernet address)
to avoid overwriting information

A project of Ingenium (Wheaton College, IL).
Created by Rachel Barron Feb 15, 2019
Last Revised Feb 15, 2019
"""
import os

#Set ethernet IP address to anything but the sensor's IP address
def setEthernet():
    ethernetIP = '192.168.1.1222'
    command = 'sudo ifconfig eth0 ' + ethernetIP + ' netmask 255.255.255.0'
    os.system(command)
    print('\nEthernet IP is set to ' + ethernetIP)
    return(ethernetIP)
