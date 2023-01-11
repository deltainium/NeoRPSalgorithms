# Import the required libraries
from tkinter import *
from textwrap import wrap

# Create an instance of tkinter frame
root = Tk()
# Iterate through the color and fill the rectangle with colors(Player1Color,DrawColor,0)


Player1Color = "#ff00ff"
Player2Color = "#0000ff"
DrawColor = "#00ff00"

def HeatmapColorHandler(P1,P2,draws):
    #The heatmap is only affected to a certain degree, it cannot be amplified, 
    #since it shows the win rate of player 1 and 2, points do not matter, 
    #only winning or losing does.

    P1Color = Player1Color.lstrip("#")
    P2Color = Player2Color.lstrip("#")
    TieColor = DrawColor.lstrip("#")

    P1Color = wrap(P1Color,2)
    P1Color_r = P1 *  int(P1Color[0],base=16)
    P1Color_g = P1 *  int(P1Color[2],base=16)
    P1Color_b = P1 *  int(P1Color[1],base=16)

    P1Color_r = P1Color_r 
    P1Color_g = P1Color_g
    P1Color_b = P1Color_b 

    P2Color = wrap(P2Color,2)
    print(P2Color)
    P2Color_r = P2 * int(P2Color[0],base=16)
    P2Color_g = P2 * int(P2Color[2],base=16)
    P2Color_b = P2 * int(P2Color[1],base=16)
    print(P2Color_r)
    print(P2Color_g)
    print(P2Color_b)


    P2Color_r = P2Color_r 
    P2Color_g = P2Color_g
    P2Color_b = P2Color_b

    TieColor = wrap(TieColor,2)
    TieColor_r = draws * int(TieColor[0],base=16)
    TieColor_g = draws * int(TieColor[2],base=16)
    TieColor_b = draws * int(TieColor[1],base=16)

    TieColor_r = TieColor_r 
    TieColor_g = TieColor_g
    TieColor_b = TieColor_b 

    r = P1 * (P1Color_r + P2Color_r + TieColor_r)/3
    b = P2 * (P1Color_b + P2Color_b + TieColor_b)/3
    g = draws * (P1Color_g + P2Color_g + TieColor_g)/3

    #All of P1 RGB values need to scale up with P1 (a float between 0 and 1)

    print("r: "+str(r)+"\ng: "+str(g)+"\nb: "+str(b))


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

    print("r: "+r+"\ng: "+g+"\nb: "+b)
    return "#"+r+g+b

ColorTester = Canvas(root,background="red")
ColorTester.pack()

ColorTester.config(background=HeatmapColorHandler(1,0,0))

root.mainloop()