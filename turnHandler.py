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
    
def getTurn(net, side, roll, team):
    
    turn = turnArray[net][side][roll][team]
    
    

    