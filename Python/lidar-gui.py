# a GUI script to run the LiDAR Sensor
# Ellie Tan, May 2019.

# import packages for GUI
from Tkinter import *
import tkMessageBox as msgbox
from ScrolledText import ScrolledText

# import packages for capturing data
import sys
import os
import time
import subprocess
import datetime
import func_ops as f

# Get wifi IP address
from subprocess import Popen, PIPE
pipe = Popen("ip route show | grep 'default' | awk '{print $3}' ",shell=True, stdout=PIPE).stdout
wifi_ip = pipe.read()
global wifi_ip

# Create window of app
window = Tk()
window.title("Ingenium LIDAR Controls")
window.geometry('720x480')

# add button status labels
ip = Label(window, text=wifi_ip,font=("Arial Bold",16))
ip.grid(column=0, row=0)

lbl = Label(window, text="Please click a button",font=("Arial Bold",16))
lbl.grid(column=1, row=1)

stat = Label(window, text="Status",font=("Arial Bold",16))
stat.grid(column=0, row=4)

# not sure how to get timer to work properly
#timer = Label(window,text="00:00",font=("Arial Bold",40))
#timer.grid(column=1,row=1)

# Add functions triggered by button click events
def init_clicked():
     lbl.configure(text="Initializing...",font=("Arial Bold",16))
     
     # initialize.py goes here
     try:
          execfile("initialize.py")
          lbl.configure(text="Initialize complete.",font=("Arial Bold",16))
     except:
          lbl.configure(text="Initialize failed.",font=("Arial Bold",16))
     
def go_clicked():
     lbl.configure(text="Capturing...",font=("Arial Bold",16))
     # execute tcpdump command
     
     # settings for recording data
     buffersize = '524288' # not used for now
     filesize = '1000' # MB, max size 2048?
     timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
     filepath = '/home/pi/' + timestamp + '.pcap'

     # set Pi's ethernet IP address to anything but sensor's IP address
     # see Velodyne manual for more information about this
     ethernetIP = '192.168.1.123' # range 0-254
     command = 'sudo ifconfig eth0 ' + ethernetIP + ' netmask 255.255.0.0'
     os.system(command)

     # begin data capture
     capturetxt = "Capture to " + filepath
     stat.configure(text=filepath,font=("Arial Bold",14))
     print(capturetxt)
     print('Target filesize ' + filesize + ' MB')
     
     try:
         # start subprocess to run tcpdump
         process = subprocess.Popen(['tcpdump','-i','eth0','-C',filesize,'-w',filepath], stdout=subprocess.PIPE)
         tcpdump_id = process.pid
         global tcpdump_id # make global variable
         print('Running process ' + str(process.pid) +' to capture data...')
     except:
         stat.configure(text="Failed to initiate tcpdump.",font=("Arial Bold",16))
         print('Failed to initiate tcpdump.')

def stop_clicked():
     response = msgbox.askyesno('Stop Warning','Are you sure you want to stop?')
     if response:
         lbl.configure(text="Stopped.",font=("ArialBold",16))
     
         # terminate tcpdump process in background 
         
         print('Ending tcpdump process, please type ps -A to double check.')
         closecommand = 'sudo kill ' + str(tcpdump_id)
         try:
            os.system(closecommand)
            stat.configure(text="Tcpdump capture ended.",font=("Arial Bold",16))
         except:
            stat.configure(text="Failed to end tcpdump process.",font=("Arial Bold",16))    
          
# add buttons
btn_font = "Arial Bold"
fontsize = 60

# define initialize button
init_btn = Button(window, text="Initialize",command=init_clicked,bg="yellow",font=(btn_font,fontsize))
init_btn.grid(column=0,row=1)

# define capture button
go_btn = Button(window,text="Capture",command=go_clicked,font=(btn_font,fontsize),bg="green")
go_btn.grid(column=0,row=2)

# define stop button
stop_btn = Button(window,text="Stop",command=stop_clicked,bg="red",font=(btn_font,fontsize))
stop_btn.grid(column=1,row=2)

# Add a status bar to show the output of script?
#status = ScrolledText(window,width=680,height=200)
#status.grid(column=0,row=3)

# starts window loop 
window.mainloop()
