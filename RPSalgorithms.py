#RoundLog format explaination:
#(<Move.Paper: 2>, <Move.Rock: 1>, <Outcomes.P1: 1>) | Example
#       ^               ^                 ^
#    P1 Move     |   P2 Move     |      Winner

import enum, random, os, os.path
from tkinter import Tk,Frame,Label,Button,Canvas,OptionMenu,LEFT,RIGHT,TOP,BOTTOM,StringVar,IntVar,Checkbutton,Entry, Menu, LabelFrame
from PIL import Image, ImageTk
PlaysoundFound = True
try:
    from playsound import playsound
except:
    print("Playsound not found")
    PlaysoundFound = False
from idlelib.tooltip import Hovertip

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
    Secret = 4

#region Tkinter interface shenanigans
root = Tk()
root.title("Rock Paper Scissors Algorithms")

funnytexts = ["I live in your walls","bitcoin miner","Get mad!","Lykke te 😈","<3","动态网自由门 天安門 天安门","The cake is a lie","Kanye East ©","https://tiny.cc/allahisbig","flyplassen wiki under construction","0 days without sarcasm","click me!","they are coming","promise that you will sing about me","'Desperate measures' på spotify"]
TrademarkText = funnytexts[random.randint(0,len(funnytexts)-1)]
MainFrame = Frame(root)
CurrentMode = Mode.Standard

#Image shenanigans
#IMAGE SETTINGS !!! <- -
Imagesize = 400     #Image size, i think its pixel length, the image is a square, so all sides are equal length.

#Get the current screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

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
    global ResetLogsPerFight
    global WinningPoints
    global LosingPoints
    global DrawPoints
    global Player1Color
    global Player2Color
    global DrawColor
    global InnerLeaderboardFrame

    CurrentMode = Mode.Tournament
    GenerateHeatmap()
    
    InputFramesHolder = LabelFrame(MainFrame)
    MainInputFrame = LabelFrame(InputFramesHolder,text="variables")
    LeaderboardFrame = LabelFrame(InputFramesHolder)

    #Variables
    Label(MainInputFrame,text="Rounds per fight ").grid(row=0,column=0,sticky="w")
    RoundsPerFight = Entry(MainInputFrame,width="7")
    RoundsPerFight.insert(0,"5000")
    RoundsPerFight.grid(row=0,column=1)
    Label(MainInputFrame,text="Reset logs after 'n' matches: ").grid(row=1,column=0,sticky="w")
    ResetLogsPerFight = Entry(MainInputFrame,width="7")
    ResetLogsPerFight.insert(0,"100")
    ResetLogsPerFight.grid(row=1,column=1)
    Label(MainInputFrame,text="Score for winning ").grid(row=2,column=0,sticky="w")
    WinningPoints = Entry(MainInputFrame,width="7")
    WinningPoints.insert(0,"25")
    WinningPoints.grid(row=2,column=1)
    Label(MainInputFrame,text="Score for losing ").grid(row=3,column=0,sticky="w")
    LosingPoints = Entry(MainInputFrame,width="7")
    LosingPoints.insert(0,"5")
    LosingPoints.grid(row=3,column=1)
    Label(MainInputFrame,text="Score for draw ").grid(row=4,column=0,sticky="w")
    DrawPoints = Entry(MainInputFrame,width="7")
    DrawPoints.insert(0,"10")
    DrawPoints.grid(row=4,column=1)

    #Leaderboard
    Label(LeaderboardFrame,text="Leaderboard",padx=66).grid(row=0,column=0)
    InnerLeaderboardFrame = LabelFrame(LeaderboardFrame,bg="#757575")
    Label(InnerLeaderboardFrame,text="Start a tournament\nto see leaderboard",bg="#757575").grid(row=0,column=0)
    InnerLeaderboardFrame.grid(row=1,column=0)

    InputFramesHolder.grid(row=0,column=1)
    MainInputFrame.grid(row=0,column=0,padx=20,pady=10)
    LeaderboardFrame.grid(row=2,column=0,padx=20,pady=10)
    LaunchTournamentMode_Buttons()

def LaunchSecretMode():
    CleanRoot()
    global CurrentMode

    CurrentMode = Mode.Secret
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

if PlaysoundFound == True and random.randint(1,101) <= 10:
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
    #Stupid bots
    "RandomBot",
    "HumanBot",
    "RockBot",
    "PaperBot",
    "ScissorsBot",
    #Counterintuitive bots
    "CopyBot",
    "GenerousBot",
    #good bots
    "BeatLastBot",
    "CounterBot",
    "RageBot",
    "EvaluationBot",
    "PredictionBotWIP",# this bot will parse the enemy moves into a string and try to find a pattern
    # to their playstyle, after a pattern has been found, it will generate a pattern that will
    # win against the enemy player every single move.

    #TesterBot, this bot works like EvaluationBot, 
    # but before he uses the first rounds to test every of his strategies 'n' amount of times, 
    # and once its done it keeps playing like before. The advantage to this is that the bot will 
    # more easily find the best strategy, but the downside is that the bot will use theirs first 
    # rounds to test.
]

TournamentBotList = BotList.copy()
TournamentBotList.remove("HumanBot")
TournamentBotList.remove("PredictionBotWIP")

Duo = False
def Introspection(BotName):
    #You must know yourself to know your enemy. Figures out who the bot 
    #is and returns what player (number) his opponent is 
    #(Why his opponent? Because thats what we actually want to know)

    #Duo checks if both players are the same, if they are the same 
    #it will return 0 and turn a boolean true so that when the next 
    #bot does introspection, who will be the copy, they will be 
    #returned 1 immediately
    global Duo
    if Duo == True:
        return 0

    if P1Value.get() == P2Value.get():
        Duo = True
        return 1
    elif P1Value.get() == BotName:
        return 1
    elif P2Value.get() == BotName:
        return 0
    else:
        print("!! Error: Bot is having an existencial crisis! Who is bot??? !!")
        print("P1: "+P1Value.get()," | P2: "+P2Value.get()," | BotName recieved: "+BotName," | Duo value: ",Duo)

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
Duo_strats = strats.copy()

def EvaluationBot(RoundLog,Enemy):
    #Has a multitude of different bots it can choose from, 
    #and picks the one that it believes has the highest odds 
    #of winning based off a scoring system
    global PreviousStrat
    global strats
    global Duo
    global Duo_strats
    global BotInfo
    global LastMoves

    if Enemy is None:
        Enemy = Introspection("EvaluationBot")

    if Duo == True:
        Temp_strats = Duo_strats
    else:
        Temp_strats = strats


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

    if BotInfo == True and P2Value.get() == "EvaluationBot" and CurrentMode == Mode.Standard:
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

StringLog = ""
def PredictionBot(RoundLog,Enemy):
    global StringLog

    if Enemy is None:
        Enemy = Introspection("PredictionBotWIP")

    match RoundLog[len(RoundLog)-1][Enemy]:
        case Move.Rock:
            StringLog += "R"
        case Move.Paper:
            StringLog += "P"
        case Move.Scissors:
            StringLog += "S"

    print(StringLog)

    #0. Will play a pattern at start, 1. rock, 2. paper, 3. scissors then repeat until a enemy pattern is found
    #!. this pattern must try to predict what the enemy will play in response to losing. Using metastrategies can help here.
    #1. If the same move has been played three times, play the winning move until loss, if a draw or loss is detected, never attempt again
    #2. If the enemy move plays the same pattern twice generate a pattern that will win against the enemy pattern, 

    return RandomBot()
#endregion

def CheckWinner(P1,P2,PlayerLog):     
    #P1 is player 1's move, P2 is player 2's move. This function checks 
    #the winner and is pretty much the main function, here all the
    #information that is crucial to the Bots is made and this function
    #is the one that calls most of the other functions.
    global P1ScoreValue
    global P2ScoreValue
    global TieScoreValue
    
    if IsAutoFighting == False and CurrentMode == Mode.Standard:
        ImageHandler(P1,P2)

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
            
        case "PredictionBotWIP":
            if len(RoundLog) == 0:
                P1 = RandomBot()
            else:
                P1 = PredictionBot(RoundLog,Enemy)
            P1Bot = "PredictionBotWIP"

        
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

        case "PredictionBotWIP":
            if len(RoundLog) == 0:
                P2 = RandomBot()
            else:
                P2 = PredictionBot(RoundLog,Enemy)
            P2Bot = "PredictionBotWIP"

    PlayerLog.append((P1Bot,P2Bot))
    RoundLog.append(CheckWinner(P1,P2,PlayerLog))

    if CurrentMode == Mode.Standard:
        if AutoFight.get() == 1:
            AutoFight.set(0)
            global IsAutoFighting
            IsAutoFighting = True

            for _ in range(int(AutoFightRange.get())-1):
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
    global Duo_strats

    strats = {"RandomBot": -5, "CopyBot": 0, "BeatLastBot": 0, "GenerousBot": 0, "CounterBot": 0,}
    Duo_strats = strats.copy()


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
                Player2BotLabel.config(text="Has a multitude\nof different bots\nit can choose from,\nand picks the\none that it\nbelieves has the\nhighest odds\nof winning based\noff a scoring\nsystem")

            case "PredictionBotWIP":
                Player2BotLabel.config(text="this bot will parse\nthe enemy moves\ninto a string and\ntry to find a\npattern to their\nplaystyle.\n\nAfter a pattern has been\nfound, it will attempt\nto generate a\npattern that will win\nagainst the enemy\nplayer every single\nmove.")

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

    CanvasHeight = TextSpread+len(TournamentBotList)*TextSpread
    CanvasWidth = 100

    P1ListCanvas = Canvas(HeatMapFrame,height=CanvasWidth,width=CanvasHeight)
    P1ListCanvas.grid(row = 0, column = 1)
    P2ListCanvas = Canvas(HeatMapFrame,width=CanvasWidth,height=CanvasHeight)
    P2ListCanvas.grid(row = 1, column = 0)

    for i in range(0,len(TournamentBotList)):
        P2ListCanvas.create_text(CanvasWidth,1+TextSpread/2+i*TextSpread, text = TournamentBotList[i], anchor = "e")

    for i in range(0,len(TournamentBotList)):
        P1ListCanvas.create_text(TextSpread/2+i*TextSpread, CanvasWidth, text = TournamentBotList[i], angle = 90, anchor = "w")


    for y in range(0,len(TournamentBotList)):
        globals()[f"CanvasFrame{y}"] = Frame(MatchingFrame)
        globals()[f"CanvasFrame{y}"].grid(row=y,column=2)
        root.update()
        for x in range(0,len(TournamentBotList)):
            globals()[f"MatchCanvas{x}_{y}"] = Canvas(globals()[f"CanvasFrame{y}"],width=20,height=20,background="#757575")
            globals()[f"MatchCanvas{x}_{y}"].grid(column=x,row=1)
            Hovertip(globals()[f"MatchCanvas{x}_{y}"],funnytexts[random.randint(0,len(funnytexts)-1)])

    
def HeatmapColorHandler(P1,P2,draws):
    #The heatmap is only affected to a certain degree, it cannot be amplified, 
    #since it shows the win rate of player 1 and 2, points do not matter, 
    #only winning or losing does. (or tieing)
    r = P1 * 255
    b = P2 * 255
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
    #Where the tourneying happens, just a big loop that changes 
    #the players to match them up and logs all the matches, then 
    #it sends these logs to other functions.

    for y in range(0,len(TournamentBotList)):   #Resets color of heatmap to default
        for x in range(0,len(TournamentBotList)):
            globals()[f"MatchCanvas{x}_{y}"].config(bg="#757575")
    root.update()

    global Player1_Tournament
    global Player2_Tournament
    global TournamentLog
    global RoundsPerFight
    global ResetLogsPerFight
    Reset = True
    if ResetLogsPerFight.get() == "0":
        Reset = False

    Bots = len(TournamentBotList)
    Result = []
    for y in range(0, Bots):    #Starts the process, this is where player 1 bot is chosen, and when all the bots have been played, the loop ends
        P1TournamentScore = 0
        P1Value.set(TournamentBotList[y])
        for x in range(0,Bots):     #This is where player 2 bot is chosen and logs are reset to simulate a fresh start for the new matchup
            P2Value.set(TournamentBotList[x])
            ResetLogs()
            for i in range(0,int(RoundsPerFight.get())):    #This is where the matches get played and where the logs are being made
                if Reset == True and i % int(ResetLogsPerFight.get()) == 0: #This is where the logs are reset, if i is divisble by the Reset logs per fight number, the logs are reset, could be improved
                    ResetLogs()
                MatchMaker()
            Points = MatchesToPoints(TournamentLog)         
            P1TournamentScore += Points[0]
            globals()[f"MatchCanvas{x}_{y}"].config(background=HeatmapColorHandler(Points[1][0],Points[1][1],Points[1][2]))     #Here the heatmap is updated
            Hovertip(globals()[f"MatchCanvas{x}_{y}"],text=("P1 winrate: "+str(round(100*(Wins/int(RoundsPerFight.get())),3))+"%"+"\nP2 winrate: "+str(round(100*(Loses/int(RoundsPerFight.get())),3))+"%"+"\nDraw rate: "+str(round(100*(Draws/int(RoundsPerFight.get())),3))+"%"))
            TournamentLog = []  #Tournamentlog gets reset
            root.update()
        Result.append((P1TournamentScore,P1Value.get()))    #Results are made and the bots are sorted with their score
        LeaderboardHandler(Result)  #Once the first loop is finished, the results are sendt to the leaderboard handler and the tournament is finished



def MatchesToPoints(Matches):   
    #Translates the matches of the games 
    #into points and wins and returns them
    #Returns them in two forms
    global Wins
    global Loses
    global Draws
    Wins = 0
    Loses = 0
    Draws = 0
    WinsPoints = 0
    LosesPoints = 0
    Draws_Points = 0
    TotalMatches = len(Matches)

    for i in range(0,TotalMatches):
        match Matches[i][2]:
            case Outcomes.P1:
                WinsPoints += int(WinningPoints.get())
                Wins += 1
            case Outcomes.P2:
                LosesPoints += int(LosingPoints.get())
                Loses += 1
            case Outcomes.Tie:
                Draws_Points += int(DrawPoints.get())
                Draws += 1
    return WinsPoints + LosesPoints + Draws_Points,(Wins/TotalMatches,Loses/TotalMatches,Draws/TotalMatches)

def LeaderboardHandler(Result):     
    #Handles sorting the results and displaying the leaderboard
    def takeFirst(elem):
        return elem[0]
    global InnerLeaderboardFrame
    for widget in InnerLeaderboardFrame.winfo_children():
        widget.destroy()

    Result.sort(key=takeFirst,reverse=True)
    for i in range(0,len(Result)):
        if i == 0:      #If first place
            Label(InnerLeaderboardFrame,text=("Rank "+str(i+1)+": "+Result[i][1]),bg="#757575",fg="#FFD700").grid(row=i,column=0,sticky="e")
            Label(InnerLeaderboardFrame,text=("| "+str(Result[i][0])),bg="#757575",fg="#FFD700").grid(row=i,column=1,sticky="w")
        elif i == 1:    #If second place
            Label(InnerLeaderboardFrame,text=("Rank "+str(i+1)+": "+Result[i][1]),bg="#757575",fg="#c0c0c0").grid(row=i,column=0,sticky="e")
            Label(InnerLeaderboardFrame,text=("| "+str(Result[i][0])),bg="#757575",fg="#c0c0c0").grid(row=i,column=1,sticky="w")
        elif i == 2:    #If third place
            Label(InnerLeaderboardFrame,text=("Rank "+str(i+1)+": "+Result[i][1]),bg="#757575",fg="#CD7F32").grid(row=i,column=0,sticky="e")
            Label(InnerLeaderboardFrame,text=("| "+str(Result[i][0])),bg="#757575",fg="#CD7F32").grid(row=i,column=1,sticky="w")
        else:           #If anything else
            Label(InnerLeaderboardFrame,text=("Rank "+str(i+1)+": "+Result[i][1]),bg="#757575").grid(row=i,column=0,sticky="e")
            Label(InnerLeaderboardFrame,text=("| "+str(Result[i][0])),bg="#757575").grid(row=i,column=1,sticky="w")

def LaunchStandardMode_Buttons():
    global Trademark
    FightButton = Button(InfoFrame,text="Fight!",command=MatchMaker,padx=35,pady=10)
    FightButton.pack(side=TOP)
    AutoFight_InfoFrame.pack(side=TOP)
    ResetButton = Button(InfoFrame,text="Reset logs",command=ResetLogs)
    ResetButton.pack(side=LEFT)

def LaunchTournamentMode_Buttons():
    StartButton = Button(InputFramesHolder,text="Start\ntournament!",command=StartTournament,padx=35,pady=10)
    StartButton.grid(row=3,column=0,pady=10)

def RerollTrademark():
    #Is for easteregg, clicking the Trademark 
    #(the funny text in the right corner) 
    #will reroll the text
    global BotInfo
    if CurrentMode == Mode.Standard:
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
Trademark = Button(root,text=TrademarkText,command=RerollTrademark,bd=0)
Trademark.pack(side=RIGHT)
LaunchStandardMode()
Player1ListUpdate(P1Value.get())

root.config(menu=menubar)
root.mainloop()
