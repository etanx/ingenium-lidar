# functions to capture pictures, videos for the Raspberry pi
# Elizabeth H. Tan, 2 Feb 2019

# PiCamera library docs
# http://picamera.readthedocs.io/


from picamera import PiCamera
import datetime
import os
import time

#############################################################################
#                               FUNCTIONS
#############################################################################

# Create an object class for each storage  drive
class StorageDrive:
	def __init__(self,name,path):

		self.name = name
		self.path = path
		# Try to open the USB drives, if you cannot open the drive, 
        #mark as not present and set size availabe as 0
		try:
			usb = os.statvfs(path)
			self.space = (usb.f_frsize * usb.f_bfree)/1024/1024
			self.present = 1
		except:
			self.space = 0
			self.present = 0



#############################################################################
#                               CONTROL PANEL
#############################################################################
 
vidlength = 10 # must be shorter than sampling interval
min_space = 50 # minimum space required (MB)

#camera settings (can be moved to a separate config.py file)
resolution = (1296,972)    # note: this affects field of view (FOV)
framerate = 30             # set as 15 if using max 2592x1944
whitebalance = 'auto'      # auto, cloudy, fluorescent etc
exposure = 'auto'		   # auto, nightpreview, verylong, beach etc
rotate = 180                  # rotate view

# see picamera documentation for best settings
# 
# ##############################################################################
#                          STORAGE MANAGEMENT
##############################################################################

# Thanks and credit to Fred Fourie 
# (https://hackaday.io/project/21222-pipecam-low-cost-autonomous-underwater-camera)

# List all USB ports
usb = []
usb.append(StorageDrive('usb1','/mnt/usb1'))
usb.append(StorageDrive('usb2','/mnt/usb2'))
usb.append(StorageDrive('usb3','/mnt/usb3'))
usb.append(StorageDrive('usb4','/mnt/usb4'))


# Decide where to save the files first, external or local
save_on_removable = 1 # Record on external drives by default (1)
min_space = 30 	  # What is the minimum space in MB which can be considered for recording

# create a list of available drives with space
availableDrives = [u for u in usb if u.space > min_space]

# if the amount of available drives is 0, do not try to save on the external
save_on_removable = 0 if len(availableDrives) == 0 else 1


# quit script is local and external drives full
local = StorageDrive('root','/')
if local.space < min_space and availableDrives == 0:
	print("All drives are full")
	sys.exit() # quit Python!

# If all has space, set the destination path and continue
if save_on_removable == 1 and len(availableDrives) != 0:
	filepath = availableDrives[0].path
	#print('\nUSB Storage = ' + str(usb.space) + ' MB') # need something to show space?
else:
	filepath = "/home/pi/camera"
	command = 'mkdir ' + filepath
	os.system(command) # make sure storage folder exists
	print('\nStorage available = ' + str(local.space) + ' MB')
	print('Saving to ' + filepath)
	print('')

##############################################################################
#                          BEGIN DATA COLLECTION
##############################################################################
# eventually making pic and vid into functions would make this robust?
# I have a script somewhere but it's so long and intertangled so... anyway
# or add feature where you can specify the number of images to capture 
# as well as an interval to pause between shots with time.sleep()

# controls to capture
pic = 1
vid = 0

# open camera and preset parameters
camera = PiCamera()
camera.resolution = resolution
camera.framerate = framerate
camera.rotation = rotate

# activate sensor and set additional params
camera.start_preview()
camera.exposure_mode = exposure
camera.awb_mode = whitebalance
settings = 'Exp:' + exposure + ' WB:' + whitebalance # for image annotation
date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

if vid == 1:  
    # capture video
    camera.start_recording( filepath + '/vid_' + date[2:17] + '.h264')
    print("Started recording video...")

    # this loop is just to write datetime on every other video frame 
    while (datetime.datetime.now() - start).seconds < vidlength:
    	camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.wait_recording(0.2)

    camera.stop_recording()
    print('Saved vid' + date[2:17] + '.h264')

if pic ==1:
    # capture image
    #camera.annotate_text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
    camera.capture( filepath + '/img' + date[2:17] + '.jpeg')
    print('Saved img' + date[2:17] + '.jpeg')


# deactivate sensor and close camera
camera.stop_preview() 
camera.close()

print('\n')

