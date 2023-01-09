from tkinter import *
root = Tk()

BotList = [     #Add list of bots here.
   "RandomBot",
   "HumanBot",
   "RockBot",
   "PaperBot",
   "ScissorsBot",
   "CopyBot",
   "BeatLastBot",
   "GenerousBot",
   "CounterBot",
   "RageBot",
   "EvaluationBot",
   "ExtraBot",
   "ExtraBot",
   "ExtraBot",
   "ExtraBot",
   "ExtraBot",
   "ExtraBot",
   "ExtraBot",
   "ExtraBot",
   "ExtraBot",
   "ExtraBot",
   "ExtraBot",
   "ExtraBot",
   "ExtraBot",
   "ExtraBot",
]

TextSpread = 24

# sideways text and grid of canvases
#Frame shenanigans
MatchingFrame = Frame(root)
MatchingFrame.grid(row=1,column=1,sticky="nw")

for i in range(0,len(BotList)):
   CanvasHeight = TextSpread+i*TextSpread
CanvasWidth = 100


canvas_1_manage = Canvas(root,height=CanvasWidth,width=CanvasHeight)
canvas_1_manage.grid(row = 0, column = 1)
canvas_2_manage = Canvas(root,width=CanvasWidth,height=CanvasHeight)
canvas_2_manage.grid(row = 1, column = 0)

for i in range(0,len(BotList)):
   print(BotList[i])
   canvas_2_manage.create_text(100,1+TextSpread/2+i*TextSpread, text = BotList[i], anchor = "e")

for i in range(0,len(BotList)):
   canvas_1_manage.create_text(TextSpread/2+i*TextSpread, 100, text = BotList[i], angle = 90, anchor = "w")


for y in range(0,len(BotList)):
   globals()[f"CanvasFrame{y}"] = Frame(MatchingFrame)
   globals()[f"CanvasFrame{y}"].grid(row=y,column=2)
   for x in range(0,len(BotList)):
      globals()[f"MatchCanvas{x}_{y}"] = Canvas(globals()[f"CanvasFrame{y}"],width=20,height=20,background="#ff0000")
      globals()[f"MatchCanvas{x}_{y}"].grid(column=x,row=1)

globals()[f"MatchCanvas1_3"].config(background="#0000ff")   #Example of how to edit a squares color


mainloop()