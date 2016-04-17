def mapToLimits(value, upper_limit = 100, lower_limit = - 100):
    output = value
    
    if (value > upper_limit):
        output = upper_limit
        
    elif (value < lower_limit):
        output = lower_limit
    return output
    
def angleMod(angle):
    output = angle
    
    while (output > 180):
        output -= 360
        
    while (output <= -180):
        output += 360
        
    return output
    
def mod4(number):
    output = number
    # output= number%4 is the same as this function. % is the modulus operator
    while (output >= 4):
        output -= 4
        
    while (output < 0):
        output += 4
        
    return output
    
def rightAngleMod(angle):
    output = angle
    
    while (output > 45):
        output -= 90
        
    while (output <= -45):
        output += 90
        
    return output
    
    