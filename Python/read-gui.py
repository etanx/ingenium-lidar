# a GUI script to run the LiDAR Sensor
# Ellie Tan, May 2019.

from Tkinter import *
import tkMessageBox as msgbox
from ScrolledText import ScrolledText
import time

window = Tk()
window.title("LIDAR Runner")
window.geometry('720x480')

# add status labels
lbl = Label(window, text="Please click a button",font=("Arial Bold",16))
lbl.grid(column=1, row=1)

# not sure how to get timer to work properly
#timer = Label(window,text="00:00",font=("Arial Bold",40))
#timer.grid(column=1,row=1)

# Add button click events
def init_clicked():
     lbl.configure(text="Initialize...",font=("Arial Bold",16))

def go_clicked():
     lbl.configure(text="Capturing...",font=("Arial Bold",16))
     # execute tcpdump command

def stop_clicked():
     response = msgbox.askyesno('Stop Warning','Are you sure you want to stop?')
     if response:
         lbl.configure(text="Stopped.",font=("ArialBold",16))
         #kill tcpdump process and display text

# add buttons
btn_font = "Arial Bold"
fontsize = 60

init_btn = Button(window, text="Initialize",command=init_clicked,bg="yellow",font=(btn_font,fontsize))
init_btn.grid(column=0,row=1)

go_btn = Button(window,text="Capture",command=go_clicked,font=(btn_font,fontsize),bg="green")
go_btn.grid(column=0,row=2)

stop_btn = Button(window,text="Stop",command=stop_clicked,bg="red",font=(btn_font,fontsize))
stop_btn.grid(column=1,row=2)

# Add a status bar to show the output of script?
#status = ScrolledText(window,width=680,height=200)
#status.grid(column=0,row=3)

# starts window loop 
window.mainloop()
