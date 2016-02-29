from sr.robot import *
def turnHandler(net, type, roll, teamOfMarker, teamOfRobot):
    
    if (roll <= 45 and roll > -45):
        rollNumber = 0 #a
    
    elif (roll <= 135 and roll > 45):
        rollNumber = 1 #b
    
    elif (roll <= -45 and roll > -135):
        rollNumber = 3 #d
    
    else:
        rollNumber = 2 #c
        
    
    if (net == NET_A):
        netNumber = 0
        
    elif (net == NET_B):
        netNumber = 1
        
    elif (net == NET_C):
        netNumber = 2
        
    else:
        print "error marker with undefined net handled in turn handler"
        netNumber = 0
        
    
    if (type == MARKER_TOKEN_SIDE):
        sideNumber = teamOfMarker
    
    elif (type == MARKER_TOKEN_TOP):
        sideNumber = 4
        
    elif (type == MARKER_TOKEN_BOTTOM):
        sideNumber = 5
    
        
    output = getTurn(netNumber, sideNumber, rollNumber, team)
    return output
    
#NET, SIDE, ROLL
A0a = [[False, 1], [True, 3], [False, 3], [True, 1]]
A0b = [[False, 1], [False, 2], [False, 3], [False, 0]]
A0c = [[False, 1], [True, 1], [False, 3], [True, 3]]
A0d = [[False, 1], [False, 0], [False, 3], [False, 2]]
A1a = [[True, 1], [False, 1], [True, 3], [False, 3]]
A1b = [[False, 0], [False, 1], [False, 2], [False, 3]]
A1c = [[True, 3], [False, 1], [True, 1], [False, 3]]
A1d = [[False, 2], [False, 1], [False, 0], [False, 3]]
A2a = [[False, 3], [True, 1], [False, 1], [True, 3]]
A2b = [[False, 3], [False, 0], [False, 1], [False, 2]]
A2c = [[False, 3], [True, 3], [False, 1], [True, 1]]
A2d = [[False, 3], [False, 2], [False, 1], [False, 0]]
A3a = [[True, 3], [False, 3], [True, 1], [False, 1]]
A3b = [[False, 2], [False, 3], [False, 0], [False, 1]]
A3c = [[True, 1], [False, 3], [True, 3], [False, 1]]
A3d = [[False, 0], [False, 3], [False, 2], [False, 1]]
A4a = [[False, 0], [True, 1], [False, 2], [True, 3]]
A4b = [[True, 3], [False, 0], [True, 1], [False, 2]]
A4c = [[False, 2], [True, 3], [False, 0], [True, 1]]
A4d = [[True, 1], [False, 2], [True, 3], [False, 0]]
A5a = [[False, 2], [True, 1], [False, 0], [True, 3]]
A5b = [[True, 1], [False, 0], [True, 3], [False, 2]]
A5c = [[False, 0], [True, 3], [False, 2], [True, 1]]
A5d = [[True, 3], [False, 2], [True, 1], [False, 0]]

A0 = [A0a, A0b, A0c, A0d]
A1 = [A1a, A1b, A1c, A1d]
A2 = [A2a, A2b, A2c, A2d]
A3 = [A3a, A3b, A3c, A3d]

B0a = [[False, 1], [False, 3], [True, 3], [True, 1]]
B0b = [[False, 1], [False, 3], [False, 2], [False, 0]]
B0c = [[False, 1], [False, 3], [True, 1], [True, 3]]
B0d = [[False, 1], [False, 3], [False, 0], [False, 2]]
B1a = [[False, 3], [False, 1], [True, 1], [True, 3]]
B1b = [[False, 3], [False, 1], [False, 0], [False, 2]]
B1c = [[False, 3], [False, 1], [True, 3], [True, 1]]
B1d = [[False, 3], [False, 1], [False, 2], [False, 0]]
B2a = [[True, 1], [True, 3], [False, 1], [False, 3]]
B2b = [[False, 0], [False, 2], [False, 1], [False, 3]]
B2c = [[True, 3], [True, 1], [False, 1], [False, 3]]
B2d = [[False, 2], [False, 0], [False, 1], [False, 3]]
B3a = [[True, 3], [True, 1], [False, 3], [False, 1]]
B3b = [[False, 2], [False, 0], [False, 3], [False, 1]]
B3c = [[True, 1], [True, 3], [False, 3], [False, 1]]
B3d = [[False, 0], [False, 2], [False, 3], [False, 1]]
B4a = [[False, 0], [False, 2], [True, 1], [True, 3]]
B4b = [[True, 3], [True, 1], [False, 0], [False, 2]]
B4c = [[False, 2], [False, 0], [True, 3], [True, 1]]
B4d = [[True, 1], [True, 3], [False, 2], [False, 0]]
B5a = [[False, 0], [False, 2], [True, 3], [True, 1]]
B5b = [[True, 3], [True, 1], [False, 0], [False, 0]]
B5c = [[False, 2], [False, 0], [True, 1], [True, 3]]
B5d = [[True, 1], [True, 3], [False, 2], [False, 2]]



C0a = [[False, 1], [True, 1], [True, 3], [False, 3]]
C0b = [[False, 1], [False, 0], [False, 2], [False, 3]]
C0c = [[False, 1], [True, 3], [True, 1], [False, 3]]
C0d = [[False, 1], [False, 2], [False, 0], [False, 3]]
C1a = [[True, 3], [False, 1], [False, 3], [True, 1]]
C1b = [[False, 2], [False, 1], [False, 3], [False, 0]]
C1c = [[True, 1], [False, 1], [False, 3], [True, 3]]
C1d = [[False, 0], [False, 1], [False, 3], [False, 2]]
C2a = [[True, 1], [False, 3], [False, 1], [True, 3]]
C2b = [[False, 0], [False, 3], [False, 1], [False, 2]]
C2c = [[True, 3], [False, 3], [False, 1], [True, 1]]
C2d = [[False, 2], [False, 3], [False, 1], [False, 0]]
C3a = [[False, 3], [True, 3], [True, 1], [False, 1]]
C3b = [[False, 3], [False, 2], [False, 0], [False, 1]]
C3c = [[False, 3], [True, 1], [True, 3], [False, 1]]
C3d = [[False, 3], [False, 0], [False, 2], [False, 1]]
C4a = [[False, 0], [True, 3], [True, 1], [False, 2]]
C4b = [[True, 3], [False, 2], [False, 0], [True, 1]]
C4c = [[False, 2], [True, 1], [True, 3], [False, 0]]
C4d = [[True, 1], [False, 0], [False, 2], [True, 3]]
C5a = [[False, 0], [True, 1], [True, 3], [False, 2]]
C5b = [[True, 3], [False, 0], [False, 2], [True, 1]]
C5c = [[False, 2], [True, 3], [True, 1], [False, 0]]
C5d = [[True, 1], [False, 2], [False, 0], [True, 3]]







    
def getTurn(net, side, roll, team):
    
    turn = turnArray[net][side][roll][team]
    
    

    