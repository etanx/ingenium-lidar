#!/bin/bash

# A script to run ros to convert PCAP to BAG files in command line language.
# make script executable by typing 'sudo chmod +x rosconvert.sh' at first run
# Elizabeth H. Tan, 17 Feb 2019.

# To run this file, type 'sh filename.sh'

echo "Please install ROS and edit PCAP file path first!"

# run this in first tab to start ROS
#roscore

# run in second tab to open pcap
#rosrun velodyne_driver velodyne_node _model:=VLP16 _pcap:=/path/to file.pcap

# run in third tab to save bag file
#rosrun rosbag record -O vlp_16.bag /velodyne_packets


