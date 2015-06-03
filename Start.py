# Remember to run with Python 2.6, not 3+
import random
import os
import time

# Globals
uuid = 0
PopulationList = []
History = []

# Arena Dimensions
ArenaBoundaryX = 80
ArenaBoundaryY = 50

# Population Level Factors | Max = 100
Visibility = 40     # 100% means creatures can see the whole arena.
FightingPref = 40   # 100% means a creature will find another one to fight with, regardless of all else. 
MatingPref = 60     # 100% means a creature will find another to mate with, regardless of all else.
SingleMinded = 60   # 100% means a creature will not pick another target until the first target has been dealt with as long as target is visible. Move to Creature Level? 

def Logger(logid, logmsg):
    global History
    History.append(logmsg)

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
    Being['SPD'] = random.randrange(1,4)                                                       # Number of turns after which creature moves.
    Being['TAR'] = ''                                                                          # Populated with uuid of target being if found.
    Being['MVF'] = 0                                                                           # Move Flag. Creature moves when MVF = SPD
    X = random.randrange(1,ArenaBoundaryX)
    Y = random.randrange(1,ArenaBoundaryY)
    while (CheckBeingPresent(X,Y) or CheckBeyondArenaBoundary(X,Y)) == 1:
        X = random.randrange(1,ArenaBoundaryX)
        Y = random.randrange(1,ArenaBoundaryY)
    Being['LOX'] = X                                                     # X Coords
    Being['LOY'] = Y                                                     # Y Coords
    return Being

def GetBeingByUUID(uuid):
    global PopulationList
    for being in PopulationList:
        if being['NAM'] == uuid:
            return being
    return {}

def AutoCreatePopulation(PopCount):
    global PopulationList
    global History
    History = []
    PopulationList = []
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
    
def RandomMove(Being):
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
    
def DistanceBetweenBeings(being1, being2):
    return (((int(being1['LOX']) - int(being2['LOX'])) ** 2) + ((int(being1['LOY']) - int(being2['LOY'])) ** 2)) ** 0.5     # Algebraic distance formula

def GetVisibleBeings(being):
    global PopulationList
    VisibleCellsX = int(ArenaBoundaryX * Visibility / 100)
    VisibleCellsY = int(ArenaBoundaryY * Visibility / 100)    
    
    VisibleBeings = []
    for being2 in PopulationList:
        if (int(being2['LOX']) <= (int(being['LOX']) + int(VisibleCellsX/2))) and (int(being2['LOX']) >= (int(being['LOX']) - int(VisibleCellsX/2))) and (int(being2['LOY']) <= (int(being['LOY'])+int(VisibleCellsY/2))) and (int(being2['LOY']) >= (int(being['LOY']) - int(VisibleCellsY/2))) and ( (being2['LOX'] != being['LOX']) and (being2['LOY'] != being['LOY']) ):
            VisibleBeings.append(being2)
    return VisibleBeings

def GetClosestMate(being):
    ClosestMate = {}
    VisibleBeings = GetVisibleBeings(being)
    
    for being2 in VisibleBeings:
        if ((being['GEN'] != being2['GEN']) and ClosestMate == {}):
            ClosestMate = being2
        elif (being['GEN'] != being2['GEN']) and (DistanceBetweenBeings(being,being2) < DistanceBetweenBeings(being,ClosestMate)):
            ClosestMate = being2
    return ClosestMate

def GetClosestRival(being):
    ClosestRival = {}
    VisibleBeings = GetVisibleBeings(being)
    
    for being2 in VisibleBeings:
        if ((being['GEN'] == being2['GEN']) and ClosestRival == {}):
            ClosestRival = being2
        elif (being['GEN'] == being2['GEN']) and (DistanceBetweenBeings(being,being2) < DistanceBetweenBeings(being,ClosestRival)):
            ClosestRival = being2
    return ClosestRival

def CalcBeingDesire(being1, being2):
    # This function will calculate how desirable being2 is to being1 and return a score on a scale of 0 to 100.
    # 0 means not desirable. 100 means very desirable.
    # Should later be extended to two subsections, desirability as a rival and desirability as a mate.
    
    # Firstly, any creature outside being1's visible area has zero desirability. Out of sight, out of mind.
    VisibleBeings = GetVisibleBeings(being1)
    if being2 not in VisibleBeings:
        return 0
    # Any visible creature will have its score determined by its distance from being1
    VisibleX = int(ArenaBoundaryX * Visibility/100)/2
    VisibleY = int(ArenaBoundaryY * Visibility/100)/2
    
    return (((1-(abs(int(being1['LOX']) - int(being2['LOX']))/VisibleX))*100) + ((1-(abs(int(being1['LOY']) - int(being2['LOY']))/VisibleY))*100))/2

def ChoseTargetMateRival(being, Mate, Rival):
    global History
    Target = GetBeingByUUID(being['TAR'])
    TargetDesire = CalcBeingDesire(being, Target)
    MateDesire = CalcBeingDesire(being, Mate)
    RivalDesire = CalcBeingDesire(being, Rival)
    if (TargetDesire*SingleMinded) > (MateDesire*(100-SingleMinded)) and (TargetDesire*SingleMinded) > (RivalDesire*(100-SingleMinded)):
        return Target
    elif (TargetDesire*SingleMinded) < (MateDesire*(100-SingleMinded)) and (TargetDesire*SingleMinded) > (RivalDesire*(100-SingleMinded)):
        History.append('Creature ' + str(being['NAM']) + ' found a new target to mate! Target is creature ' + str(Mate['NAM']))
        return Mate
    elif (TargetDesire*SingleMinded) > (MateDesire*(100-SingleMinded)) and (TargetDesire*SingleMinded) < (RivalDesire*(100-SingleMinded)):
        History.append('Creature ' + str(being['NAM']) + ' found a new target to fight! Target is creature ' + str(Rival['NAM']))
        return Rival
    elif (TargetDesire*SingleMinded) < (MateDesire*(100-SingleMinded)) and (TargetDesire*SingleMinded) < (RivalDesire*(100-SingleMinded)):
        if MateDesire > RivalDesire:    #TODO: Implement Mate/Fight Factors
            History.append('Creature ' + str(being['NAM']) + ' found a new target to mate! Target is creature ' + str(Mate['NAM']))
            return Mate
        else:
            History.append('Creature ' + str(being['NAM']) + ' found a new target to fight! Target is creature ' + str(Rival['NAM']))
            return Rival
    return Target
    
def MoveTowardsPoint(being1, X, Y):
        if being1['LOX'] < X:
            being1['LOX'] += 1
        elif being1['LOX'] > X:
            being1['LOX'] -= 1
        if being1['LOY'] < Y:
            being1['LOY'] += 1
        elif being1['LOY'] > Y:
            being1['LOY'] -= 1
        BeingInteraction(being1)
            
def BeingMove(being):
    global MatingPref
    global FightingPref
    global SingleMinded
    global History
    
    # Initialize the following variables to dummy values ( itself )
    ClosestMate = being
    ClosestRival = being
    
    #First get all visible beings
    VisibleBeings = GetVisibleBeings(being)
    if VisibleBeings == []:
        # If no beings are visible, any targets existing are reset and a Random move is done.
        History.append('Creature ' + str(being['NAM']) + ' cannot see any other creatures. Target reset.')
        being['TAR'] = ''
        RandomMove(being)
    else:
        ClosestMate = GetClosestMate(being)
        ClosestRival = GetClosestRival(being)

        # Validate Target still exists. If it doesn't, it is reset.
        if (GetBeingByUUID(being['TAR']) == {} and being['TAR'] != '' ):
            History.append('Creature ' + str(being['NAM']) + ' lost its target, creature ' + str(being['TAR']) + ', because it is dead. Target reset.')
            being['TAR'] = ''

        # Check if Target is in visible area. If not, target is reset.
        if (GetBeingByUUID(being['TAR']) not in VisibleBeings) and being['TAR'] != '':
                History.append('Creature ' + str(being['NAM']) + ' lost sight of its target, creature ' + str(being['TAR']) + '. Target reset.')
                being['TAR'] = ''
                
        # If being has no target, assign ClosestMate or Rival based on closest.
        if being['TAR'] == '':
            if CalcBeingDesire(being, ClosestMate) > CalcBeingDesire(being,ClosestRival):
                History.append('Creature ' + str(being['NAM']) + ' found a target to mate! Target is creature ' + str(ClosestMate['NAM']))
                being['TAR'] = ClosestMate['NAM']
            else:
                History.append('Creature ' + str(being['NAM']) + ' found a target to fight! Target is creature ' + str(ClosestRival['NAM']))
                being['TAR'] = ClosestRival['NAM']
              
        # Now compare Target with closest mate and rival and decide whether to change target or not.
        Target = GetBeingByUUID(being['TAR'])
        NewTarget = ChoseTargetMateRival(being, ClosestMate, ClosestRival)
        being['TAR'] = NewTarget['NAM']
        MoveTowardsPoint(being, NewTarget['LOX'],NewTarget['LOY'])
                        
def PopulationMove():
    global PopulationList
    for Being in PopulationList:
        if Being['MVF'] == Being['SPD']:
            BeingMove(Being)
            Being['MVF'] = 0
        else:
            Being['MVF'] += 1
            
def CheckForBeingNearby(being1):
    global PopulationList
    X = being1['LOX']
    Y = being1['LOY']
    for being2 in PopulationList:
        if ((X+1)==being2['LOX'] and Y==being2['LOY']) or ((X-1)==being2['LOX'] and Y==being2['LOY']):
            return being2
            break
        if ((Y+1)==being2['LOY'] and X==being2['LOX']) or ((Y-1)==being2['LOY'] and X==being2['LOX']):
            return being2
            break
        if ((X+1)==being2['LOX'] and (Y+1)==being2['LOY']) or ((X+1)==being2['LOX'] and (Y-1)==being2['LOY']):
            return being2
            break
        if ((X-1)==being2['LOX'] and (Y+1)==being2['LOY']) or ((X-1)==being2['LOX'] and (Y-1)==being2['LOY']):
            return being2
            break
    return {}
    
def ReturnPopCount(Attribute, DesiredValue):
    global PopulationList
    counter = 0
    for being in PopulationList:
        if being[Attribute] == DesiredValue:
            counter += 1
    return counter
    
def Fight(being1, being2):
    global History
    total1 = being1['AGG'] + 1.5*being1['HEL'] + being1['STR']
    total2 = being2['AGG'] + 1.5*being2['HEL'] + being2['STR']
    if total1 == total2:
        History.append('Creature ' + str(being1['NAM']) + ' and creature ' + str(being2['NAM']) + ' are evenly matched!')
        RandomMove(being1)
    elif total1 > total2:
        History.append('Creature ' + str(being1['NAM']) + ' eliminated creature ' + str(being2['NAM']))
        BeingDie(being2)
    else:
        History.append('Creature ' + str(being2['NAM']) + ' eliminated creature ' + str(being1['NAM']))
        BeingDie(being1)

def BeingInteraction(being1):
    being2 = CheckForBeingNearby(being1)
    if being2 != {} and being1['GEN'] == being2['GEN']:
        Fight(being1,being2)        

def BeingDie(being):
    global PopulationList
    global History
    History.append('Creature ' + str(being['NAM']) + ' died.')
    PopulationList.remove(being)
    
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
    string = ''
    X = Y = 0
    while Y <= ArenaBoundaryY:
        X = 0
        string = '\t'
        while X <= ArenaBoundaryX:
            if (Y==0 and X==0) or (Y==0 and X==ArenaBoundaryX) or (Y==ArenaBoundaryY and X==0) or (Y==ArenaBoundaryY and X==ArenaBoundaryX):
                string += '+'      # Draws the corners
            elif (Y==0 and X<ArenaBoundaryX) or (Y == ArenaBoundaryY and X<ArenaBoundaryX):
                string += '-'      # Draws the top and bottom lines
            elif Y!=ArenaBoundaryY and Y!=0 and ( X == 0 or X == ArenaBoundaryX):
                string += '|'      # Draws the vertical lines
            else:
                found = 0
                for Being in PopulationList:
                    if Being['LOX'] == X and Being['LOY'] == Y:
                        found = 1
                        if Being['GEN'] == 1:
                            string += 'M'
                        else:
                            string += 'F'
                if found == 0:
                    string += ' '
            X += 1
        print string
        Y += 1

def WorldInfo():
    global PopulationList
    ScreenClear()
    PrintArena()
    for being in PopulationList:
        print 'NAM ' + str(being['NAM']) + '\t' + 'GEN ' + str(being['GEN']) + '\t' + 'TAR ' + str(being['TAR']) + '\t' + 'LOX ' + str(being['LOX']) + '\t' + 'LOY ' + str(being['LOY']) + '\t' + 'AGG ' + str(being['AGG']) + '\t' + 'HEL ' + str(being['HEL']) + '\t' + 'SPD ' + str(being['SPD'])
    ContinueKey()

        
def StartSim():
    global History
    if PopulationList == []:
        ScreenClear()
        print 'Population has not been created yet. Lets do that now.'
        PopCount = int(raw_input('Enter Population Count :: '))
        AutoCreatePopulation(PopCount)
    ScreenClear()
    max_years = 1
    curr_year = 1
    max_years = int(raw_input('Enter number of years to run through :: '))
    while curr_year < max_years:
        History.append('***Year ' + str(curr_year) + '***')
        time.sleep(0.2)
        ScreenClear()
        PrintArena()
        PopulationMove()
        print '\t\tMale   : ' + str(ReturnPopCount('GEN',1)) + '\t\t' + 'Female : ' + str(ReturnPopCount('GEN',2))
        print 
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
    print "6. View History"
    print "9. Exit"

def PrintHistory():
    global History
    counter = 0
    ScreenClear()
    for line in History:
        print line
        counter += 1
        if counter == 80:
            ContinueKey()
            counter = 0
    ContinueKey()


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
        StartSim()
    if chinp == 5:
        WorldInfo()
    if chinp == 6:
        PrintHistory()
    if chinp == 9:
        exit()