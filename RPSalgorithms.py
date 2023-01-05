#RoundLog format explaination:
#(<Move.Paper: 2>, <Move.Rock: 1>, <Outcomes.P1: 1>) | Example
#       ^               ^                 ^
#    P1 Move     |   P2 Move     |      Winner

import enum, random, os, os.path, re
#from tkinter import Tk,Frame,Label,Button,Canvas,OptionMenu,LEFT,RIGHT,TOP,BOTTOM,StringVar,IntVar,Checkbutton,Entry, Menu, LabelFrame,NW, Toplevel
from tkinter import *
from PIL import Image, ImageTk
from playsound import playsound

class Move(enum.Enum):
    Rock = 1
    Paper = 2
    Scissors = 3

class Outcomes(enum.Enum):
    P1 = 1
    P2 = 2
    Tie = 3

class Mode(enum.Enum):
    Standard = 1
    Tournament = 2
    ClassicTournament = 3
    misc = 4

#region Tkinter interface shenanigans
root = Tk()
root.title("Rock Paper Scissors Algorithms")

funnytexts = ["I live in your walls","bitcoin miner","Get mad!","Lykke te 😈","<3","动态网自由门 天安門 天安门","The cake is a lie","Kanye East ©","https://tiny.cc/allahisbig","flyplassen wiki under construction","0 days without sarcasm","click me!","they are coming","promise that you will sing about me","'Desperate measures' på spotify"]
TrademarkText = funnytexts[random.randint(0,len(funnytexts)-1)]
MainFrame = Frame(root)
CurrentMode = Mode.Standard

#Image shenanigans
#Get the current screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

Imagesize = 400     #Image size, i think its pixel length, the image is a square, so all sides are equal length.
FilePath = os.path.dirname(__file__)   #finds file location and saves it as path
FilePath = FilePath.replace("\\","/")

img = Image.open(FilePath+"/Images/paper.jpg")
img = img.resize((Imagesize,Imagesize))
PaperImage = ImageTk.PhotoImage(img)
img = img.resize((50,50))
Button_PaperImage = ImageTk.PhotoImage(img)

img = Image.open(FilePath+"/Images/scissors.jpg")
img = img.resize((Imagesize,Imagesize))
ScissorsImage = ImageTk.PhotoImage(img)
img = img.resize((50,50))
Button_ScissorsImage = ImageTk.PhotoImage(img)

if random.randint(1,101) <= 5:  #Nothing to see here
    print("\nCan you smell what the rock is cooking?")
    img = Image.open(FilePath+"/Images/THErock.jpg")
else:
    img = Image.open(FilePath+"/Images/rock.jpg")
img = img.resize((Imagesize,Imagesize))
RockImage = ImageTk.PhotoImage(img)
img = img.resize((50,50))
Button_RockImage = ImageTk.PhotoImage(img)

img = Image.open(FilePath+"/Images/Jumpscare.jpg")
img = img.resize((screen_width,screen_height))
JumpScareImage = ImageTk.PhotoImage(img)

class HoverInfo(Menu):
    def __init__(self, parent, text, command=None):
       self._com = command
       Menu.__init__(self,parent, tearoff=0)
       if not isinstance(text, str):
          raise TypeError('Trying to initialise a Hover Menu with a non string type: ' + text.__class__.__name__)
       toktext=re.split('\n', text)
       for t in toktext:
            self.add_command(label = t)
            self._displayed=False
            self.master.bind("<Enter>",self.Display )
            self.master.bind("<Leave>",self.Remove )

    def __del__(self):
       self.master.unbind("<Enter>")
       self.master.unbind("<Leave>")

    def Display(self,event):
       if not self._displayed:
          self._displayed=True
          self.post(event.x_root, event.y_root)
       if self._com != None:
          self.master.unbind_all("<Return>")
          self.master.bind_all("<Return>", self.Click)

    def Remove(self, event):
     if self._displayed:
       self._displayed=False
       self.unpost()
     if self._com != None:
       self.unbind_all("<Return>")

    def Click(self, event):
       self._com()

def LaunchStandardMode():
    root.attributes('-fullscreen',False)
    CleanRoot()
    global CurrentMode
    global P1Frame
    global P1InputFrame
    global P1Score
    global TieScore
    global P2Frame
    global P2InputFrame
    global P2Score
    global InfoFrame
    global WinnerLabel
    global AutoFight
    global AutoFight_InfoFrame
    global AutoFight_CheckBox
    global AutoFightText
    global AutoFightRange
    global Player2BotLabel
    global HumanBot_PaperMove
    global Image1Canvas
    global Image2Canvas
    global P2BotList
    global Starting_P2BotList
    global P1Value
    global P2Value
    global P1List
    global P2List
    global HumanBot_ButtonFrame

    CurrentMode = Mode.Standard

    P1Frame = Frame(MainFrame)
    P1InputFrame = Frame(P1Frame)
    P1Score = Label(P1InputFrame,text="Wins: 0")
    TieScore = Label(P1InputFrame,text="Ties: 0")

    P2Frame = Frame(MainFrame)
    P2InputFrame = Frame(P2Frame)
    P2Score = Label(P2InputFrame,text="Wins: 0")

    InfoFrame = Frame(MainFrame)
    WinnerLabel = Label(InfoFrame,text="")

    AutoFight = IntVar()
    AutoFight_InfoFrame = Frame(InfoFrame)
    AutoFight_CheckBox = Checkbutton(AutoFight_InfoFrame,text="Auto fight ",variable=AutoFight)
    AutoFightText = Label(AutoFight_InfoFrame,text="rounds: ")
    AutoFightRange = Entry(AutoFight_InfoFrame,width="10")
    AutoFightRange.insert(0,"100")

    Player2BotLabel = Label(P2Frame,text="")
    HumanBot_ButtonFrame = Frame(P1InputFrame)

    Image1Canvas = Canvas(P1Frame,width=Imagesize, height=Imagesize)
    Image2Canvas = Canvas(P2Frame,width=Imagesize,height=Imagesize)

    P2BotList = BotList.copy()
    P2BotList.remove("HumanBot")
    Starting_P2BotList = P2BotList.copy()
    P2BotList.append("ImpossibleBot")

    P1Value = StringVar()
    P1Value.set(BotList[random.randint(0,len(BotList))-1]) 
    P2Value = StringVar()
    P2Value.set(Starting_P2BotList[random.randint(0,len(Starting_P2BotList))-1])

    P1List = OptionMenu(P1InputFrame,P1Value,*BotList,command=Player1ListUpdate)
    P2List = OptionMenu(P2InputFrame,P2Value,*P2BotList,command=Player2ListUpdate)

    P1List.pack(side=TOP)
    P2List.pack(side=TOP)

    InfoFrame.pack(fill="x",side=BOTTOM)
    WinnerLabel.pack(side=TOP)

    AutoFight_CheckBox.pack(side=TOP)
    AutoFightText.pack(side=LEFT)
    AutoFightRange.pack(side=RIGHT)
    HumanBot_ButtonFrame.pack(side=BOTTOM)

    P1Frame.pack(side=LEFT)
    Image1Canvas.pack(side=RIGHT)
    P1InputFrame.pack(side=TOP)
    P1Score.pack(side=LEFT)
    TieScore.pack(side=RIGHT)

    P2Frame.pack(side=RIGHT)
    Image2Canvas.pack(side=LEFT)
    P2InputFrame.pack(side=TOP)
    P2Score.pack(side=RIGHT)
    Player2BotLabel.pack(side=TOP)

    LaunchStandardMode_Buttons()

def LaunchTournamentMode():
    #Put all tkinter UI stuff in here and make them global
    root.attributes('-fullscreen',False)
    CleanRoot()
    global CurrentMode
    global InputFramesHolder
    global RoundsPerFight
    global WinningPoints
    global LosingPoints
    global DrawPoints
    global Player1Color
    global Player2Color
    global DrawColor

    CurrentMode = Mode.Tournament
    GenerateHeatmap()
    
    InputFramesHolder = LabelFrame(MainFrame)
    MainInputFrame = LabelFrame(InputFramesHolder,text="variables")
    ColorInputFrame = LabelFrame(InputFramesHolder,text="Color settings")
    LeaderboardFrame = LabelFrame(InputFramesHolder)

    #Variables
    Label(MainInputFrame,text="Rounds per fight ").grid(row=0,column=0)
    RoundsPerFight = Entry(MainInputFrame,width="10")
    RoundsPerFight.insert(0,"10")
    RoundsPerFight.grid(row=0,column=1)
    Label(MainInputFrame,text="Score for winning ").grid(row=1,column=0)
    WinningPoints = Entry(MainInputFrame,width="10")
    WinningPoints.insert(0,"1")
    WinningPoints.grid(row=1,column=1)
    Label(MainInputFrame,text="Score for losing ").grid(row=2,column=0)
    LosingPoints = Entry(MainInputFrame,width="10")
    LosingPoints.insert(0,"1")
    LosingPoints.grid(row=2,column=1)
    Label(MainInputFrame,text="Score for draw ").grid(row=3,column=0)
    DrawPoints = Entry(MainInputFrame,width="10")
    DrawPoints.insert(0,"1")
    DrawPoints.grid(row=3,column=1)

    #Color settings
    Label(ColorInputFrame,text="Player 1 color ").grid(row=0,column=0)
    Player1Color = Entry(ColorInputFrame,width="13")
    Player1Color.insert(0,"#ff0000")
    Player1Color.grid(row=0,column=1)
    Label(ColorInputFrame,text="Player 2 color ").grid(row=1,column=0)
    Player2Color = Entry(ColorInputFrame,width="13")
    Player2Color.insert(0,"#0000ff")
    Player2Color.grid(row=1,column=1)
    Label(ColorInputFrame,text="Draw color     ").grid(row=2,column=0)
    DrawColor = Entry(ColorInputFrame,width="13")
    DrawColor.insert(0,"#00ff00")
    DrawColor.grid(row=2,column=1)

    #Leaderboard
    Label(LeaderboardFrame,text="Leaderboard",padx=45).grid(row=0,column=0)
    InnerLeaderboardFrame = Frame(LeaderboardFrame)
    InnerLeaderboardFrame.grid(row=1,column=0)
    Label(InnerLeaderboardFrame,text="FIX LATER").grid(row=0,column=0)

    InputFramesHolder.grid(row=0,column=1)
    MainInputFrame.grid(row=0,column=0,padx=20,pady=10)
    ColorInputFrame.grid(row=1,column=0)
    LeaderboardFrame.grid(row=2,column=0,padx=20,pady=10)
    LaunchTournamentMode_Buttons()

def LaunchSecretMode():
    CleanRoot()
    global CurrentMode

    CurrentMode = Mode.misc
    root.attributes('-fullscreen',True)
    JumpscareCanvas = Canvas(MainFrame,width=screen_width,height=screen_height)
    JumpscareCanvas.create_image(screen_width/2,screen_height/2,image=JumpScareImage)
    JumpscareCanvas.pack()
    root.update()
    try:
        playsound(FilePath+'/misc/scary.mp3')
    except:
        print("\n!! Error: Playsound is not installed or version 1.2.2 is not installed !!\nplease run the following lines into command prompt if you wish to install Playsound. If you do not wish to install playsound, please ignore the error.\npip uninstall playsound   (only if you have playsound installed)\npip install playsound==1.2.2\n")

def CleanRoot():
    for widgets in MainFrame.winfo_children():
        widgets.destroy()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Standard mode", command=LaunchStandardMode)
filemenu.add_command(label="Tournament mode", command=LaunchTournamentMode)

if random.randint(1,101) <= 10:
    filemenu.add_command(label="Secret mode (rare)", command=LaunchSecretMode)
    print("\nSecret unlocked!")
    root.quit()
    
menubar.add_cascade(label="Modes", menu=filemenu)
filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)

#endregion

RoundLog = []
PlayerLog = []
TournamentLog = []
Summary = []

P1ScoreValue = 0
P2ScoreValue = 0
TieScoreValue = 0

IsAutoFighting = False

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
    "EvaluationBot"
    #TesterBot, this bot works like EvaluationBot, 
    # but before he uses the first rounds to test every of his strategies 'n' amount of times, 
    # and once its done it keeps playing like before. The advantage to this is that the bot will 
    # more easily find the best strategy, but the downside is that the bot will use theirs first 
    # rounds to test.
]

TournamentBotList = BotList.copy()
TournamentBotList.remove("HumanBot")

def Introspection(BotName):
    #You must know yourself to know your enemy. Figures out who the bot 
    #is and returns what player (number) his opponent is 
    #(Why his opponent? Because thats what we actually want to know)
    global Duo

    if Duo == True:     #Duo checks if both players are the same, if they are the same it will return 0 and turn a boolean true so that when the next bot does introspection, they will be returned 1 instantly
        return 0

    if P1Value.get() == P2Value.get():
        Duo = True
        return 1
    elif P1Value.get() == BotName:
        return 1
    elif P2Value.get() == BotName:
        return 0
    else:
        print("Error: Bot is having an existencial crisis! Who is bot???")
        print("P1: "+P1Value.get()," | P2: "+P2Value.get()," | BotName: "+BotName," | Duo: ",Duo)  #Debugging, incase någe går kalt med introspection, så hjelpe det å vita dette.

#region | Player (bot) Algorithms
def RandomBot():
    #Chooses a pseudo random move
    match random.randint(0,2): 
        case 0:
            return Move.Rock
        case 1:
            return Move.Paper
        case 2:
            return Move.Scissors

PlayerMove = None
PlayerHasMoved = False
def HumanBot_RockMove():
    #For human bot, same with the 2 other functions under, 
    # these are for the buttons that display when playing 
    # humanbot
    global PlayerHasMoved
    global PlayerMove
    PlayerHasMoved = True
    PlayerMove = Move.Rock
    MatchMaker()
    
def HumanBot_PaperMove():
    global PlayerHasMoved
    global PlayerMove
    PlayerHasMoved = True
    PlayerMove = Move.Paper
    MatchMaker()

def HumanBot_ScissorsMove():
    global PlayerHasMoved
    global PlayerMove
    PlayerHasMoved = True
    PlayerMove = Move.Scissors
    MatchMaker()

NextHumanBotMove = None
def HumanBot():
    #Lets a human play (haha HumanBot???+ humans arent bot??+!!1)
    return PlayerMove

def RockBot():      #Will always play rock
    return Move.Rock

def PaperBot():     #Will always play paper
    return Move.Paper

def ScissorsBot():  #Will always play scissors
    return Move.Scissors

def CopyBot(RoundLog,Enemy):    #will play the enemies last move.

    if Enemy is None:
        Enemy = Introspection("CopyBot")

    return RoundLog[len(RoundLog)-1][Enemy]

def BeatLastBot(RoundLog,Enemy):
    #Will Play the winning move against the enemies last move.

    if Enemy is None:
        Enemy = Introspection("BeatLastBot")

    match RoundLog[len(RoundLog)-1][Enemy]:
        case Move.Rock:
            return Move.Paper

        case Move.Paper:
            return Move.Scissors

        case Move.Scissors:
            return Move.Rock

def GenerousBot(RoundLog,Enemy):
    #Will play the losing move against the enemies last move.
    if Enemy is None:
        Enemy = Introspection("GenerousBot")

    match RoundLog[len(RoundLog)-1][Enemy]:
        case Move.Rock:
            return Move.Scissors

        case Move.Paper:
            return Move.Rock

        case Move.Scissors:
            return Move.Paper

RageBot_Friendly = True
Rage = 0
def RageBot(RoundLog,Enemy):
    #Will play generousbot, but if the bot loses 5 times in a row, 
    #it will enter a rage mode and play BeatLastBot for the 
    #rest of the game
    global RageBot_Friendly
    global Rage

    if Enemy is None:
        Enemy = Introspection("RageBot")

    if Enemy == 1:
        RageEnemy = Outcomes.P2
    else:
        RageEnemy = Outcomes.P1

    if RageBot_Friendly == True and RoundLog[len(RoundLog)-1][2] == RageEnemy:  #Checks if the bot is friendly and if the enemy won the round, if both are true, rage is increased, else, rage is decreased.
        Rage += 1
    else:
        if Rage  != 0:      #Looks sketchy since if the code skips 0 and becomes negative, nothing is stopping it from just decreasing far below zero, oh well its probably fine.
            Rage -= 1

    if Rage > 4:
        if CurrentMode == Mode.Standard:
            Player2BotLabel.config(text="RAGING!!")
        RageBot_Friendly = False
    
    if RageBot_Friendly == True:
        return GenerousBot(RoundLog,Enemy)
    else:
        return BeatLastBot(RoundLog,Enemy)

Duo_LastMoves = []
LastMoves = []
def CounterBot(RoundLog,Enemy):
    #Will play the move that wins against the enemies recently most common moves.
    global LastMoves
    if Duo == True or P2Value.get() == "EvaluationBot":
        Temp_LastMoves = Duo_LastMoves
    else:
        Temp_LastMoves = LastMoves

    if Enemy is None:
        Enemy = Introspection("CounterBot")

    Temp_LastMoves.append(RoundLog[len(RoundLog)-1][Enemy])
    if len(Temp_LastMoves) > 5:
        Temp_LastMoves.pop(0)

    RockMoves_CountBot = Temp_LastMoves.count(Move.Rock)
    PaperMoves_CountBot = Temp_LastMoves.count(Move.Paper)
    ScissorsMoves_CountBot = Temp_LastMoves.count(Move.Scissors)

    if RockMoves_CountBot > PaperMoves_CountBot and RockMoves_CountBot > ScissorsMoves_CountBot:
        return Move.Paper
    
    elif PaperMoves_CountBot > RockMoves_CountBot and PaperMoves_CountBot > ScissorsMoves_CountBot:
        return Move.Scissors
    
    elif ScissorsMoves_CountBot > RockMoves_CountBot and ScissorsMoves_CountBot > PaperMoves_CountBot:
        return Move.Rock

    else:
        return RandomBot()

def ImpossibleBot():    
    #Only works against human bot because it reads 
    #the button the player pushed and plays the 
    #move that wins against it
    global PlayerMove
    match PlayerMove:
        case Move.Rock:
            return Move.Paper
        case Move.Paper:
            return Move.Scissors
        case Move.Scissors:
            return Move.Rock

PreviousStrat = "RandomBot"
strats = {"RandomBot": -5, "CopyBot": 0, "BeatLastBot": 0, "GenerousBot": 0, "CounterBot": 0,}
Duo_strats = {"RandomBot": -5, "CopyBot": 0, "BeatLastBot": 0, "GenerousBot": 0, "CounterBot": 0,}

def EvaluationBot(RoundLog,Enemy):
    #Has a multitude of different bots it can choose from, 
    #and picks the one that it believes has the highest odds 
    # of winning based off a scoring system
    global PreviousStrat
    global strats
    global Duo
    global Duo_strats
    global BotInfo
    global LastMoves

    if Duo == True:
        Temp_strats = Duo_strats
    else:
        Temp_strats = strats

    if Enemy is None:
        Enemy = Introspection("EvaluationBot")

    if Enemy == 0:  #Translate the enemy type (Integer) to Outcomes so that we can use it to see who won the previous match
        Enemy_outcome = Outcomes.P2
    elif Enemy == 1:
        Enemy_outcome = Outcomes.P1
    else:
        Enemy_outcome = Outcomes.Tie

    if RoundLog[len(RoundLog)-1][2] == Outcomes.Tie:            #Tie, here the penalty for getting tied is given
        Temp_strats[PreviousStrat] = Temp_strats[PreviousStrat] * 0.5 - 7.5 
    elif RoundLog[len(RoundLog)-1][2] == Enemy_outcome:         #Win, here the reward for winning is given
        Temp_strats[PreviousStrat] = Temp_strats[PreviousStrat] + 20  
    else:                                                       #Lose, here the penatly for losing is given
        Temp_strats[PreviousStrat] = Temp_strats[PreviousStrat] * (random.randint(0,11) / 100) - 12.5

    if BotInfo == True and P2Value.get() == "EvaluationBot":
        Player2BotLabel.config(text="Has a multitude\nof different bots\nit can choose from,\nand picks the\none that it\nbelieves has the\nhighest odds\nof winning based\noff a scoring\nsystem\n\n"+PreviousStrat+"\n\n"+str(Temp_strats).replace(",","\n").replace("'",""))

    LastMoves.append(RoundLog[len(RoundLog)-1][Enemy])
    if len(LastMoves) > 5:
        LastMoves.pop(0)

    PreviousStrat = max(Temp_strats, key=Temp_strats.get)
    match PreviousStrat:
        case "RandomBot":
            return RandomBot()

        case "CopyBot":
            return CopyBot(RoundLog,Enemy)

        case "BeatLastBot":
            return BeatLastBot(RoundLog,Enemy)

        case "GenerousBot":
            return GenerousBot(RoundLog,Enemy)

        case "CounterBot":
            return CounterBot(RoundLog,Enemy)
#endregion

def CheckWinner(P1,P2,PlayerLog):     
    #P1 is player 1's move, P2 is player 2's move. This function checks 
    #the winner and is pretty much the main function, here all the
    #information that is crucial to the Bots is made and this function
    #is the one that calls most of the other functions.
    global P1ScoreValue
    global P2ScoreValue
    global TieScoreValue
    
    if CurrentMode == Mode.Standard:
        if len(PlayerLog) > 1 and PlayerLog[len(PlayerLog)-2] == PlayerLog[len(PlayerLog)-1]:
            pass
        else:
            P1ScoreValue = 0
            P2ScoreValue = 0
            TieScoreValue = 0
            P1Score.config(text=("Wins: "+str(P1ScoreValue)))
            P2Score.config(text=("Wins: "+str(P2ScoreValue)))
            TieScore.config(text=("Ties: "+str(TieScoreValue)))
        
    if IsAutoFighting == False and CurrentMode == Mode.Standard:
        ImageHandler(P1,P2)

    #Checks for tie, this is done first because it is cheap to check and if 
    #the result is a tie then we wont need to check any win conditions, 
    #saving us some computer processesing 
    if P1 == P2:
        if CurrentMode == Mode.Standard:
            WinnerLabel.config(text="It was a tie!")
            TieScoreValue += 1
            TieScore.config(text=("Ties: "+str(TieScoreValue)))
        return(P1,P2,Outcomes.Tie)

    #All Player 2 win conditions, if none of them are met, player 1 wins.
    #look into optimizations here, maybe some super smart logic?
    elif P1 == Move.Rock and P2 == Move.Paper or P1 == Move.Paper and P2 == Move.Scissors or P1 == Move.Scissors and P2 == Move.Rock:
        if CurrentMode == Mode.Standard:
            WinnerLabel.config(text="Player 2 wins!")
            P2ScoreValue += 1
            P2Score.config(text=("Wins: "+str(P2ScoreValue)))
        return(P1,P2,Outcomes.P2)

    #If the game is not tied, and player 2 does not win, 
    #then the only outcome is that P1 wins, therefor we dont
    #need to check anymore moves
    else:
        if CurrentMode == Mode.Standard:
            WinnerLabel.config(text="Player 1 wins!")
            P1ScoreValue += 1
            P1Score.config(text=("Wins: "+str(P1ScoreValue)))
        return(P1,P2,Outcomes.P1)


def MatchMaker():
    #Matchmakes <3, first identifies the option chosen on the lists, 
    #then has them fight and logs the players and round 
    Enemy = None
    global P1Bot
    global P2Bot
    global Duo

    #Makes the bot chosen on the list of bots into the player for player 1
    match P1Value.get():
        case "RandomBot":
            P1Bot = "RandomBot"
            P1 = RandomBot()

        case "HumanBot":
            P1Bot = "HumanBot"
            P1 = HumanBot()
        
        case "RockBot":
            P1Bot = "RockBot"
            P1 = RockBot()

        case "PaperBot":
            P1Bot = "PaperBot"
            P1 = PaperBot()

        case "ScissorsBot":
            P1Bot = "ScissorsBot"
            P1 = ScissorsBot()

        case "CopyBot":
            if len(RoundLog) == 0:
                P1 = RandomBot()
            else:
                P1 = CopyBot(RoundLog,Enemy)
            P1Bot = "CopyBot"

        case "BeatLastBot":
            if len(RoundLog) == 0:
                P1 = RandomBot()
            else:
                P1 = BeatLastBot(RoundLog,Enemy)
            P1Bot = "BeatLastBot"

        case "GenerousBot":
            if len(RoundLog) == 0:
                P1 = RandomBot()
            else:
                P1 = GenerousBot(RoundLog,Enemy)
            P1Bot = "GenerousBot"
    
        case "CounterBot":
            if len(RoundLog) == 0:
                P1 = RandomBot()
            else:
                P1 = CounterBot(RoundLog,Enemy)
            P1Bot = "CounterBot"

        case "RageBot":
            if len(RoundLog) == 0:
                P1 = RandomBot()
            else:
                P1 = RageBot(RoundLog,Enemy)
            P1Bot = "RageBot"

        case "EvaluationBot":
            if len(RoundLog) == 0:
                P1 = RandomBot()
            else:
                P1 = EvaluationBot(RoundLog,Enemy)
            P1Bot = "EvaluationBot"

        
    #Makes the bot chosen on the list of bots into the player for player 2
    match P2Value.get():
        case "RandomBot":
            P2Bot = "RandomBot"
            P2 = RandomBot()

        case "RockBot":
            P2Bot = "RockBot"
            P2 = RockBot()

        case "PaperBot":
            P2Bot = "PaperBot"
            P2 = PaperBot()

        case "ScissorsBot":
            P2Bot = "ScissorsBot"
            P2 = ScissorsBot()

        case "CopyBot":
            if len(RoundLog) == 0:
                P2 = RandomBot()
            else:
                P2 = CopyBot(RoundLog,Enemy)
            P2Bot = "CopyBot"

        case "BeatLastBot":
            if len(RoundLog) == 0:
                P2 = RandomBot()
            else:
                P2 = BeatLastBot(RoundLog,Enemy)
            P2Bot = "BeatLastBot"

        case "GenerousBot":
            if len(RoundLog) == 0:
                P2 = RandomBot()
            else:
                P2 = GenerousBot(RoundLog,Enemy)
            P2Bot = "GenerousBot"
    
        case "CounterBot":
            if len(RoundLog) == 0:
                P2 = RandomBot()
            else:
                P2 = CounterBot(RoundLog,Enemy)
            P2Bot = "CounterBot"

        case "ImpossibleBot":
            P2Bot = "ImpossibleBot"
            P2 = ImpossibleBot()

        case "RageBot":
            if len(RoundLog) == 0:
                P2 = RandomBot()
            else:
                P2 = RageBot(RoundLog,Enemy)
            P2Bot = "RageBot"

        case "EvaluationBot":
            if len(RoundLog) == 0:
                P2 = RandomBot()
            else:
                P2 = EvaluationBot(RoundLog,Enemy)
            P2Bot = "EvaluationBot"

    PlayerLog.append((P1Bot,P2Bot))
    RoundLog.append(CheckWinner(P1,P2,PlayerLog))

    if CurrentMode == Mode.Standard:
        if AutoFight.get() == 1:
            AutoFight.set(0)
            global IsAutoFighting
            IsAutoFighting = True

            for _ in range(0,int(AutoFightRange.get())):
                MatchMaker()
            IsAutoFighting = False
            AutoFight.set(1)

    elif CurrentMode == Mode.Tournament:
        CurrentMatch = CheckWinner(P1,P2,PlayerLog)[2]
        TournamentLog.append((P1Bot,P2Bot,CurrentMatch))
        RoundLog.append(CheckWinner(P1,P2,PlayerLog))

    Duo = False
    #print(RoundLog[len(RoundLog)-1])


def ResetLogs():    #Resets logs (wow who wouldve thought)
    global RoundLog
    RoundLog = []
    global PlayerLog
    PlayerLog = []

    #Bot values
    global RockMoves_CountBot
    global PaperMoves_CountBot
    global ScissorsMoves_CountBot

    global P1ScoreValue
    global P2ScoreValue
    global TieScoreValue

    global RageBot_Friendly
    global Rage

    global strats

    strats = {"RandomBot": -5, "CopyBot": 0, "BeatLastBot": 0, "GenerousBot": 0, "CounterBot": 0,}

    RockMoves_CountBot = 0
    PaperMoves_CountBot = 0
    ScissorsMoves_CountBot = 0

    P1ScoreValue = 0
    P2ScoreValue = 0
    TieScoreValue = 0

    RageBot_Friendly = True
    Rage = 0

    if CurrentMode == Mode.Standard:
        P1Score.config(text="Wins: "+str(P1ScoreValue))
        P2Score.config(text="Wins: "+str(P2ScoreValue))
        TieScore.config(text="Ties: "+str(TieScoreValue))
    
def ImageHandler(P1Move,P2Move):    #Handles what images to use depending on the player moves
    match P1Move:
        case Move.Rock:
            Image1Canvas.create_image(Imagesize/2,Imagesize/2,image=RockImage)

        case Move.Paper:
            Image1Canvas.create_image(Imagesize/2,Imagesize/2,image=PaperImage)

        case Move.Scissors:
            Image1Canvas.create_image(Imagesize/2,Imagesize/2,image=ScissorsImage)

    match P2Move:
        case Move.Rock:
            Image2Canvas.create_image(Imagesize/2,Imagesize/2,image=RockImage)

        case Move.Paper:
            Image2Canvas.create_image(Imagesize/2,Imagesize/2,image=PaperImage)

        case Move.Scissors:
            Image2Canvas.create_image(Imagesize/2,Imagesize/2,image=ScissorsImage)
            

def Player1ListUpdate(Player):
    if Player == "HumanBot":
        for widgets in HumanBot_ButtonFrame.winfo_children():
            widgets.destroy()
        HumanBot_ScissorsButton = Button(HumanBot_ButtonFrame,image=Button_ScissorsImage,text="Scissors",compound=TOP,command=HumanBot_ScissorsMove)
        HumanBot_ScissorsButton.pack(side=BOTTOM)
        HumanBot_PaperButton = Button(HumanBot_ButtonFrame,image=Button_PaperImage,text="Paper",compound=TOP,command=HumanBot_PaperMove)
        HumanBot_PaperButton.pack(side=BOTTOM)
        HumanBot_RockButton = Button(HumanBot_ButtonFrame,image=Button_RockImage,text="Rock",compound=TOP,command=HumanBot_RockMove)
        HumanBot_RockButton.pack(side=BOTTOM)

        global PlayerHasMoved
        if PlayerHasMoved == True:
            PlayerHasMoved = False
            for widgets in HumanBot_ButtonFrame.winfo_children():
                widgets.destroy()

    else:
        for widgets in HumanBot_ButtonFrame.winfo_children():
                widgets.destroy()
    ResetLogs()

BotInfo = False

def Player2ListUpdate(Player):      
    #If the easteregg is activated, descriptions of what 
    #the bots do will be displayed when a bot is selected.
    global BotInfo
    global PreviousStrat
    Player2BotLabel.config(text="")
    if BotInfo == True:
        match Player:
            case "RandomBot":
                Player2BotLabel.config(text="Plays a\nrandom move")
            
            case "RockBot":
                Player2BotLabel.config(text="Only plays rock")
                
            case "PaperBot":
                Player2BotLabel.config(text="Only plays paper")

            case "ScissorsBot":
                Player2BotLabel.config(text="Only plays\nscissors")

            case "CopyBot":
                Player2BotLabel.config(text="Copies\nopponents move")

            case "BeatLastBot":
                Player2BotLabel.config(text="Tries to play the\nwinning move\nagainst opponents\nlast move")

            case "GenerousBot":
                Player2BotLabel.config(text="Tries to play the\nlosing move\nagainst opponents\nlast move")

            case "CounterBot":
                Player2BotLabel.config(text="Counts what moves\nhis opponent\nplays and plays\nthe winning move\nagainst his\nopponents most\ncommon move")

            case "RageBot":
                Player2BotLabel.config(text="Is usually nice,\nbut if he loses\ntoo much he\ngets angry")

            case "ImpossibleBot":
                Player2BotLabel.config(text="Does not lose\n\nOnly works against\nHumanBot!")

            case "EvaluationBot":
                Player2BotLabel.config(text=Player2BotLabel.config(text="Has a multitude\nof different bots\nit can choose from,\nand picks the\none that it\nbelieves has the\nhighest odds\nof winning based\noff a scoring\nsystem"))

    else:
        match Player:
            case "ImpossibleBot":
                Player2BotLabel.config(text="Only works against\nHumanBot!")

    ResetLogs()

def GenerateHeatmap():
    TextSpread = 24

    # sideways text and grid of canvases
    #Frame shenanigans
    HeatMapFrame = Frame(MainFrame)
    HeatMapFrame.grid(row=0,column=0)
    MatchingFrame = Frame(HeatMapFrame)
    MatchingFrame.grid(row=1,column=1,sticky="nw")


    for i in range(0,len(TournamentBotList)):
        CanvasHeight = TextSpread+i*TextSpread
    CanvasWidth = 100

    canvas_1_manage = Canvas(HeatMapFrame,height=CanvasWidth,width=CanvasHeight)
    canvas_1_manage.grid(row = 0, column = 1)
    canvas_2_manage = Canvas(HeatMapFrame,width=CanvasWidth,height=CanvasHeight)
    canvas_2_manage.grid(row = 1, column = 0)

    for i in range(0,len(TournamentBotList)):
        canvas_2_manage.create_text(CanvasWidth,1+TextSpread/2+i*TextSpread, text = TournamentBotList[i], anchor = "e")

    for i in range(0,len(TournamentBotList)):
        canvas_1_manage.create_text(TextSpread/2+i*TextSpread, CanvasWidth, text = TournamentBotList[i], angle = 90, anchor = "w")


    for y in range(0,len(TournamentBotList)):
        globals()[f"CanvasFrame{y}"] = Frame(MatchingFrame)
        globals()[f"CanvasFrame{y}"].grid(row=y,column=2)
        for x in range(0,len(TournamentBotList)):
            globals()[f"MatchCanvas{x}_{y}"] = Canvas(globals()[f"CanvasFrame{y}"],width=20,height=20,background="#ff0000")
            globals()[f"MatchCanvas{x}_{y}"].grid(column=x,row=1)
            globals()[f"MatchCanvas{x}_{y}"].hover = HoverInfo(globals()[f"MatchCanvas{x}_{y}"],'P1 wins points: 0\nP2 wins points: 0\nDraw points: 0')

    
def HeatmapColorHandler(wins,loses,draws):
    #globals()[f"MatchCanvas1_3"].config(background="0000ff")   #Example of how to change color of specific square
    r = wins * 255
    b = loses * 255
    g = draws * 255

    if r < 0:
        r = 0
    if b < 0:
        b = 0
    if g < 0:
        g = 0

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

def StartTournament():
    global Player1_Tournament
    global Player2_Tournament
    global TournamentLog
    global RoundsPerFight
    Bots = len(TournamentBotList)
    for y in range(0, Bots):
        P1Value.set(TournamentBotList[y])
        for x in range(0,Bots):
            P2Value.set(TournamentBotList[x])
            ResetLogs()
            for _ in range(0,int(RoundsPerFight.get())):
                MatchMaker()
            ColorPoints = MatchesToPoints(TournamentLog)
            globals()[f"MatchCanvas{x}_{y}"].config(background=HeatmapColorHandler(ColorPoints[0],ColorPoints[1],ColorPoints[2]))
            globals()[f"MatchCanvas{x}_{y}"].hover = HoverInfo(globals()[f"MatchCanvas{x}_{y}"],text=("P1 wins points: "+str(Wins)+"\nP2 wins points: "+str(Loses)+"\nDraw points: "+str(Draws)))
            TournamentLog = []
            root.update()

def MatchesToPoints(Matches):
    global Wins
    global Loses
    global Draws
    Wins = 0
    Loses = 0
    Draws = 0
    for i in range(0,len(Matches)):
        match Matches[i][2]:
            case Outcomes.P1:
                Wins += int(WinningPoints.get())
            case Outcomes.P2:
                Loses += int(LosingPoints.get())
            case Outcomes.Tie:
                Draws += int(DrawPoints.get())
    return Wins/(0.000001+len(Matches)*int(WinningPoints.get())),Loses/(0.000001+len(Matches)*int(LosingPoints.get())),+Draws/(0.000001+len(Matches)*int(DrawPoints.get()))


def LaunchStandardMode_Buttons():
    global Trademark
    FightButton = Button(InfoFrame,text="Fight!",command=MatchMaker,padx=35,pady=10)
    FightButton.pack(side=TOP)
    AutoFight_InfoFrame.pack(side=TOP)
    ResetButton = Button(InfoFrame,text="Reset logs",command=ResetLogs)
    ResetButton.pack(side=LEFT)
    Trademark = Button(InfoFrame,text=TrademarkText,command=RerollTrademark,bd=0)
    Trademark.pack(side=RIGHT)

def LaunchTournamentMode_Buttons():
    StartButton = Button(InputFramesHolder,text="Start\ntournament!",command=StartTournament,padx=35,pady=10)
    StartButton.grid(row=3,column=0,pady=10)

def RerollTrademark():
    #Is for easteregg, clicking the Trademark 
    #(the funny text in the right corner) will reroll the text
    global BotInfo
    BotInfo = True
    Player2ListUpdate(P2Value.get())

    global TrademarkText
    NewTrademarkText = funnytexts[random.randint(0,len(funnytexts)-1)]

    Finished = False
    while Finished == False:
        Trademark.config(text=TrademarkText)
        if NewTrademarkText == TrademarkText:
            NewTrademarkText = funnytexts[random.randint(0,len(funnytexts)-1)]
        else:
            Finished = True
            
    TrademarkText = NewTrademarkText
    Trademark.config(text=TrademarkText)


MainFrame.pack()
LaunchStandardMode()
Player1ListUpdate(P1Value.get())

root.config(menu=menubar)
root.mainloop()
