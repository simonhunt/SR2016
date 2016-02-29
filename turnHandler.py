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
A0a = [[f, 1], [t, 3], [f, 3], [t, 1]]
A0b = [[f, 1], [f, 2], [f, 3], [f, 0]]
A0c = [[f, 1], [t, 1], [f, 3], [t, 3]]
A0d = [[f, 1], [f, 0], [f, 3], [f, 2]]
A1a = [[t, 1], [f, 1], [t, 3], [f, 3]]
A1b = [[f, 0], [f, 1], [f, 2], [f, 3]]
A1c = [[t, 3], [f, 1], [t, 1], [f, 3]]
A1d = [[f, 2], [f, 1], [f, 0], [f, 3]]
A2a = [[f, 3], [t, 1], [f, 1], [t, 3]]
A2b = [[f, 3], [f, 0], [f, 1], [f, 2]]
A2c = [[f, 3], [t, 3], [f, 1], [t, 1]]
A2d = [[f, 3], [f, 2], [f, 1], [f, 0]]
A3a = [[t, 3], [f, 3], [t, 1], [f, 1]]
A3b = [[f, 2], [f, 3], [f, 0], [f, 1]]
A3c = [[t, 1], [f, 3], [t, 3], [f, 1]]
A3d = [[f, 0], [f, 3], [f, 2], [f, 1]]
A4a = [[f, 0], [t, 1], [f, 2], [t, 3]]
A4b = [[t, 3], [f, 0], [t, 1], [f, 2]]
A4c = [[f, 2], [t, 3], [f, 0], [t, 1]]
A4d = [[t, 1], [f, 2], [t, 3], [f, 0]]
A5a = [[f, 2], [t, 1], [f, 0], [t, 3]]
A5b = [[t, 1], [f, 0], [t, 3], [f, 2]]
A5c = [[f, 0], [t, 3], [f, 2], [t, 1]]
A5d = [[t, 3], [f, 2], [t, 1], [f, 0]]

B0a = [[f, 1], [f, 3], [t, 3], [t, 1]]
B0b = [[f, 1], [f, 3], [f, 2], [f, 0]]
B0c = [[f, 1], [f, 3], [t, 1], [t, 3]]
B0d = [[f, 1], [f, 3], [f, 0], [f, 2]]
B1a = [[f, 3], [f, 1], [t, 1], [t, 3]]
B1b = [[f, 3], [f, 1], [f, 0], [f, 2]]
B1c = [[f, 3], [f, 1], [t, 3], [t, 1]]
B1d = [[f, 3], [f, 1], [f, 2], [f, 0]]
B2a = [[t, 1], [t, 3], [f, 1], [f, 3]]
B2b = [[f, 0], [f, 2], [f, 1], [f, 3]]
B2c = [[t, 3], [t, 1], [f, 1], [f, 3]]
B2d = [[f, 2], [f, 0], [f, 1], [f, 3]]
B3a = [[t, 3], [t, 1], [f, 3], [f, 1]]
B3b = [[f, 2], [f, 0], [f, 3], [f, 1]]
B3c = [[t, 1], [t, 3], [f, 3], [f, 1]]
B3d = [[f, 0], [f, 2], [f, 3], [f, 1]]
B4a = [[f, 0], [f, 2], [t, 1], [t, 3]]
B4b = [[t, 3], [t, 1], [f, 0], [f, 2]]
B4c = [[f, 2], [f, 0], [t, 3], [t, 1]]
B4d = [[t, 1], [t, 3], [f, 2], [f, 0]]
B5a = [[f, 0], [f, 2], [t, 3], [t, 1]]
B5b = [[t, 3], [t, 1], [f, 0], [f, 0]]
B5c = [[f, 2], [f, 0], [t, 1], [t, 3]]
B5d = [[t, 1], [t, 3], [f, 2], [f, 2]]

C0a = [[f, 1], [t, 1], [t, 3], [f, 3]]
C0b = [[f, 1], [f, 0], [f, 2], [f, 3]]
C0c = [[f, 1], [t, 3], [t, 1], [f, 3]]
C0d = [[f, 1], [f, 2], [f, 0], [f, 3]]
C1a = [[t, 3], [f, 1], [f, 3], [t, 1]]
C1b = [[f, 2], [f, 1], [f, 3], [f, 0]]
C1c = [[t, 1], [f, 1], [f, 3], [t, 3]]
C1d = [[f, 0], [f, 1], [f, 3], [f, 2]]
C2a = [[t, 1], [f, 3], [f, 1], [t, 3]]
C2b = [[f, 0], [f, 3], [f, 1], [f, 2]]
C2c = [[t, 3], [f, 3], [f, 1], [t, 1]]
C2d = [[f, 2], [f, 3], [f, 1], [f, 0]]
C3a = [[f, 3], [t, 3], [t, 1], [f, 1]]
C3b = [[f, 3], [f, 2], [f, 0], [f, 1]]
C3c = [[f, 3], [t, 1], [t, 3], [f, 1]]
C3d = [[f, 3], [f, 0], [f, 2], [f, 1]]
C4a = [[f, 0], [t, 3], [t, 1], [f, 2]]
C4b = [[t, 3], [f, 2], [f, 0], [t, 1]]
C4c = [[f, 2], [t, 1], [t, 3], [f, 0]]
C4d = [[t, 1], [f, 0], [f, 2], [t, 3]]
C5a = [[f, 0], [t, 1], [t, 3], [f, 2]]
C5b = [[t, 3], [f, 0], [f, 2], [t, 1]]
C5c = [[f, 2], [t, 3], [t, 1], [f, 0]]
C5d = [[t, 1], [f, 2], [f, 0], [t, 3]]


    
def getTurn(net, side, roll, team):
    
    turn = turnArray[net][side][roll][team]
    
    

    