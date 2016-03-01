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
    
    