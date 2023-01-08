# Import the required libraries
from tkinter import *
import time

# Create an instance of tkinter frame
root = Tk()
# Iterate through the color and fill the rectangle with colors(r,g,0)


def TurnPointsToColor(points):
    x = points * 255

    if x < 128:
        r = 255-x*2 
    else:
        r = 0

    if x > 128: 
        b = (x-128)*2
    else:
        b = 0

    if x < 64:
        g = 0
    elif x < 128:
        g = (x-64)*2
    elif x < 192:
        g = 255 - (2*x-128)
    else:
        g = 0
    
    print(x,"\n",round(r,2),"\n",round(g,2),"\n",round(b,2),"\n")

    r = hex(int(r)).lstrip("0x").rstrip("L")
    if len(r) < 2:
        if len(r) == 0:
            r = "00"
        else:
            r = "0"+r
    b = hex(int(b)).lstrip("0x").rstrip("L")
    if len(b) < 2:
        if len(b) == 0:
            b = "00"
        else:
            b = "0"+b
    g = hex(int(g)).lstrip("0x").rstrip("L")
    if len(g) < 2:
        if len(g) == 0:
            g = "00"
        else:
            g = "0"+g

    return "#"+r+g+b

ColorTester = Canvas(root,background="red")
ColorTester.pack()

for i in range(0,101):
    ColorTester.config(background=TurnPointsToColor(i/100))
    root.update()
    time.sleep(0.05)

root.mainloop()