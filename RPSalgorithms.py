#RoundLog format explaination:
#(<Move.Paper: 2>, <Move.Rock: 1>, <Outcomes.P1: 1>) | Example
#       ^               ^                 ^
#    P1 Move     |   P2 Move     |      Winner

import enum, random, os, os.path
from tkinter import Tk,Frame,Label,Button,Canvas,OptionMenu,LEFT,RIGHT,TOP,BOTTOM,StringVar,IntVar,Checkbutton,Entry
from PIL import Image, ImageTk

class Move(enum.Enum):
    Rock = 1
    Paper = 2
    Scissors = 3

class Outcomes(enum.Enum):
    P1 = 1
    P2 = 2
    Tie = 3

#region Tkinter interface shenanigans
root = Tk()
root.title("Rock Paper Scissors Algorithms")

funnytexts = ["I live in your walls","bitcoin miner","Get mad!","Lykke te 😈","<3","动态网自由门 天安門 天安门","The cake is a lie","Kanye East ©","https://tiny.cc/allahisbig","flyplassen wiki under construction","0 days without sarcasm","click me!","they are coming","promise that you will sing about me","'Desperate measures' på spotify"]

P1Frame = Frame(root)
P1InputFrame = Frame(P1Frame)
P1Score = Label(P1InputFrame,text="Wins: 0")
TieScore = Label(P1InputFrame,text="Ties: 0")

P2Frame = Frame(root)
P2InputFrame = Frame(P2Frame)
P2Score = Label(P2InputFrame,text="Wins: 0")

InfoFrame = Frame(root)
WinnerLabel = Label(InfoFrame,text="")

AutoFight = IntVar()
AutoFight_InfoFrame = Frame(InfoFrame)
AutoFight_CheckBox = Checkbutton(AutoFight_InfoFrame,text="Auto fight ",variable=AutoFight)
AutoFightText = Label(AutoFight_InfoFrame,text="rounds: ")
AutoFightRange = Entry(AutoFight_InfoFrame,width="10")
AutoFightRange.insert(0,"100")

Player2BotLabel = Label(P2Frame,text="")

HumanBot_ButtonFrame = Frame(P1InputFrame)

ImagePath = os.path.dirname(__file__)   #finds file location and saves it as path
ImagePath = ImagePath.replace("\\","/")

Imagesize = 400                         #Image size, i think its pixel length, the image is a square, so all sides are equal length.

#Image shenanigans
img = Image.open(ImagePath+"/Images/paper.jpg")
img = img.resize((Imagesize,Imagesize))
PaperImage = ImageTk.PhotoImage(img)
img = img.resize((50,50))
Button_PaperImage = ImageTk.PhotoImage(img)

img = Image.open(ImagePath+"/Images/scissors.jpg")
img = img.resize((Imagesize,Imagesize))
ScissorsImage = ImageTk.PhotoImage(img)
img = img.resize((50,50))
Button_ScissorsImage = ImageTk.PhotoImage(img)

if random.randint(1,101) <= 5:  #Nothing to see here *hum hum*
    print("Can you smell what the rock is cooking?")
    img = Image.open(ImagePath+"/Images/THErock.jpg")
else:
    img = Image.open(ImagePath+"/Images/rock.jpg")
img = img.resize((Imagesize,Imagesize))
RockImage = ImageTk.PhotoImage(img)
img = img.resize((50,50))
Button_RockImage = ImageTk.PhotoImage(img)

Image1Canvas = Canvas(P1Frame,width=Imagesize, height=Imagesize)

Image2Canvas = Canvas(P2Frame,width=Imagesize,height=Imagesize)

#endregion

BotList = [             #Add list of bots here.
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
    "FinalBossBot"
]

def Introspection(BotName):    #You must know yourself to know your enemy. Figures out who the bot is and returns who his opponent is (Why his opponent? Because thats what we actually want to know).

    global P1Bot
    global P2Bot
    global Duo

    if Duo == True:              #Duo checks if both players are the same, if they are the same it will return 0 and turn a boolean true so that when the next bot does introspection, they will be returned 1 instantly
        return 1

    if P1Bot == P2Bot:
        Duo = True
        return 0
    elif P1Bot == BotName:
        return 1
    elif P2Bot == BotName:
        return 0
    else:
        print("Error: Bot is having an existencial crisis! Who is bot???")
        print("P1: "+P1Value.get()," | P2: "+P2Value.get()," | BotName: "+BotName)

#region | Player (bot) Algorithms
def RandomBot():                                    #Chooses a pseudo random move
    match random.randint(0,2): 
        case 0:
            return Move.Rock
        case 1:
            return Move.Paper
        case 2:
            return Move.Scissors

PlayerMove = None
PlayerHasMoved = False
def HumanBot_RockMove():                            #For human bot, same with the 2 other functions under, these are for the buttons that display when playing humanbot
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
def HumanBot():                                     #Lets a human play (haha HumanBot???+ humans arent bot??+!!1)
    return PlayerMove

def RockBot():                                      #Will always play rock
    return Move.Rock

def PaperBot():                                     #Will always play paper
    return Move.Paper

def ScissorsBot():                                  #Will always play scissors
    return Move.Scissors

def CopyBot(RoundLog,Enemy):                    #Bugged when playing against itself, will play the enemies last move.
    if Enemy is None:
        Enemy = Introspection("CopyBot")

    return RoundLog[len(RoundLog)-1][Enemy]

def BeatLastBot(RoundLog,Enemy):                 #Will Play the winning move against the enemies last move.

    if Enemy is None:
        Enemy = Introspection("BeatLastBot")

    match RoundLog[len(RoundLog)-1][Enemy]:
        case Move.Rock:
            return Move.Paper

        case Move.Paper:
            return Move.Scissors

        case Move.Scissors:
            return Move.Rock

def GenerousBot(RoundLog,Enemy):                #Will play the losing move against the enemies last move.

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
def RageBot(RoundLog,Enemy):                    #Will play generousbot, but if the bot loses 5 times in a row, it will enter a rage mode and play BeatLastBot for the rest of the game
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
        Player2BotLabel.config(text="RAGING!!")
        RageBot_Friendly = False
    
    if RageBot_Friendly == True:
        return GenerousBot(RoundLog,Enemy)
    else:
        return BeatLastBot(RoundLog,Enemy)

LastMoves = []
def CounterBot(RoundLog,Enemy):                 #Will play the move that wins against the enemies recently most common moves.
    global LastMoves
    if Enemy is None:
        Enemy = Introspection("CounterBot")

    LastMoves.append(RoundLog[len(RoundLog)-1][Enemy])
    if len(LastMoves) > 5:
        LastMoves.pop(0)

    RockMoves_CountBot = LastMoves.count(Move.Rock)
    PaperMoves_CountBot = LastMoves.count(Move.Paper)
    ScissorsMoves_CountBot = LastMoves.count(Move.Scissors)

    if RockMoves_CountBot > PaperMoves_CountBot and RockMoves_CountBot > ScissorsMoves_CountBot:
        return Move.Paper
    
    elif PaperMoves_CountBot > RockMoves_CountBot and PaperMoves_CountBot > ScissorsMoves_CountBot:
        return Move.Scissors
    
    elif ScissorsMoves_CountBot > RockMoves_CountBot and ScissorsMoves_CountBot > PaperMoves_CountBot:
        return Move.Rock

    else:
        return RandomBot()

def ImpossibleBot():
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

def FinalBossBot(RoundLog,Enemy):   #Has a multitude of different bots it can choose from, and picks the one that it believes has the highest odds of winning based off a scoring system
    global PreviousStrat
    global strats
    global BotInfo

    if Enemy is None:
        Enemy = Introspection("FinalBossBot")

    if Enemy == 0:
        Enemy_outcome = Outcomes.P2
    elif Enemy == 1:
        Enemy_outcome = Outcomes.P1
    else:
        Enemy_outcome = Outcomes.Tie

    if RoundLog[len(RoundLog)-1][2] == Outcomes.Tie:            #Tie
        strats[PreviousStrat] = strats[PreviousStrat] - 5 
    elif RoundLog[len(RoundLog)-1][2] == Enemy_outcome:         #Win
        strats[PreviousStrat] = strats[PreviousStrat] + 20  
    else:                                                       #Lose
        strats[PreviousStrat] = strats[PreviousStrat] * round((random.randint(0,11) / 100),3) - 10

    if BotInfo == True:
        Player2BotLabel.config(text="Has a multitude\nof different bots\nit can choose from,\nand picks the\none that it\nbelieves has the\nhighest odds\nof winning based\noff a scoring\nsystem\n\n"+PreviousStrat)

    PreviousStrat = max(strats, key=strats.get)
    print(strats)
    match PreviousStrat:
        case "RandomBot":
            print("Random")
            return RandomBot()

        case "CopyBot":
            print("Copy")
            return CopyBot(RoundLog,Enemy)

        case "BeatLastBot":
            print("BeatLast")
            return BeatLastBot(RoundLog,Enemy)

        case "GenerousBot":
            print("Generous")
            return GenerousBot(RoundLog,Enemy)

        case "CounterBot":
            print("Counter")
            return CounterBot(RoundLog,Enemy)


#endregion

RoundLog = []
PlayerLog = []

P1ScoreValue = 0
P2ScoreValue = 0
TieScoreValue = 0

IsAutoFighting = False

def CheckWinner(P1,P2,PlayerLog):     #P1 is player 1's move, P2 is player 2's move. This function checks the winner and is pretty much the main function, handles
    global P1ScoreValue
    global P2ScoreValue
    global TieScoreValue
    
    if len(PlayerLog) > 1 and PlayerLog[len(PlayerLog)-2] == PlayerLog[len(PlayerLog)-1]:
        pass
    else:
        P1ScoreValue = 0
        P2ScoreValue = 0
        TieScoreValue = 0
        P1Score.config(text=("Wins: "+str(P1ScoreValue)))
        P2Score.config(text=("Wins: "+str(P2ScoreValue)))
        TieScore.config(text=("Ties: "+str(TieScoreValue)))

    if IsAutoFighting == False:
        ImageHandler(P1,P2)

    #Checks for tie, this is done first because it is cheap to check and if the result is a tie then we wont need to check any win conditions, saving us some computer processesing 
    if P1 == P2:
        WinnerLabel.config(text="It was a tie!")
        TieScoreValue += 1
        TieScore.config(text=("Ties: "+str(TieScoreValue)))
        return(P1,P2,Outcomes.Tie)

    #All Player 2 win conditions, if none of them are met, player 1 wins. look into optimizations here, maybe some super smart logic?
    elif P1 == Move.Rock and P2 == Move.Paper or P1 == Move.Paper and P2 == Move.Scissors or P1 == Move.Scissors and P2 == Move.Rock:
        WinnerLabel.config(text="Player 2 wins!")
        P2ScoreValue += 1
        P2Score.config(text=("Wins: "+str(P2ScoreValue)))
        return(P1,P2,Outcomes.P2)

    else:
        WinnerLabel.config(text="Player 1 wins!")
        P1ScoreValue += 1
        P1Score.config(text=("Wins: "+str(P1ScoreValue)))
        return(P1,P2,Outcomes.P1) #If the game is not tied, and player 2 does not win, then the only outcome is that P1 wins, therefor we dont need to check anymore moves


def MatchMaker():           #Matchmakes <3, first identifies the option chosen on the lists, then has them fight and logs the players and round 
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
                P1 = CounterBot(RoundLog,PlayerLog)
            P1Bot = "CounterBot"

        case "RageBot":
            if len(RoundLog) == 0:
                P1 = RandomBot()
            else:
                P1 = RageBot(RoundLog,Enemy)
            P1Bot = "RageBot"

        case "FinalBossBot":
            if len(RoundLog) == 0:
                P1 = RandomBot()
            else:
                P1 = FinalBossBot(RoundLog,Enemy)
            P1Bot = "FinalBossBot"

        
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
                P2 = CounterBot(RoundLog,PlayerLog)
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

        case "FinalBossBot":
            if len(RoundLog) == 0:
                P2 = RandomBot()
            else:
                P2 = FinalBossBot(RoundLog,Enemy)
            P2Bot = "FinalBossBot"

    if AutoFight.get() == 1:
        AutoFight.set(0)
        global IsAutoFighting
        IsAutoFighting = True

        for _ in range(0,int(AutoFightRange.get())):
            MatchMaker()
        IsAutoFighting = False
        AutoFight.set(1)

    else:
        PlayerLog.append((P1Bot,P2Bot))
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

def Player2ListUpdate(Player):      #If the easteregg is activated, descriptions of what the bots do will be displayed when a bot is selected.
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

            case "FinalBossBot":
                Player2BotLabel.config(text=Player2BotLabel.config(text="Has a multitude\nof different bots\nit can choose from,\nand picks the\none that it\nbelieves has the\nhighest odds\nof winning based\noff a scoring\nsystem")

    else:
        match Player:
            case "ImpossibleBot":
                Player2BotLabel.config(text="Only works against\nHumanBot!")

    ResetLogs()


def RerollTrademark():              #Is for easteregg, clicking the Trademark (the funny text in the right corner) will reroll the text
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


FightButton = Button(InfoFrame,text="Fight!",command=MatchMaker,padx=35,pady=10)
ResetButton = Button(InfoFrame,text="Reset logs",command=ResetLogs)

P2BotList = BotList.copy()
P2BotList.remove("HumanBot")
Starting_P2BotList = P2BotList.copy()
P2BotList.append("ImpossibleBot")

P1Value = StringVar()
P1Value.set(BotList[random.randint(0,len(BotList))-1]) 
P2Value = StringVar()
P2Value.set(Starting_P2BotList[random.randint(0,len(Starting_P2BotList))-1])

Player1ListUpdate(P1Value.get())

P1List = OptionMenu(P1InputFrame,P1Value,*BotList,command=Player1ListUpdate)
P2List = OptionMenu(P2InputFrame,P2Value,*P2BotList,command=Player2ListUpdate)

InfoFrame.pack(fill="x",side=BOTTOM)
WinnerLabel.pack(side=TOP)
FightButton.pack(side=TOP)

AutoFight_InfoFrame.pack(side=TOP)
AutoFight_CheckBox.pack(side=TOP)
AutoFightText.pack(side=LEFT)
AutoFightRange.pack(side=RIGHT)
HumanBot_ButtonFrame.pack(side=BOTTOM)
ResetButton.pack(side=LEFT)

TrademarkText = funnytexts[random.randint(0,len(funnytexts)-1)]
Trademark = Button(InfoFrame,text=TrademarkText,command=RerollTrademark,bd=0)
Trademark.pack(side=RIGHT)

P1Frame.pack(side=LEFT)
Image1Canvas.pack(side=RIGHT)
P1InputFrame.pack(side=TOP)
P1List.pack(side=TOP)
P1Score.pack(side=LEFT)
TieScore.pack(side=RIGHT)

P2Frame.pack(side=RIGHT)
Image2Canvas.pack(side=LEFT)
P2InputFrame.pack(side=TOP)
P2List.pack(side=TOP)
P2Score.pack(side=RIGHT)
Player2BotLabel.pack(side=TOP)

root.mainloop()