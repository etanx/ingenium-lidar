## Using Tcpdump in Python to Capture data
The small Raspberry Pi 3 will be used for the main purpose of recording sensor data in the field, since data visualization will be done on a more powerful computer.

# Initialize Sensor
This script resets the sensor and defines motor and laser settings. You can also access the web interface by typing 192.168.1.201 (default sensor IP) in the browser.

Install needed Python packages: `pycurl, urllib, urllib2, json`. To reset the sensor and show diagnostic settings, type the command:
```
sudo python initialize.py
```

# Capture Data (.pcap files)
Make sure tcpdump is installed. If not type:
```
sudo apt-get install tcpdump
```
To record .pcap files for later visualization, navigate to the folder with the script,type the command below, and input the optional record duration in seconds:
```
sudo python read.py <30>
```

# Data Visualization
PCAP files generated can be playback in 3D with the open-source (free!) VeloView sotware.