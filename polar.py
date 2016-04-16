import math

def getPolarR(start_location, finish_location):
    dx = start_location['x'] - finish_location['x']
    dy = start_location['y'] - finish_location['y']
    polar_r = (dx**2 + dy**2)**0.5
    
def getPolarT(start_location, finish_location):
    dx = start_location['x'] - finish_location['x']
    dy = start_location['y'] - finish_location['y']
    polar_t = math.degrees(math.atan2(dy, dx))
    