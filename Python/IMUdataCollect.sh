#!/bin/bash
#Before this can be used, you need to check the filepath to the script capturing the IMU data. It's probably not this one since I don't actually have access to that .py file right now :)Happy LiDARing! It's a fun project!
ts=`date +"%Y%m%d%H%M%s"`
sudo ~/pi/lidar/IMU/readIMU.py | tee -a data_$ts.txt