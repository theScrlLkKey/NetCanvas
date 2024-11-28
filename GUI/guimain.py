#import tkinter and math functions
import random
from tkinter import *
from math import *
import numpy as np

#configure the size and name of the window
windowWidth = 500
windowHeight = 500
window_name = str(windowWidth) + " by " + str(windowHeight) + " window"
mouseX = 0
mouseY = 0

#generate a set of randoms (between 0-1 inclusive) in a 12 by 12 array
data = np.random.random((12, 12))

#label modification
def changeSizeLabel(event):
    global window_name
    window_name = str(root.winfo_width()) + " by " + str(root.winfo_height()) + " window"
    root.title(window_name)

#click detection
left_click = False
right_click = False

def left_click_start(event):
    global left_click
    left_click = True

def left_click_stop(event):
    global left_click
    left_click = False

def right_click_start(event):
    global right_click
    right_click = True

def right_click_stop(event):
    global right_click
    right_click = False

#should draw blue where the mouse is
def customMouseAction(e=None):
    title_bar_height = root.winfo_rooty() - root.winfo_y()
    x = int((e.x_root - root.winfo_x()) - (canvas.winfo_x() + 8))
    y = int((e.y_root - root.winfo_y()) - (canvas.winfo_y() + title_bar_height))
    if left_click:
        print("Left mouse down.")
        #img.put("#ffffff", (x,y)) replace with something else
    elif right_click:
        print("Right mouse down.")
        #img.put("#000000", (x,y)) replace with something else
    else:
        print("Mouse not down.")
    label.configure(text = str(x) + ", " + str(y))

#Set the first point in the tkinter interpreter tree
root = Tk()

#start click detection
root.bind("<Button-1>", left_click_start)
root.bind("<B1-ButtonRelease>", left_click_stop)

#right click can be two actions I guess
root.bind("<Button-2>", right_click_start)
root.bind("<B2-ButtonRelease>", right_click_stop)
root.bind("<Button-3>", right_click_start)
root.bind("<B3-ButtonRelease>", right_click_stop)

#creates a canvas that is the same size as the window
''' 
canvas = Canvas(root, width=windowWidth, height=windowHeight, bg="#000000")
canvas.pack()
img = PhotoImage(width=windowWidth, height=windowHeight)
canvas.create_image((windowWidth/2, windowHeight/2), image=img, state="normal")
''' #replace with something else

#randomly changes the colors of pixels to white or blue
'''
for y in range(windowHeight):
    for x in range(windowWidth):
        randomValue = random.randint(3,3)
        if randomValue == 0:
            img.put("#ff0000",(x,y))
        elif randomValue == 1:
            img.put("#00ff00",(x,y))
        elif randomValue == 2:
            img.put("#0000ff",(x,y))
        elif randomValue == 3:
            img.put("#000000",(x,y))
'''


#should draw stuff with the mouse
root.bind("<Motion>", customMouseAction)

#adds a mouse coordinate checker label (probably?)
label = Label(root)
label.pack()
#root.bind("<Motion>", lambda event: label.configure(text=f"{event.x}, {event.y}"))

#adds a click me button that closes the window
button = Button(root, text = 'Close app', command = root.destroy)
button.pack(side = 'bottom')

#Set the name of the window from config
root.title(window_name)

#set the size of the window from config
root.geometry(str(windowWidth) + "x" + str(windowHeight))

#locks the size of the window
#root.resizable(0, 0)

#detects window size change, and updates teh title bar
root.bind("<Configure>", changeSizeLabel)

#start tkinter
root.mainloop()