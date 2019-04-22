# VeloDyne VLP-32c LiDAR Mapping by Ingenium

Ingenium project for scanning and 3D visualization with the Velodyne VLP-32c LiDAR "Ultra-Puck" sensor. Ingenium's goal is to use a Raspberry Pi 3 for recording data via Ethernet, then 3D-reconstruct excavation sites with SLAM algorithm's mapping.

## Raspberry Pi 3 Setup 
The small Raspberry Pi 3 will be used for the main purpose of recording sensor data in the field, since data visualization will be done on a more powerful computer. Install git on your device and clone this repository:
```
sudo apt-get install git
sudo apt-get update
sudo apt-get upgrade
git clone https://github.com/etanx/ingenium-lidar.git
```
To navigate to the folder in terminal, change directory with:
```
cd /home/pi/ingenium-lidar
```
Install needed Python packages for our scripts: `pycurl, urllib, urllib2, json`. Our script uses `tcpdump` to capture data packets over the Ethernet connection to the sensor, so make sure to install that as well.

## Data Capture
We currently use Python scripts in operations. To run a script, type `sudo python scriptname.py` in the command line.

### initialize.py
This script resets the sensor and defines motor and laser settings. You can also access the web interface by typing 192.168.1.201 (default sensor IP) in a browser.

### read.py
This initiates tcpdump to capture data packets coming in fromt the eth0 (ethernet) port. Stopping the Python script does tnot stop the tcpdump process, so the script uses a method to specifically kill the tcpdump process.

## (Geo)Mapping and SLAM
Work in progress.


Project Log for Team Members (https://goo.gl/cQuSM1)








 To reset the sensor and show diagnostic settings, type the command:
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
