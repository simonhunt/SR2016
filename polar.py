import math

def getPolarR(start_location, finish_location):
    dx = finish_location['x'] - start_location['x']
    dy = finish_location['y'] - start_location['y']
    polar_r = (dx**2 + dy**2)**0.5
    
def getPolarT(start_location, finish_location):
    dx = finish_location['x'] - start_location['x']
    dy = finish_location['y'] - start_location['y']
    polar_t = math.degrees(math.atan2(dy, dx))
    