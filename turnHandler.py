from sr.robot import NET_A, NET_B, NET_C, MARKER_TOKEN_SIDE, MARKER_TOKEN_TOP, MARKER_TOKEN_BOTTOM
from lut import TURN_TABLE
from limits import mod4

def getTurn(net, roll, code, zone):
    
    if (roll <= 45 and roll > -45):
        roll_index = 0 #a
        
    elif (roll <= -45 and roll > -135):
        roll_index = 1 #b
    
    elif (roll <= 135 and roll > 45):
        roll_index = 3 #d
    
    else:
        roll_index = 2 #c
        
    
    #if (type == MARKER_TOKEN_SIDE):
    #    pass
    #
    #elif (type == MARKER_TOKEN_TOP):
    #   sideNumber = 4
    #    
    #elif (type == MARKER_TOKEN_BOTTOM):
    #    sideNumber = 5
    
    if (net == NET_A):
        net_index = 0
        side_index = code - 34
        
    elif (net == NET_B):
        net_index = 1
        side_index = code - 40
        
    elif (net == NET_C):
        net_index = 2
        side_index = code - 46
        
    else:
        print "error marker with undefined net handled in turn handler"
        
        #defaults
        
        net_index = 0 
        side_index = code - 34 
    
    
    zone_index = zone
    
    table_output = TURN_TABLE[net_index][side_index][roll_index][zone_index]
    
    turns = [[False, 0], [False, 0], [False, 0], [False, 0]]
    
    if (table_output[0] == False):
        if (table_output[1] == 0 or table_output[1] == 2):
            turns[0] = [True, table_output[1]]
            turns[1] = [True, table_output[1]]
            turns[2] = [True, table_output[1]]
            turns[3] = [True, table_output[1]]            
        
        elif (table_output[1] == 1 or table_output[1] == 3):
            turns[0] = [True, table_output[1]]
            turns[2] = [True, mod4( - table_output[1])]
        
    else: #table_output[0] == True
        turns[1] = [True, table_output[1]]
        turns[3] = [True, mod4( - table_output[1])]   
    
    return turns

    