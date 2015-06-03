# Remember to run with Python 2.6, not 3+
import random
import os
import time
import ctypes
import sys

# Constants from the Windows API for coloring text.
STD_OUTPUT_HANDLE = -11
FOREGROUND_RED    = 0x0004 # text color contains red.
FOREGROUND_BLUE   = 0x0001
FOREGROUND_GREEN     = 0x0002 # text color contains green.
FOREGROUND_INTENSITY = 0x0008 # text color is intensified.
FOREGROUND_WHITE     = FOREGROUND_BLUE|FOREGROUND_GREEN |FOREGROUND_RED


uuid = 0
PopulationList = []
ArenaBoundaryX = 80
ArenaBoundaryY = 50

# Again, code related to coloring console output.
def get_csbi_attributes(handle):
    # Based on IPython's winconsole.py, written by Alexander Belchenko
    import struct
    csbi = ctypes.create_string_buffer(22)
    res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
    assert res
    (bufx, bufy, curx, cury, wattr,
    left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
    return wattr

handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
reset = get_csbi_attributes(handle)

def ContinueKey():
    raw_input('Press Enter to continue...')

def AutoCreateBeing():
    global uuid
    global ArenaBoundaryX
    global ArenaBoundaryY
    uuid = uuid + 1
    Being = {}
    Being['NAM'] = uuid                                                                        # Unique ID for each Being in History
    Being['AGG'] = random.randrange(1,11)                                                      # Aggression [Meek(1) - Suicidal(10)]
    Being['VIR'] = random.randrange(1,11)                                                      # Virility [Impotent(1) - Potent(10)]
    Being['HEL'] = random.randrange(1,11)                                                      # Health [Sickly(1) - Healthy(10)]
    Being['STR'] = random.randrange(1,11)                                                      # Strength [Weak(1) - Strong(10)]
    Being['GEN'] = random.randrange(1,3)                                                       # 1 is male, 2 is female.
    Being['MXA'] = random.randrange(5,10)                                                      # Age at which Being dies due to old age.
    Being['AGE'] = random.randrange(0,3)                                                       # Current Age of Being
    X = random.randrange(1,ArenaBoundaryX)
    Y = random.randrange(1,ArenaBoundaryY)
    while (CheckBeingPresent(X,Y) or CheckBeyondArenaBoundary(X,Y)) == 1:
        X = random.randrange(1,ArenaBoundaryX)
        Y = random.randrange(1,ArenaBoundaryY)
    Being['LOX'] = X                                                     # X Coords
    Being['LOY'] = Y                                                     # Y Coords
    return Being

def AutoCreatePopulation(PopCount):
    global PopulationList
    counter = 0
    while counter < PopCount:
        PopulationList.append(AutoCreateBeing())
        counter += 1
    
def UserInputBeing():
    global uuid
    global ArenaBoundaryX
    global ArenaBoundaryY
    ReturnFish = {}
    uuid = uuid + 1
    print "Enter Fish Details...\n"
    print "Fish ID : " + uuid
    print "-----------------------------"
    ReturnFish['NAM'] = uuid
    ReturnFish['AGG'] = int(input("Enter Aggression [Meek(1) - Suicidal(10)] ::"))
    ReturnFish['VIR'] = int(input("Enter Virility [Impotent(1) - Potent(10)] ::"))
    ReturnFish['HEL'] = int(input("Enter Health [Sickly(1) - Healthy(10)] ::"))
    ReturnFish['STR'] = int(input("Enter Strength [Weak(1) - Strong(10)] ::"))
    ReturnFish['GEN'] = int(input("Enter Gender [Male(1)/Female(2)] ::"))
    ReturnFish['LOX'] = random.randrange(1,ArenaBoundaryX)                                                     # X Coords
    ReturnFish['LOY'] = random.randrange(1,ArenaBoundaryY)                                                     # Y Coords
    ReturnFish['MXA'] = random.randrange(5,10)                                                                 # Age at which Being dies due to old age.
    ReturnFish['AGE'] = random.randrange(0,3)                                                                  # Current Age of Being
    return ReturnFish
    
def Create_Adam_Eve(user_or_auto):
    global PopulationList
    Being = {}
    if user_or_auto == 0:
        PopulationList.append(UserInputBeing())
        PopulationList.append(UserInputBeing())
    else:
        print 'Creating Adam...'
        Being = AutoCreateBeing()
        Being['GEN'] = 1
        PopulationList.append(Being)
        print 'Creating Eve...'
        Being = AutoCreateBeing()
        Being['GEN'] = 2
        PopulationList.append(Being)
        
def World_Info():
    global PopulationList
    print PopulationList
    ContinueKey()

def Mate():
    pass

def CheckBeingPresent(X,Y):
    global PopulationList
    for Being in PopulationList:
        if Being['LOX'] == X and Being['LOY'] == Y:
            return 1
    return 0

def CheckBeyondArenaBoundary(X,Y):
    global ArenaBoundaryX
    global ArenaBoundaryY
    if X >= ArenaBoundaryX or Y >= ArenaBoundaryY or X <= 0 or Y <= 0:
        return 1
    return 0
    
def Move(Being):
    #All we do is find a direction to move in - Directions are labelled clockwise
    #N - 1, NE - 2 and so on till W - 8
    ret = 1
    X = 0
    Y = 0
    while ret == 1:
        dir = random.randrange(0,9) # Since random only returns between 1 and 8
        if dir == 1:
            Y = Being['LOY'] - 1
        if dir == 2:
            X = Being['LOX'] + 1
            Y = Being['LOY'] - 1
        if dir == 3:
            X = Being['LOX'] + 1
        if dir == 4:
            X = Being['LOX'] + 1
            Y = Being['LOY'] + 1
        if dir == 5:
            Y = Being['LOY'] + 1
        if dir == 6:
            X = Being['LOX'] - 1
            Y = Being['LOY'] + 1
        if dir == 7:
            X = Being['LOX'] - 1
        if dir == 8:
            X = Being['LOX'] - 1
            Y = Being['LOY'] - 1
        ret = CheckBeingPresent(X,Y) or CheckBeyondArenaBoundary(X,Y)
    Being['LOX'] = X
    Being['LOY'] = Y
    return Being

def PopulationMove():
    global PopulationList
    for Being in PopulationList:
        Move(Being)

def Fight():
    pass

def SearchMate():
    pass

def SearchRival():
    pass

def BeingDie():
    pass

def ScreenClear():
    os.system('cls')
    
def PrintArena():
    global handle
    global reset
    global ArenaBoundaryX
    global ArenaBoundaryY
    global PopulationList
    print
    print
    X = Y = 0
    while Y <= ArenaBoundaryY:
        X = 0
        sys.stdout.write('\t')
        while X <= ArenaBoundaryX:
            if (Y==0 and X==0) or (Y==0 and X==ArenaBoundaryX) or (Y==ArenaBoundaryY and X==0) or (Y==ArenaBoundaryY and X==ArenaBoundaryX):
                sys.stdout.write('+')      # Draws the corners
            elif (Y==0 and X<ArenaBoundaryX) or (Y == ArenaBoundaryY and X<ArenaBoundaryX):
                sys.stdout.write('-')      # Draws the top and bottom lines
            elif Y!=ArenaBoundaryY and Y!=0 and ( X == 0 or X == ArenaBoundaryX):
                sys.stdout.write('|')      # Draws the vertical lines
            else:
                found = 0
                for Being in PopulationList:
                    if Being['LOX'] == X and Being['LOY'] == Y:
                        found = 1
                        if Being['GEN'] == 1:
                            ctypes.windll.kernel32.SetConsoleTextAttribute(handle, FOREGROUND_BLUE)
                            sys.stdout.write('M')
                            ctypes.windll.kernel32.SetConsoleTextAttribute(handle, reset)
                        else:
                            ctypes.windll.kernel32.SetConsoleTextAttribute(handle, FOREGROUND_RED)
                            sys.stdout.write('F')
                            ctypes.windll.kernel32.SetConsoleTextAttribute(handle, reset)
                if found == 0:
                    sys.stdout.write(' ')
            X += 1
        print
        Y += 1
        
def Start_Sim():
    ScreenClear()
    max_years = 1
    curr_year = 1
    max_years = int(raw_input('Enter number of years to run through :: '))
    while curr_year < max_years:
        time.sleep(0.1)
        ScreenClear()
        PopulationMove()
        PrintArena()
        curr_year += 1
        

def TitleScreen():
    ScreenClear()
    print "FishSim Project"
    print '------------------------'
    print
    print 'This is how I intend to (re)learn Python'
    print '		- Sir AristoMat'
    print
    print
    print 'Options'
    print
    print "1. User Create Adam and Eve"
    print "2. Auto Create Adam and Eve"
    print "3. Auto Create Population"
    print "4. Start Simulation"
    print "5. View Population Info"
    print "9. Exit"

chinp = 0
while 0 == 0:
    TitleScreen()
    chinp = int(input('Enter Choice and hit Enter ::'))
    if chinp == 1:
        Create_Adam_Eve(0)
    if chinp == 2:
        Create_Adam_Eve(1)
    if chinp == 3:
        ScreenClear()
        PopCount = int(raw_input('Enter Population Count :: '))
        AutoCreatePopulation(PopCount)
    if chinp == 4:
        Start_Sim()
    if chinp == 5:
        World_Info()
    if chinp == 9:
        exit()